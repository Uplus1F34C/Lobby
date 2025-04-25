from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, String

from typing import Annotated

# from config import settings

#Движое алхимии
engine = create_engine(
    # url=settings.DATABASE_URL_pymysql,
    url="mysql+pymysql://root:zjq.2-;HSOM4@localhost:3306/kvant_game",
    echo=False,
)

session_factory = sessionmaker(engine) #Фабрика сессий

str_256 = Annotated[str, 256]
str_32 = Annotated[str, 32]

class Base(DeclarativeBase): #Основной класс
    type_annotation_map = {
        str_256: String(256),
        str_32: String(32)
    }