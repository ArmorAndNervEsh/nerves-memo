from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://nerv:nervDatabase@localhost/nerv_database"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Task(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(Text)
    isFinished = Column(Boolean)


Base.metadata.create_all(bind=engine)

app = FastAPI()


class TaskResponse(BaseModel):
    id: int
    name: str
    description: str
    isFinished: bool


class TaskCreate(BaseModel):
    name: str
    description: str


@app.post("/items/", response_model=TaskResponse)
def create_item(item: TaskCreate):
    db = SessionLocal()
    db_item = Task(name=item.name,
                   description=item.description,
                   isFinished=False)
    db.add(db_item)
    db.commit()
    response = TaskResponse(id=db_item.id,
                            name=db_item.name,
                            description=db_item.description,
                            isFinished=db_item.isFinished)
    db.refresh(db_item)
    db.close()
    return response


@app.get("/items/{item_id}", response_model=TaskResponse)
def read_item(item_id: int):
    db = SessionLocal()
    db_item = db.query(Task).filter(Task.id == item_id).first()
    db.close()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return TaskResponse(id=db_item.id,
                        name=db_item.name,
                        description=db_item.description,
                        isFinished=db_item.isFinished)
