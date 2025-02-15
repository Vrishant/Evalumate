from .nlp.nlp_nlkt import generate_answer_with_rag, evaluate_answers
from fastapi import FastAPI, Form, UploadFile, Depends
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, SessionLocal
from .vector_store import VectorStore


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
@app.get("/blog")
def hello():
    return {"message": "Hello, World!"}
"""


@app.post("/document/upload", response_model=schemas.Document)
async def upload_file(
    file: UploadFile = Form(...),
    chatroom_No: int = Form(...),
    db: Session = Depends(get_db),
):
    file_content = await file.read()
    metadata = {
        "chatroom_No": chatroom_No,
        "file_name": file.filename,
        "file_type": file.content_type,
    }
    vector_id = VectorStore.store_vector(file_content, metadata)

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
    results = VectorStore.find_similar(query, top_k)

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


@app.post("/document/evaluate")
async def evaluate_student_answers(student_answers: dict):
    ideal_answers = {q: generate_answer_with_rag(q) for q in student_answers.keys()}
    evaluation_results = evaluate_answers(student_answers, ideal_answers)
    return evaluation_results
