from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

#############################################
class DocumentBase(BaseModel):
    TITLE: str
    FILE_TYPE: str
    #FILE_CONTENT: bytes
    
    class Config:
        orm_mode = True

# Schema for creating a document (without the ID field)
class DocumentCreate(BaseModel):
    TITLE: str
    FOLDER_ID: int
    FILE_TYPE: str
    
    class Config:
        orm_mode = True

# Schema for reading document data (includes the ID field)
class Document(DocumentBase):
    id: int
    FOLDER_ID: int
    TITLE: str
    FILE_TYPE: str
    CREATE_DATE: Optional[datetime] = None
    UPDATE_DATE: Optional[datetime] = None
    
    
    class Config:
        orm_mode = True
###########################################

# Folder Pydantic Schema
class FolderBase(BaseModel):
    USER_ID: int
    FOLDER_NAME: str
    
    
    class Config:
        orm_mode = True

# Schema for creating a folder (without the ID field)
class FolderCreate(BaseModel):
    USER_ID: int
    FOLDER_NAME: str
    
    class Config:
        orm_mode = True

# Schema for reading folder data (includes the ID field)
class Folder(FolderBase):
    id: int
    USER_ID: int
    FOLDER_NAME: str
    CREATE_DATE: Optional[datetime] = None
    UPDATE_DATE: Optional[datetime] = None
    documents: List[Document] = [] # List of full Document objects
    
    class Config:
        orm_mode = True
        
        
########################################################
class FolderDocumentBase(BaseModel):
    folder_id: int
    document_id: int

    class Config:
        orm_mode = True

# Schema for creating a folder-document association
class FolderDocumentCreate(FolderDocumentBase):
    pass

# Schema for reading a folder-document association (not often used directly)
class FolderDocument(FolderDocumentBase):
    folder_id: int
    document_id: int

    class Config:
        orm_mode = True
