from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from typing import Annotated

from DataBase.settings.config import settings

#Движое алхимии
engine = create_async_engine(
    url=settings.DATABASE_URL_pymysql,
    echo=False,
)

session_factory = async_sessionmaker(engine, expire_on_commit=False) #Фабрика сессий

str_256 = Annotated[str, 256]
str_32 = Annotated[str, 32]

class Base(DeclarativeBase): #Основной класс
    type_annotation_map = {
        str_256: String(256),
        str_32: String(32)
    }