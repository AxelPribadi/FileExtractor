# **File Input Portal**

## **Overview**
The file input portal is responsible for handling file uploads, organizing them into the correct directories, and preparing them for processing in the `extractor/` module. It currently supports various document formats and integrates with LanceDB for efficient data storage and retrieval.

### **Modes of Operation**
The file input portal has two modes of action:

1. **Reset Mode**
   - Clears all existing data from the LanceDB table.
   - Inserts newly extracted data from the uploaded files.

2. **Upsert Mode**
   - Updates the LanceDB table with data from the newly uploaded files.
   - Preserves and adds to the existing collection.

## **Setup**
1. Navigate to the File Portal project directory:
```zsh
cd file_portal
```

2. Start the FastAPI server with uvicorn:
```zsh
uvicorn app.main:app --reload
```

## **Additional Information**

### **Supported File Formats**
The portal currently supports the following file types:

✅ **Documents**: `pdf`, `txt`, `doc`, `docx`

✅ **Images**: `jpg`, `jpeg`, `png`, `svg`

### **Upcoming Features**
🔜 **Tabular Data Support**: `csv`, `tsv`, `xls`, `xlsx`
