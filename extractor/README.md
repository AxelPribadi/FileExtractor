# **Ingestor (Data Extractor)**

## **Overview**
The data extractor is a component of the FileExtractor project that is responsible for processing uploaded files. It monitors the downloads folder for new files, extracts their content, generates embeddings, and stores the processed data in a LanceDB table. This enables efficient retrieval of context for a LLM to generate intelligent responses to user queries.

### **Subprocesses**

#### **Watcher**
- Monitors the downloads folder for newly uploaded files.
- Schedules ingestion tasks to process the files.
- Ensures timely processing of files.

#### **Ingestor**
- Implements an algorithm that determines the optimal starting point for ingestion.
- Extracts content from uploaded files.
- Breaks down data into smaller, manageable chunks for efficient processing.
- Generates embeddings for the extracted content.
- Stores the processed data in the LanceDB vector database.


## **Setup**
1. Navigate to the Data Extractor project directory:
```zsh
cd extractor
```

2. Start the extractor module:
```zsh
python3 -m app.main
```

## **Additional Information**
