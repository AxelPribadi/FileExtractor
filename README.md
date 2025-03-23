# FileExtractor

## What is this all about?
FileExtractor is a retrieval augmented generation (RAG) pipeline designed to extract, process and store data in a vector database. This data serves as context to an LLM model, which results to a more intelligent and context-aware response for the users.

## Project Structure (As of Now)
This repository consists of two main components:

### 1. File Portal (`app/`)  
The File Portal is responsible for handling file uploads and organizing them into the appropriate directory before processing.
- Accepts and uploads files into the downloads folder
- Ensures proper file organization before ingestion
- Acts as the entry point for files before they are processed

### 2. Extractor (`extractor/`)
The Extractor is responsible for processing the uploaded files by watching the downloads folder and running scheduled ingestion jobs.
- Monitors the downloads folder for new files
- Extracts file content and chunks the data
- Generates embeddings for storage
- Stores the processed data in a LanceDB vector database

### Workflow Summary
1. The File Portal accepts file uploads and places them into the downloads folder.
2. The Extractor runs periodically, detects new files, and processes them.
3. Extracted and chunked content is embedded and stored in LanceDB for retrieval.
4. The stored data is later used to enhance LLM responses with relevant contextual information.

Both components work together to form an efficient RAG pipeline for document ingestion and retrieval. 🚀
