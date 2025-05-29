from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from enum import Enum
import secrets, string

from DataBase.Settings.configuration_DB import Base, str_256, str_32, session_factory, intpk

# ==== ПОМОЩЬ ====
class level(Enum):
    С = "С"
    Б = "Б"
    У = "У"
    П = "П"
class kvant(Enum):
    IT = "IT"
    Пром_дизайн = "Пром_дизайн"
    Медиа = "Медиа"
    Хай_тек = "Хай_тек"
    Космо = "Космо"
    Гео = "Гео"
    VR_AR = "VR_AR"
    Пром_робо = "Пром_робо"

async def generate_random_code(length: int = 8, max_attempts: int = 100) -> str:
    async with session_factory() as session:
        alphabet = string.ascii_uppercase + string.digits 
        for _ in range(max_attempts):
            code = ''.join(secrets.choice(alphabet) for _ in range(length))
            # real_teacher_code = await session.execute(
            #     select(TeacherClass).where(TeacherClass._code == code)
            # )
            # real_student_code = await session.execute(
            #     select(StudentClass).where(StudentClass._code == code)
            # )
            # print(real_student_code.scalars().first())
            # if not real_student_code.scalars().first() and real_teacher_code.scalars().first():
            return code
        raise ValueError(f"Не удалось сгенерировать уникальный код после {max_attempts} попыток.")

# ==== СТУДЕНТ ====
class StudentClass(Base):
    __tablename__ = "student"

    id: Mapped[intpk]
    name: Mapped[str_32]
    surname: Mapped[str_32]
    patronymic: Mapped[str_32]
    tg_id: Mapped[str] = mapped_column(String(10), default="")
    _code: Mapped[str] = mapped_column(String(8))

    marks: Mapped["MarkClass"] = relationship(back_populates="student")
        
    async def generate_and_set_code(self):
        if not self._code:
            self._code = await generate_random_code()

    @hybrid_property
    def code(self):
        return self._code

    @code.setter
    def code(self, code: str):
      self._code = code

    

# ==== УЧИТЕЛЬ ====
class TeacherClass(Base):
    __tablename__ = "teacher"

    id: Mapped[intpk]
    name: Mapped[str_32]
    surname: Mapped[str_32]
    patronymic: Mapped[str_32]
    tg_id: Mapped[str] = mapped_column(String(10), default="")
    _code: Mapped[str] = mapped_column(String(8))

    async def generate_and_set_code(self):
        if not self._code:
            self._code = await generate_random_code()

    @hybrid_property
    def code(self):
        return self._code

    @code.setter
    def code(self, code: str):
      self._code = code


# ==== ГРУППА ====
class GroupClass(Base):
    __tablename__ = "_group"

    id: Mapped[intpk]
    year: Mapped[str_256]
    level: Mapped[level]
    kvant: Mapped[kvant]
    group_num: Mapped[int]
    topics: Mapped[str_256]

    marks: Mapped[list["MarkClass"]] = relationship(back_populates="group")

# ==== ОЦЕНКИ ====
class MarkClass(Base):
    __tablename__ = "mark"

    id: Mapped[intpk]
    id_student: Mapped[int] = mapped_column(ForeignKey("student.id", ondelete="CASCADE"))
    id_group: Mapped[int] = mapped_column(ForeignKey("_group.id"))
    points: Mapped[int]
    marks: Mapped[str_256]
    achivment: Mapped[str_256]
    
    student: Mapped["StudentClass"] = relationship(back_populates="marks") 
    group: Mapped["GroupClass"] = relationship(back_populates="marks")