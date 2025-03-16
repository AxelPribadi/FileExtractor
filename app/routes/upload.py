import os
from fastapi import APIRouter, UploadFile, HTTPException, Request, File, Form
from fastapi.templating import Jinja2Templates
from pathlib import Path
from typing import List
from app.services.file_service import *

filepath = "/Users/axel/Documents/GitHub Repo/FileExtractor/downloads"
DOWNLOADS_FOLDER = filepath
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

templates = Jinja2Templates(directory="app/templates/")

router = APIRouter()

@router.post("/upload")  # upload file from file portal
async def upload_file(
    request: Request, 
    filenames: List[str] = Form(...),
    files: list[UploadFile] = File(...)
):
    saved_files = []
    try:
        print(filenames, files)
        print(len(filenames), len(files))

        # Validate input lengths match
        if len(filenames) != len(files):
            raise Exception("Number of filenames doesn't match number of files")
            
        for _filename, _file in zip(filenames, files):
            ext = get_file_extension(_file.filename)
            
            # Categorize file using the class
            categorizer = FileCategorizer(_filename, ext, "/Users/axel/Documents/GitHub Repo/FileExtractor/downloads/")
            categorizer.categorize()
            file_location, folder_name = categorizer.get_file_details()
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(file_location), exist_ok=True)
            
            # Store into local storage
            with open(file_location, "wb") as f:
                f.write(await _file.read())
            
            # Upload to S3
            # conn.s3_juwai_conn.store(
            #     local_file=file_location,
            #     s3_filename=_filename,
            #     s3_folder=folder_name
            # )
            
            saved_files.append(_file.filename)
        
        return templates.TemplateResponse("success.html", {"request": request, "saved_files": saved_files})
        
    except Exception as e:
        return templates.TemplateResponse("failed.html", {"request": request, "error": str(e)})