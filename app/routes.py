import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path


filepath = "/Users/axel/Documents/GitHub Repo/FileExtractor/downloads"
DOWNLOADS_FOLDER = filepath
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)


router = FastAPI()

@router.post("/upload") # upload file from file portal
async def upload_file(file: UploadFile = File(...)):
    allowed_ext = [".pdf", ".doc", ".docx", ".txt"]    
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in allowed_ext:
        raise HTTPException(status_code=400, detail="❌ Invalid file type!")

    file_location = os.path.join(DOWNLOADS_FOLDER, file.filename)
    counter = 1
    while os.path.exists(file_location):
        name, ext = os.path.splitext(file.filename)
        file_location = os.path.join(DOWNLOADS_FOLDER, f"{name}_{counter}{ext}")
        counter += 1

    try:
        with open(file_location, "wb") as f:
            while chunk := await file.read(1024 * 1024):  # Read in 1MB chunks
                f.write(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Upload failed: {str(e)}")
    
    return {"message": "✅ File uploaded successfully!", "filename": file.filename}
