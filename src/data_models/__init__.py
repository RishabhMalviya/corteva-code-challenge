import os

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


engine = create_engine(os.getenv('DB_URL'), echo=os.getenv('DEBUG')=="True")


class Base(DeclarativeBase):
    pass
