# Agno does all the internal processes from extracting -> chunking -> embedding -> storing data in lanceDB
import os
import shutil

from agno.agent import Agent, AgentKnowledge
from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader, PDFImageReader
from agno.knowledge.text import TextKnowledgeBase, TextReader
from agno.knowledge.docx import DocxKnowledgeBase, DocxReader
from agno.knowledge.combined import CombinedKnowledgeBase
from agno.document.chunking.document import DocumentChunking
from agno.embedder.openai import OpenAIEmbedder
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType
from pydantic import BaseModel
from typing import List

from app.core.config import settings
from app.utils.file_metadata import FileMetadata
from app.utils.util import *


class Ingestor(BaseModel):
    table_name: str
    vector_db: object = None

    def build_vector_db(self):
        """
        Initializes and returns a LanceDB vector database instance.
        """
        vector_db = LanceDb(
            table_name=self.table_name,
            uri=settings.LANCE_DB_URI,
            search_type=SearchType.keyword,
            embedder=OpenAIEmbedder(api_key=settings.OPENAI_API_KEY)
        )

        return vector_db

    def build_knowledge_base(self, metadata: FileMetadata):
        """
        Determines the appropriate knowledge base type based on the file extension 
        and initializes it with the given vector database.

        Args:
            metadata (FileMetadata): Metadata object containing file details.
            vector_db (LanceDb): The vector database instance to use.

        Returns:
            An initialized KnowledgeBase instance (PDF, Text, or Docx).
        """
        # Check which knowledge base to use
        if metadata.extension == "pdf":
            knowledge_base = PDFKnowledgeBase(
                path=os.path.join(settings.DOWNLOADS_FOLDER_PATH, metadata.original_filename),
                vector_db=self.vector_db,
                reader=PDFImageReader(chunk=True),
                chunking_strategy=DocumentChunking(chunk_size=1000, overlap=200)
            )
        elif metadata.extension == "txt":
            knowledge_base =  TextKnowledgeBase(
                path=os.path.join(settings.DOWNLOADS_FOLDER_PATH, metadata.original_filename),
                vector_db=self.vector_db,
                reader=TextReader(chunk=True),
                chunking_strategy=DocumentChunking(chunk_size=1000, overlap=200)
            )
        elif metadata.extension == "docx" or metadata.extension == "doc":
            knowledge_base =  DocxKnowledgeBase(
                path=os.path.join(settings.DOWNLOADS_FOLDER_PATH, metadata.original_filename),
                vector_db=self.vector_db,
                reader=DocxReader(chunk=True),
                chunking_strategy=DocumentChunking(chunk_size=1000, overlap=200)
            )
        else:
            raise Exception(f"Unsupported file type: {metadata.extension}")

        return knowledge_base

    def build_combined_knowledge_base(self, files: List[str]):
        """
        Builds a combined knowledge base from multiple files.

        Args:
            files (List[str]): List of file paths to process.

        Returns:
            CombinedKnowledgeBase: A combined knowledge base with all sources.
        """
        sources = [self.build_knowledge_base(FileMetadata(file)) for file in files]

        combined_knowledge_base = CombinedKnowledgeBase(
            sources=sources,
            vector_db=self.vector_db,
        )

        return combined_knowledge_base

    def ingest(self, files: List[str]):
        """
        Processes a file by extracting metadata, initializing the vector database,
        and loading the knowledge base. Supports resetting or upserting data.

        Args:
            file (str): The path to the file to be processed.
            table_name (str): The name of the LanceDB table.

        Returns:
            None
        """

        if not files:
            print("No Files to Process")
            return

        self.vector_db = self.build_vector_db()

        # Algorithm to enhance workload
        optimized_files, unused_files = self.optimizer(self.sort_files(files))

        try:
            knowledge_base = self.build_combined_knowledge_base(optimized_files)
            
            if FileMetadata(optimized_files[0]).action == "reset":        
                knowledge_base.load(recreate=True)
            else:
                knowledge_base.load(upsert=True)

        except Exception as e:
            print(f"Error: {e}")

            for file in optimized_files:
                move_files(
                    file,
                    settings.DOWNLOADS_FOLDER_PATH,
                    settings.FAILED_FOLDER_PATH
                )

        # Move optimized files to the processed folder
        for file in optimized_files:
            move_files(
                file,
                settings.DOWNLOADS_FOLDER_PATH,
                settings.PROCESSED_FOLDER_PATH
            )

        # Move redundant files to the processed folder
        for file in unused_files:
            move_files(
                file,
                settings.DOWNLOADS_FOLDER_PATH,
                settings.PROCESSED_FOLDER_PATH
            )

    def optimizer(self, files: List[str]):
        """
        Optimizes the file processing order based on reset actions.
        
        Args:
            files (List[str]): Sorted list of files to optimize.
            
        Returns:
            Tuple[List[str], List[str]]: Tuple of (files to process, unused files).
        """
        # for i in range(len(files)-1, 0, -1):
        #     if (FileMetadata(files[i]).action == "reset"):
        #         return files[i:], files[:i]
        # return files, []

        latest_timestamp = 0
        index = 0

        for i in range(len(files)-1, -1, -1):
            metadata = FileMetadata(files[i])

            if metadata.action == "reset":
                if latest_timestamp == 0:
                    latest_timestamp = metadata.timestamp
                    index = i
                elif metadata.timestamp == latest_timestamp:
                    index = i
                else:
                    break
            elif latest_timestamp != 0:
                break
            
        if latest_timestamp != 0:
            return files[index:], files[:index]
        
        return files, []
    
    def sort_files(self, files: List[str]):
        """
        Sorts files by timestamp.
        
        Args:
            files (List[str]): List of files to sort.
            
        Returns:
            List[str]: Sorted list of files.
        """
        return sorted(files, key=lambda file: FileMetadata(file).timestamp)
