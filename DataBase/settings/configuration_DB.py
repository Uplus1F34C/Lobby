from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from typing import Annotated

from DataBase.Settings.config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL_pymysql
)

session_factory = async_sessionmaker(engine, expire_on_commit=False) #Фабрика сессий

intpk = Annotated[int, mapped_column(primary_key=True)]
str_256 = Annotated[str, 256]
str_32 = Annotated[str, 32]

class Base(DeclarativeBase): #Основной класс
    type_annotation_map = {
        str_256: String(256),
        str_32: String(32)
    }