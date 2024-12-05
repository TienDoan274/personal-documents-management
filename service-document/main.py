from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
 
 #################################
 #          FOLDER               #
 #################################
        
# CREATE
@app.post('/folders', response_model= schemas.Folder)
async def create_folder( folder: schemas.FolderCreate, db: Session = Depends(get_db)):
    db_folder = db.query(models.FOLDER).filter(models.FOLDER.FOLDER_NAME == folder.FOLDER_NAME).first()
    if db_folder:
        raise HTTPException(status_code=400, detail="Folder already exists")
    new_folder = models.FOLDER(USER_ID=folder.USER_ID, FOLDER_NAME=folder.FOLDER_NAME)
    db.add(new_folder)
    db.commit()
    db.refresh(new_folder)
    return new_folder

# READ
@app.get("/folders/{folder_id}", response_model=schemas.Folder )
async def get_folder( folder_id: int, db: Session = Depends(get_db)):
    folder = db.query(models.FOLDER).filter(models.FOLDER.id == folder_id).first()
    
    if not folder: 
        raise HTTPException(status_code=404, detail="Folder not found")
    
    folder_document= db.query(models.FOLDER_DOCUMENT).filter(models.FOLDER_DOCUMENT.folder_id==folder_id).all()
    document_ids = [fd.document_id for fd in folder_document]
    
    # Retrieve document detail
    documents= db.query(models.DOCUMENT).filter(models.DOCUMENT.id.in_(document_ids)).all()
    
    document_list = [
        schemas.Document(
            id=doc.id,
            FOLDER_ID= folder_id,
            TITLE=doc.TITLE,
            FILE_TYPE=doc.FILE_TYPE,
            CREATE_DATE=doc.CREATE_DATE,
            UPDATE_DATE=doc.UPDATE_DATE
        ) for doc in documents]
    
    return schemas.Folder(
        id= folder.id,
        USER_ID=folder.USER_ID,
        FOLDER_NAME=folder.FOLDER_NAME,
        CREATE_DATE=folder.CREATE_DATE,
        UPDATE_DATE=folder.UPDATE_DATE,
        documents=document_list
    )
    
# UPDATE -> update what?

    
# DELETE
def delete_documnent_by_id(document_id: int, db=Session):
    document = db.query(models.DOCUMENT).filter(models.DOCUMENT.id==document_id).first()
    if document:
        folder_document = db.query(models.FOLDER_DOCUMENT).filter(
            models.FOLDER_DOCUMENT.document_id==document_id
        ).first()
        if folder_document:
            db.delete(folder_document)
        
        db.delete(document)
        db.commit()

@app.delete("/folders/{folder_id}", response_model=schemas.Folder)
async def delete_folder( folder_id: int, db: Session = Depends(get_db) ):
    folder = db.query(models.FOLDER).filter(models.FOLDER.id==folder_id).first()
    
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    
    # xóa tất cả các document trong folder
    folder_documents= db.query(models.FOLDER_DOCUMENT).filter(models.FOLDER_DOCUMENT.folder_id==folder_id).all()
    document_ids = [fd.document_id for fd in folder_documents]
    
    for doc_id in document_ids:
        delete_documnent_by_id(doc_id, db)
        
    db.delete(folder)
    db.commit()
    
    return schemas.Folder(
        id=folder.id,
        USER_ID=folder.USER_ID,
        FOLDER_NAME=folder.FOLDER_NAME,
        CREATE_DATE=folder.CREATE_DATE,
        UPDATE_DATE=folder.UPDATE_DATE,
        documents=[]
    )
    
    
    
  #################################
 #          DOCUMENT              #
 #################################

# CREATE
@app.post('/documents', response_model= schemas.Document)
async def create_document( 
                        document: schemas.DocumentCreate,
                        db: Session = Depends(get_db)
):
    folder= db.query(models.FOLDER).filter(models.FOLDER.id==document.FOLDER_ID).first()
    if not folder:
        raise HTTPException(status_code=404, detail="Folder not found")
    
    # Retrieve all documents in the folder via FOLDER_DOCUMENT
    folder_document= db.query(models.FOLDER_DOCUMENT).filter(models.FOLDER_DOCUMENT.folder_id==document.FOLDER_ID).all()
    
    # Map document IDs to their titles
    document_ids = [fd.document_id for fd in folder_document]
    existing_titles = db.query(models.DOCUMENT.TITLE).filter(models.FOLDER_DOCUMENT.document_id.in_(document_ids)).all()
    existing_titles = {title[0] for title in existing_titles}# Convert list of tuples to set for quick lookup
    if document.TITLE in existing_titles:
        raise HTTPException(status_code=400, detail="A document with this title already exists in the folder")
    
    #file_content = await file.read()
    
    new_document = models.DOCUMENT(
        TITLE= document.TITLE,
        FILE_TYPE= document.FILE_TYPE,
        #FILE_CONTENT=file_content
    )
    
    db.add(new_document) # add to DOCUMENT model
    db.commit()
    db.refresh(new_document)
    
    # add the folder-document relationship
    folder_document= models.FOLDER_DOCUMENT(
        folder_id= document.FOLDER_ID,
        document_id= new_document.id
    )
    db.add(folder_document) # add to FOLDER_DOCUMENT model
    db.commit()
    
    return schemas.Document(
        id= new_document.id,
        FOLDER_ID= document.FOLDER_ID,
        TITLE= new_document.TITLE,
        FILE_TYPE= new_document.FILE_TYPE,
        CREATE_DATE= new_document.CREATE_DATE,
        UPDATE_DATE= new_document.UPDATE_DATE,
    )

# READ
@app.get('/documents/{document_id}', response_model=schemas.Document)
async def read_document(document_id: int, db: Session=Depends(get_db)):
    document = db.query(models.DOCUMENT).filter(models.DOCUMENT.id==document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    folder_document = db.query(models.FOLDER_DOCUMENT).filter(models.FOLDER_DOCUMENT.document_id==document_id).first()
    
    return schemas.Document(
        id=document.id,
        FOLDER_ID=folder_document.folder_id if folder_document else None,
        TITLE=document.TITLE,
        FILE_TYPE=document.FILE_TYPE,
        CREATE_DATE=document.CREATE_DATE,
        UPDATE_DATE=document.UPDATE_DATE,
    )
    


# UPDATE -> update what?


# DELETE
@app.delete('/documents/{document_id}', response_model=schemas.Document)
async def delete_document(document_id: int, db: Session=Depends(get_db)):
    document = db.query(models.DOCUMENT).filter(models.DOCUMENT.id==document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    folder_document = db.query(models.FOLDER_DOCUMENT).filter(models.FOLDER_DOCUMENT.document_id==document_id).first()
    if folder_document:
        db.delete(folder_document)
    db.delete(document)
    db.commit()
    
    return schemas.Document(
        id=document.id,
        FOLDER_ID=folder_document.folder_id if folder_document else None,
        TITLE=document.TITLE,
        FILE_TYPE=document.FILE_TYPE,
        CREATE_DATE=document.CREATE_DATE,
        UPDATE_DATE=document.UPDATE_DATE,
    )
    
