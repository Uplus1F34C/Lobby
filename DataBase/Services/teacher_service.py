from sqlalchemy import select

from DataBase.Settings.configuration_DB import session_factory
from DataBase.Settings.models import TeacherClass

file_name = "teacher_service"

# === ДОБАВЛЕНИЕ УЧИТЕЛЯ ===
async def add_teacher(name: str = "", surname: str = "", patronymic: str = "", tg_id: str = ""):
    async with session_factory() as session:
        try:
            teacher = TeacherClass(
                name=name,
                surname=surname,
                patronymic=patronymic,
                tg_id=tg_id,
                _code=""
            )

            session.add(teacher)
            await teacher.generate_and_set_code()  # Генерируем код перед коммитом
            await session.commit()
            await session.refresh(teacher)  # Обновляем объект из БД

            return {
                "status": True, 
                "ERROR": False, 
                "info": f"Учитель добавлен в бд", 
                "id": teacher.id,
                "name": teacher.name,
                "surname": teacher.surname,
                "patronymic": teacher.patronymic,
                "Tg_id": teacher.tg_id,
                "code": teacher.code
            }
        except Exception as e:
            await  session.rollback()
            return {"status": False, 
                    "ERROR": True, 
                    "info": f"Ошибка при добавлении учителя в файле {file_name}: {e}"
            }
        finally:
            await session.close()

# === УДАЛЕНИЕ УЧИТЕЛЯ ===
async def del_teacher(tg_id: str = "", name: str = "", surname: str = "", patronymic: str = "",):
    async with session_factory() as session:
        try:
            if tg_id:
                teacher = await session.get(TeacherClass, tg_id)
            elif name and surname:
                stmt = await session.execute(select(TeacherClass).where(
                    TeacherClass.name == name,
                    TeacherClass.surname == surname,
                    TeacherClass.patronymic == patronymic,
                    ))
                teacher = stmt.scalars().first()

            if not teacher:
                return {"status": False, 
                        "ERROR": False,
                        "info": f"Учитель с такими данными не найден"
                }

            await session.delete(teacher)
            await session.commit()

            return {"status": True, 
                    "ERROR": False, 
                    "info": "Учитель удален"
            }

        except Exception as e:
            await session.rollback()
            return {"status": False, 
                    "ERROR": True,
                    "info": f"Ошибка при удалении учителя в файле {file_name}: {e}"
            }
        finally:
            await session.close()