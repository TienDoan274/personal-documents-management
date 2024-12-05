from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, LargeBinary
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

# Folder Model
class FOLDER(Base):
    __tablename__ = "FOLDER"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    USER_ID = Column(Integer)  # Assuming USER_ID is an integer, add your desired type
    FOLDER_NAME = Column(String(255), index=True)  # Folder name
    CREATE_DATE = Column(DateTime, default=func.now())  # Creation date, default to current time
    UPDATE_DATE = Column(DateTime, default=func.now(), onupdate=func.now())  # Updated time, auto-updated

    # Relationship with FOLDER_DOCUMENT
    documents = relationship("FOLDER_DOCUMENT", back_populates="folder")


# Document Model
class DOCUMENT(Base):
    __tablename__ = "DOCUMENT"

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    TITLE = Column(String(255), index=True)  # Title of the document
    FILE_TYPE = Column(String(50))  # File type (e.g., pdf, docx, etc.)
    #FILE_CONTENT = Column(LargeBinary)
    CREATE_DATE = Column(DateTime, default=func.now())  # Creation date, default to current time
    UPDATE_DATE = Column(DateTime, default=func.now(), onupdate=func.now())  # Updated time, auto-updated

    # Relationship with FOLDER_DOCUMENT
    folders = relationship("FOLDER_DOCUMENT", back_populates="document")


# Folder-Document Relationship Model (many-to-many)
class FOLDER_DOCUMENT(Base):
    __tablename__ = 'FOLDER_DOCUMENT'

    folder_id = Column(Integer, ForeignKey('FOLDER.id'), primary_key=True)
    document_id = Column(Integer, ForeignKey('DOCUMENT.id'), primary_key=True)

    # Define the relationship in both directions
    folder = relationship("FOLDER", back_populates='documents')
    document = relationship("DOCUMENT", back_populates="folders")
