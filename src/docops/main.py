from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.orm import Session

from docops.db import Base, engine, get_session
from docops.models import DocumentRow


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="DocOps", lifespan=lifespan)

SessionDep = Annotated[Session, Depends(get_session)]


class DocumentIn(BaseModel):
    title: str
    content: str


class Document(DocumentIn):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/documents", status_code=201)
def create_document(payload: DocumentIn, session: SessionDep) -> Document:
    row = DocumentRow(**payload.model_dump())
    session.add(row)
    session.commit()
    session.refresh(row)
    return Document.model_validate(row)


@app.get("/documents")
def list_documents(session: SessionDep) -> list[Document]:
    rows = session.scalars(select(DocumentRow).order_by(DocumentRow.id)).all()
    return [Document.model_validate(row) for row in rows]


@app.get("/documents/{document_id}")
def get_document(document_id: int, session: SessionDep) -> Document:
    row = session.get(DocumentRow, document_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return Document.model_validate(row)


@app.delete("/documents/{document_id}", status_code=204)
def delete_document(document_id: int, session: SessionDep) -> None:
    row = session.get(DocumentRow, document_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Document not found")
    session.delete(row)
    session.commit()
