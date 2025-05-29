from sqlalchemy import select

from DataBase.Settings.configuration_DB import session_factory
from DataBase.Settings.models import TeacherClass, StudentClass

file_name = "auth_service"

# === РЕГИСТРАЦИЯ УЧИТЕЛЯ ===
async def reg_teacher(tg_id: str = "", code: str = ""):
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(TeacherClass).where(
                    TeacherClass.tg_id == tg_id
                    ))
            teacher = stmt.scalars().first()
            if teacher:
                return {"status": False, 
                        "ERROR": False, 
                        "info": "Учитель с таким tg_id уже существует"
                }

            stmt = await session.execute(select(TeacherClass).where(
                    TeacherClass._code == code
                    ))
            teacher = stmt.scalars().first()

            if not teacher:
                return {"status": False, 
                        "ERROR": False, 
                        "info": "Учитель с таким кодом не найден"}
            
            if teacher.tg_id:
                return {"status": False, 
                        "ERROR": False, 
                        "info": "Учитель с таким кодом уже зарегестрирован на другом устройстве"}


            teacher.tg_id = tg_id
            await session.commit()

            return {
                "status": True, 
                "ERROR": False,
                "info": "Учитель зарегистрирован",
                "id": teacher.id,
                "name": teacher.name,
                "surname": teacher.surname,
                "patronymic": teacher.patronymic,
                "tg_id": teacher.tg_id,
            }
            
        except Exception as e:
            await session.rollback()
            return {"status": False, 
                    "ERROR": True, 
                    "info": f"Ошибка при регистрации учителя по tg_id в файле {file_name}: {e}"
            }
        finally:
            await session.close()

# === АУТЕНТИФИКАЦИЯ УЧИТЕЛЯ ===
async def log_teacher(tg_id: str = ""):
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(TeacherClass).where(
                    TeacherClass.tg_id == tg_id
                    ))
            teacher = stmt.scalars().first()

            if teacher is None:
                return {"status": False, 
                        "ERROR": False, 
                        "info": f"Учитель с таким tg_id не найден"
                }
            return {
                "status": True, 
                "ERROR": False,
                "info": "Учитель аутентифицирован", 
                "id": teacher.id,
                "name": teacher.name,
                "surname": teacher.surname,
                "patronymic": teacher.patronymic,
                "tg_id": teacher.tg_id,
            }
        except Exception as e:
            return {"status": False, 
                    "ERROR": True, 
                    "info": f"Ошибка при аутентификации учителя по tg_id в файле {file_name}: {e}"
                }
        finally:
            await session.close()

# === УДАЛЕНИЕ tg_id УЧИТЕЛЯ ===
async def logout_teacher(tg_id: str = ""):
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(TeacherClass).where(
                    TeacherClass.tg_id == tg_id
                    ))
            teacher = stmt.scalars().first()
            if not teacher:
                return {
                    "status": False, 
                    "ERROR": False, 
                    "info": "Учитель не найден"}

            teacher.tg_id = ""

            await session.commit()

            return {
                "status": True, 
                "ERROR": False,
                "info": "tg_id учителя удален"
            }

        except Exception as e:
            await session.rollback()
            return {
                "status": False, 
                "ERROR": True, 
                "info": f"Ошибка при удалении tg_id учителя в файле {file_name}: {e}"
            }
        
        finally:
            await session.close()

# === РЕГИСТРАЦИЯ СТУДЕНТА ===
async def reg_student(tg_id: str = "", code: str = ""):
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(StudentClass).where(
                    StudentClass.tg_id == tg_id
                    ))
            student = stmt.scalars().first()

            if student:
                return {
                    "status": False, 
                    "ERROR": False, 
                    "info": "Студент с таким tg id_id уже существует"
                }


            stmt = await session.execute(select(StudentClass).where(
                    StudentClass._code == code
                    ))
            student = stmt.scalars().first()

            if not student:
                return {
                    "status": False, 
                    "ERROR": False, 
                    "info": "Студент с таким кодом не найден"
                }
            
            if student.tg_id == "":

                student.tg_id = tg_id
                await session.commit()

                return {
                    "status": True, 
                    "ERROR": False,
                    "info": "Студент зарегистрирован по tg_id", 
                    "student_id": student.id,
                    "name": student.name,
                    "surname": student.surname,
                    "patronymic": student.patronymic
                }
            else: 
                return {
                    "status": False, 
                    "ERROR": False,
                    "info": "Студент c таким кодом зарегестрирован на другом устройсвте",
                }

        except Exception as e:
            await session.rollback()
            return {
                "status": False, 
                "ERROR": True, 
                "info": f"Ошибка при регистрации по tg_id в файле {file_name}: {e}"
            }
        finally:
            await session.close()

# === АУТЕНТИФИКАЦИЯ СТУДЕНТА ===
async def log_student(tg_id: str = ""):
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(StudentClass).where(
                    StudentClass.tg_id == tg_id
                    ))
            student = stmt.scalars().first()

            if student is None:
                return {"status": False, 
                        "ERROR": False, 
                        "info": f"Студент с таким tg_id не найден"
                }
            return {
                "status": True, 
                "ERROR": False,
                "info": "Студент аутентифицирован", 
                "id": student.id,
                "name": student.name,
                "surname": student.surname,
                "patronymic": student.patronymic,
                "tg_id": student.tg_id,
            }
        except Exception as e:
            return {"status": False, 
                    "ERROR": True, 
                    "info": f"Ошибка при аутентификации студента по tg_id в файле {file_name}: {e}"
                }
        finally:
            await session.close()

# === УДАЛЕНИЕ tg_id СТУДЕНТА ===
async def logout_student(tg_id: str = ""):
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(StudentClass).where(
                    StudentClass.tg_id == tg_id
                    ))
            student = stmt.scalars().first()
            if not student:
                return {
                    "status": False, 
                    "ERROR": False, 
                    "info": "Учитель не найден"}

            student.tg_id = ""

            await session.commit()

            return {
                "status": True, 
                "ERROR": False,
                "info": "tg_id студента удален"
            }

        except Exception as e:
            await session.rollback()
            return {
                "status": False, 
                "ERROR": True, 
                "info": f"Ошибка при удалении tg_id студента в файле {file_name}: {e}"
            }
        
        finally:
            await session.close()