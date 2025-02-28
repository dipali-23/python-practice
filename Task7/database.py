from sqlmodel import create_engine,Session
from fastapi import Depends, FastAPI, HTTPException, Query
from typing import Annotated



DATABASE_URL = 'postgresql://postgres:postgres@localhost/fastapi'

engine = create_engine(DATABASE_URL,echo=True)


def get_session():
   with Session(engine) as session:
       yield session

SessionDep = Annotated[Session, Depends(get_session)]
