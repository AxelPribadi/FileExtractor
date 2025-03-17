# from dataclasses import dataclass
# from pathlib import Path
# import os

# # Define accepted extensions globally
# DOCUMENT_EXT = [".pdf", ".doc", ".docx", ".txt"]
# IMAGE_EXT = [".jpg", ".jpeg", ".png", ".svg"]


# class FileCategorizer:
#     CATEGORY_RULES = {
#         "DOCUMENT_EXT": {
#             "keyword": "documentContext_",
#             "path": "documentContext/Active/",
#             "accepted_ext": DOCUMENT_EXT
#         },
#         "IMAGE_EXT": {
#             "keyword": "imageGenerator_",
#             "path": "imageGenerator/Active/",
#             "accepted_ext": IMAGE_EXT
#         },
#     }
    
#     def __init__(self, filename, ext, output_folder):
#         self.filename = filename
#         self.ext = ext
#         self.output_folder = output_folder
#         self.file_location = None
#         self.folder_name = None
    
#     def categorize(self):
#         for category, details in self.CATEGORY_RULES.items():
#             # Check if ext is in the appropriate extension list and filename has the keyword
#             if (
#                 (category == "DOCUMENT_EXT" and self.ext in DOCUMENT_EXT) or
#                 (category == "IMAGE_EXT" and self.ext in IMAGE_EXT)
#             ) and details["keyword"] in self.filename:
#                 self.file_location = os.path.join(self.output_folder, details["path"], self.filename)
#                 # self.folder_name = details["s3_folder"]
#                 return
            
#         raise Exception(f"Unsupported file type or filename format: {self.ext}")
    
#     def get_file_details(self):
#         return self.file_location # , self.folder_name

# def get_file_extension(filename):
#     return Path(filename).suffix

# # def get_file_metadata(file):
# #     raw_file = Path(file)
# #     raw_filename = raw_file.name
# #     ext = raw_file.suffix

# #     file_splits = raw_filename.split("_")    
# #     app, action, filename, timestamp = file_splits[0], file_splits[1], file_splits[2], file_splits[3]

# #     return {"app": app,
# #             "action": action,
# #             "filename": filename,
# #             "timestamp": timestamp,
# #             "ext": ext
# #             }





from pathlib import Path
import os

# Define accepted extensions globally
DOCUMENT_EXT = [".pdf", ".doc", ".docx", ".txt"]
IMAGE_EXT = [".jpg", ".jpeg", ".png", ".svg"]

class FileCategorizer:
    CATEGORY_RULES = {
        "DOCUMENT_EXT": {
            "keyword": "documentContext_",
            "path": "documentContext/Active/",
            # "s3_folder": "AI_DATA/documentContext/Active"
        },
        "IMAGE_EXT": {
            "keyword": "imageGenerator_",
            "path": "imageGenerator/Active/",
            # "s3_folder": "AI_DATA/imageGenerator/Active"
        },
    }
    
    def __init__(self, filename, ext, output_folder):
        self.filename = filename
        self.ext = ext
        self.output_folder = output_folder
        self.file_location = None
        # self.folder_name = None
    
    def categorize(self):
        for category, details in self.CATEGORY_RULES.items():
            # Check if ext is in the appropriate extension list and filename has the keyword
            if (
                (category == "DOCUMENT_EXT" and self.ext in DOCUMENT_EXT) or
                (category == "IMAGE_EXT" and self.ext in IMAGE_EXT)
            ) and details["keyword"] in self.filename:
                self.file_location = os.path.join(self.output_folder, details["path"], self.filename)
                # self.folder_name = details["s3_folder"]
                return
            
        raise Exception(f"Unsupported file type or filename format: {self.ext}")
    
    def get_file_details(self):
        return self.file_location #, self.folder_name

def get_file_extension(filename):
    return Path(filename).suffix

def get_file_metadata(file):
    raw_file = Path(file)
    raw_filename = raw_file.name
    ext = raw_file.suffix

    file_splits = raw_filename.split("_")    
    app, action, filename, timestamp = file_splits[0], file_splits[1], file_splits[2], file_splits[3]

    return {"app": app,
            "action": action,
            "filename": filename,
            "timestamp": timestamp,
            "ext": ext
            }

