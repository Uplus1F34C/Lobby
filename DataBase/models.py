from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from typing import Annotated
from enum import Enum
import secrets, string, bcrypt

from settings.database import Base, str_256, str_32, session_factory


# Помощь --------------------------------------------------------------------------
def generate_random_code(length: int = 8, max_attempts: int = 100) -> str: #Генерация кода
        with session_factory() as session:
            alphabet = string.ascii_uppercase + string.digits 
            for _ in range(max_attempts):
                code = ''.join(secrets.choice(alphabet) for _ in range(length))
                if not session.query(StudentClass).filter_by(_code=code).first():  # Проверяем наличие кода в БД
                    print(f"УИ код успешно сгенерирован")
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
    name: Mapped[str_32] = mapped_column()
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

    @hybrid_property
    def code(self):
        return self._code

    @code.setter
    def code(self, code: str):
      self._code = code

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self._code:
            self._code = generate_random_code()
# Студент --------------------------------------------------------------------------


# Группа --------------------------------------------------------------------------
class GroupClass(Base):
    __tablename__ = "kgroup"

    id: Mapped[intpk]
    year: Mapped[str_256]
    level: Mapped[level]
    kvant: Mapped[kvant]
    group_num: Mapped[int]
    topics: Mapped[str_256]
# Группа --------------------------------------------------------------------------


# Оценка --------------------------------------------------------------------------
class MarkClass(Base):
    __tablename__ = "mark"

    id: Mapped[intpk]
    id_student: Mapped[int] = mapped_column(ForeignKey("student.id", ondelete="CASCADE"))
    id_group: Mapped[int] = mapped_column(ForeignKey("kgroup.id"))
    points: Mapped[int]
    marks: Mapped[str_256]
    achivment: Mapped[str_256]
    
    student: Mapped["StudentClass"] = relationship(back_populates="marks") 
# Оценка --------------------------------------------------------------------------