from sqlalchemy import String, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import event

import asyncio
from typing import Annotated
from enum import Enum
import secrets, string, bcrypt

from DataBase.settings.configuration_DB import Base, str_256, str_32, session_factory


# Помощь --------------------------------------------------------------------------
async def generate_random_code(length: int = 8, max_attempts: int = 100) -> str:
    async with session_factory() as session:
        alphabet = string.ascii_uppercase + string.digits 
        for _ in range(max_attempts):
            code = ''.join(secrets.choice(alphabet) for _ in range(length))
            result = await session.execute(
                select(TeacherClass).where(TeacherClass._code == code)
            )
            if not result.scalars().first():
                return code
        raise ValueError(f"Не удалось сгенерировать уникальный код после {max_attempts} попыток.")

class level(Enum):
    Стартовый = "Стартовый"
    Базовый = "Базовый"
    Углубленный = "Углубленный"
    Проектный = "Проектный"
class kvant(Enum):
    IT = "IT"
    Пром_дизайн = "Пром_дизайн"
    Медиа = "Медиа"
    Хай_тек = "Хай_тек"
    Космо = "Космо"
    Гео = "Гео"
    VR = "VR"
    Пром_робо = "Пром_робо"
intpk = Annotated[int, mapped_column(primary_key=True)] #id
# Помощь --------------------------------------------------------------------------


# Студент --------------------------------------------------------------------------
class StudentClass(Base):
    __tablename__ = "student"

    id: Mapped[intpk]
    name: Mapped[str_32]
    surname: Mapped[str_32]
    patronymic: Mapped[str_32]
    login: Mapped[str_256] = mapped_column(default="")
    password: Mapped[str_256] = mapped_column(default="")
    tg_id: Mapped[str] = mapped_column(String(10), default="")
    _code: Mapped[str] = mapped_column(String(8))

    marks: Mapped["MarkClass"] = relationship(back_populates="student")

    def check_password(self, password: str) -> bool: #авторизация
        if self.password is None:
            return  {"status": False, "info": "Пароль не указан"}
        if bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8')):
            return {"status": True, "info": f"Успешная утентификация", "id": self.id}
        else: 
            return {"status": False, "info": f"Неверный пароль"}
        
    async def generate_and_set_code(self):
        if not self._code:
            self._code = await generate_random_code()

    @hybrid_property
    def code(self):
        return self._code

    @code.setter
    def code(self, code: str):
      self._code = code


# Студент --------------------------------------------------------------------------


# Учитель --------------------------------------------------------------------------
class TeacherClass(Base):
    __tablename__ = "teacher"

    id: Mapped[intpk]
    name: Mapped[str_32]
    surname: Mapped[str_32]
    patronymic: Mapped[str_32]
    tg_id: Mapped[str] = mapped_column(String(10), default="")
    _code: Mapped[str] = mapped_column(String(8))

    @hybrid_property
    def code(self):
        return self._code

    @code.setter
    def code(self, code: str):
      self._code = code

    async def generate_and_set_code(self):
        if not self._code:
            self._code = await generate_random_code()
# Учитель --------------------------------------------------------------------------

# Группа --------------------------------------------------------------------------
class GroupClass(Base):
    __tablename__ = "kgroup"

    id: Mapped[intpk]
    year: Mapped[str_256]
    level: Mapped[level]
    kvant: Mapped[kvant]
    group_num: Mapped[int]
    topics: Mapped[str_256]

    marks: Mapped[list["MarkClass"]] = relationship(back_populates="group")
# Группа --------------------------------------------------------------------------


# Оценки --------------------------------------------------------------------------
class MarkClass(Base):
    __tablename__ = "mark"

    id: Mapped[intpk]
    id_student: Mapped[int] = mapped_column(ForeignKey("student.id", ondelete="CASCADE"))
    id_group: Mapped[int] = mapped_column(ForeignKey("kgroup.id"))
    points: Mapped[int]
    marks: Mapped[str_256]
    achivment: Mapped[str_256]
    
    student: Mapped["StudentClass"] = relationship(back_populates="marks") 
    group: Mapped["GroupClass"] = relationship(back_populates="marks")
# Оценки --------------------------------------------------------------------------


# Админ --------------------------------------------------------------------------
class AdminClass(Base):
    __tablename__ = "admin"

    id: Mapped[intpk]
    name: Mapped[str_32]
    surname: Mapped[str_32]
    patronymic: Mapped[str_32]
    tg_id: Mapped[str] = mapped_column(String(10), default="")
    _code: Mapped[str] = mapped_column(String(8))

    @hybrid_property
    def code(self):
        return self._code

    @code.setter
    def code(self, code: str):
      self._code = code

    async def generate_and_set_code(self):
        if not self._code:
            self._code = await generate_random_code()
# Админ --------------------------------------------------------------------------