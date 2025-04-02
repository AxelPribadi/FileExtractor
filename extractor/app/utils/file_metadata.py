from dataclasses import dataclass
from pathlib import Path
from pydantic import BaseModel, Field

class FileMetadata(BaseModel):
    original_filename: str
    app_id: str = Field(..., min_length=1)
    action: str = Field(..., min_length=1)
    filename: str = ""
    timestamp: str = Field(..., max_length=14)
    extension: str = ""

    def __init__(self, file: str):
        file_path = Path(file)
        raw_filename = file_path.stem.split("_")

        if len(raw_filename) != 4:
            raise ValueError(f"Invalid file naming convention: {file}")
            
        super().__init__(
            original_filename=file,
            app_id=raw_filename[0],
            action=raw_filename[1],
            filename=raw_filename[2],
            timestamp=raw_filename[3],
            extension=file_path.suffix.lstrip(".")
        )

