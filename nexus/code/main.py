from click import File
from fastapi import FastAPI, Form, UploadFile
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal
from .vector_store import VectorStore
from nexus.code import vector_store


app = FastAPI()
vector_store = VectorStore()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/document/upload", response_model=schemas.Document)
async def upload_file(
    file: UploadFile = File(...),
    chatroom_No: int = Form(...),
    db: Session = Depends(get_db),
):
    file_content = await file.read()
    metadata = {
        "chatroom_No": chatroom_No,
        "file_name": file.filename,
        "file_type": file.content_type,
    }
    vector_id = vector_store.store_document(file_content, metadata)

    db_document = models.Nex_doc(
        chatroom_No=chatroom_No,
        file_name=file.filename,
        file_type=file.content_type,
        vector_id=vector_id,
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return db_document


@app.get("/document/search")
async def search_documents(query: str, top_k: int = 5, db: Session = Depends(get_db)):
    results = vector_store.search_similar(query, top_k)

    documents = []
    for match in results.matches:
        doc = (
            db.query(models.Nex_doc)
            .filter(models.Nex_doc.vector_id == match.id)
            .first()
        )
        if doc:
            documents.append(doc)

    return documents
