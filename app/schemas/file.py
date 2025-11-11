from pydantic import BaseModel, ConfigDict
from typing import Optional
import uuid
from datetime import datetime
from enum import Enum

class FileOperationType(str, Enum):
    CONVERT_JPG_TO_PNG = "convert_jpg_to_png"
    CONVERT_PNG_TO_JPG = "convert_png_to_jpg"
    CONVERT_TXT_TO_PDF = "convert_txt_to_pdf"
    COMPRESS_ZIP = "compress_zip"
    RESIZE_IMAGE = "resize_image"

class FileBase(BaseModel):
    original_filename: str

class FileCreate(FileBase):
    user_id: uuid.UUID
    stored_filename: str
    file_path: str
    file_size: int
    mime_type: str
    extension: str

class FileUpload(BaseModel):
    operation: FileOperationType

class FileResponse(FileBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID
    user_id: uuid.UUID
    stored_filename: str
    file_path: str
    file_size: int
    mime_type: str
    extension: str
    is_processed: bool
    uploaded_at: datetime

class FileListResponse(BaseModel):
    files: list[FileResponse]
    total_count: int
    total_size: int  

class FileConversionParameters(BaseModel):
    width: Optional[int] = None
    height: Optional[int] = None
    quality: Optional[int] = 95