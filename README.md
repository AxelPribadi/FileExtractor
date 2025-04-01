# **FileExtractor**

## **Overview**
FileExtractor is a Retrieval-Augmented Generation (RAG) pipeline designed to efficiently extract, process, and store data in a vector database. This data is used as context for a large language model (LLM), enabling it to generate more intelligent, context-aware responses to user queries.

## **Project Structure**
As of now, this repository consists of three primary components:

### **1. File Portal (`app/`)**
The File Portal is responsible for handling file uploads and organizing them into appropriate directories before they are processed.
- Accepts and uploads files to the downloads folder.
- Ensures proper organization of files before ingestion.
- Acts as the entry point for files prior to processing.

### **2. Extractor (`extractor/`)**
The Extractor is responsible for processing the uploaded files by monitoring the downloads folder and executing scheduled ingestion tasks.
- Monitors the downloads folder for newly uploaded files.
- Extracts content from files and chunks the data.
- Generates embeddings for efficient storage and retrieval.
- Stores processed data in the LanceDB vector database.

### **3. Chatbot (`chatbot/`)**
The Chatbot is an interactive interface that allows users to ask questions based on the data processed and stored by the system.
- Users can ask questions, and the bot generates responses based on the relevant context stored in the vector database.

## **Workflow Summary**
1. The **File Portal** accepts file uploads and places them in the downloads folder.
2. The **Extractor** periodically detects new files in the downloads folder and processes them.
3. The extracted content is chunked, embedded, and stored in **LanceDB** for efficient retrieval.
4. The **Chatbot** uses the stored data to provide contextually relevant, intelligent responses to user queries.

## **Additional Information**
More details can be found in each folder's respective `README.md`.

Together, these components form a cohesive and efficient RAG pipeline for document ingestion, context extraction, and real-time query resolution. 🚀
