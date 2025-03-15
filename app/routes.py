import os
from fastapi import APIRouter, File, UploadFile, HTTPException, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

filepath = "/Users/axel/Documents/GitHub Repo/FileExtractor/downloads"
DOWNLOADS_FOLDER = filepath
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

templates = Jinja2Templates(directory="app/templates/")

router = APIRouter()

@router.post("/upload")  # upload file from file portal
async def upload_file(request: Request, file: UploadFile = File(...)):
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
        # wriitng in chunks
        with open(file_location, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                f.write(chunk)
        return templates.TemplateResponse("success.html", {"request": request, "saved_file": file.filename})

    except Exception as e:
        return templates.TemplateResponse("failed.html", {"request": request, "error": str(e)})
