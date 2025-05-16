from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from typing import Annotated

from DataBase.settings.config import settings

engine = create_async_engine(
    url=settings.DATABASE_URL_pymysql,
)

session_factory = async_sessionmaker(engine, expire_on_commit=False) #Фабрика сессий

str_256 = Annotated[str, 256]
str_32 = Annotated[str, 32]
class Base(DeclarativeBase): #Основной класс
    type_annotation_map = {
        str_256: String(256),
        str_32: String(32)
    }