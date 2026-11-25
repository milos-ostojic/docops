from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title='DocOps')

class DocumentIn(BaseModel):
    title: str
    content:str

class Document (DocumentIn):
    id: int
    created_at: datetime


_db: dict[int, Document] = {}

@app.get("/health")
def health() -> dict[str,str]:
    return {"status": "ok"}

@app.post('/documents', status_code=201)
def create_document(payload: DocumentIn) -> Document:
    doc = Document(id=len(_db)+1, created_at=datetime.now(),**payload.model_dump())
    _db[doc.id] = doc
    return doc

@app.get('/documents')
def list_documents() -> list[Document]:
    return list(_db.values())