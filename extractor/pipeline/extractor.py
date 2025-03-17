# Agno does all the internal processes from extracting -> chunking -> embedding -> storing data in lanceDB

from agno.agent import Agent, AgentKnowledge

from agno.knowledge.pdf import PDFKnowledgeBase, PDFImageReader
from agno.knowledge.text import TextKnowledgeBase, TextReader
from agno.knowledge.docx import DocxKnowledgeBase, DocxReader

from agno.document.chunking.document import DocumentChunking
from agno.embedder.openai import OpenAIEmbedder
from agno.vectordb.lancedb import LanceDb
from agno.vectordb.search import SearchType

from extractor.models.file_metadata import FileMetadata
from extractor.core.config import settings

def build_vector_db(table_name: str):
    vector_db = LanceDb(
        table_name=table_name,
        uri=settings.LANCE_DB_URI,
        search_type=SearchType.keyword,
        embedder=OpenAIEmbedder(api_key=settings.OPENAI_API_KEY)
    )

    return vector_db

def build_knowledge_base(metadata: FileMetadata, vector_db: LanceDb):
    #check which knowledge base to use
    if metadata.extension == "pdf":
        knowledge_base = PDFKnowledgeBase(
            path=metadata.original_filename,
            vector_db=vector_db,
            reader=PDFImageReader(chunk=True),
            chunking_strategy=DocumentChunking(chunk_size=1000, overlap=200)
        )
    elif metadata.extension == "txt":
        knowledge_base =  TextKnowledgeBase(
            path=metadata.original_filename,
            vector_db=vector_db,
            reader=TextReader(chunk=True),
            chunking_strategy=DocumentChunking(chunk_size=1000, overlap=200)
        )
    else:
        knowledge_base =  DocxKnowledgeBase(
            path=metadata.original_filename,
            vector_db=vector_db,
            reader=DocxReader(chunk=True),
            chunking_strategy=DocumentChunking(chunk_size=1000, overlap=200)
        )

    return knowledge_base

def process_files(file: str, table_name: str):

    metadata = FileMetadata.from_file(file)

    vector_db = build_vector_db(table_name)
    knowledge_base = build_knowledge_base(metadata, vector_db)

    if metadata.action == "reset":
        knowledge_base.load(recreate=True)
    elif metadata.action == "upsert":
        knowledge_base.load(recreate=False)

