import shutil, os

from sqlalchemy import select

from DataBase.Settings.configuration_DB import session_factory
from DataBase.Settings.models import GroupClass, StudentClass, MarkClass, level, kvant

file_name = "student_service"

# === ДОБАВЛЕНИЕ СТУДЕНТА ===
async def add_student(name: str = "", surname: str = "", patronymic: str = "",
                      level: level = "", kvant: kvant = "", group_num: int = 0, 
                      tg_id: str = ""):
    async with session_factory() as session:
        try:
            # Поиск группы
            stmt = await session.execute(select(GroupClass).where(
                    GroupClass.level == level,
                    GroupClass.kvant == kvant,
                    GroupClass.group_num == group_num,
            ))
            group = stmt.scalars().first()
            
            if not group:
                return {
                    "status": False, 
                    "ERROR": False, 
                    "info": f"Группа {level}-{kvant}-{group_num} не найдена"
                }

            # Создание студента
            student = StudentClass(
                name=name,
                surname=surname,
                patronymic=patronymic,
                tg_id=tg_id,
                code=""
            )

            session.add(student)
            await student.generate_and_set_code()
            await session.commit()
            await session.refresh(student)

            # Создание файла с оценками
            marks_file_path = os.path.join("DataBase\Data\MARKS", f"{student.id}.json")
            shutil.copy(group.topics, marks_file_path)

            # Создание файла с достижениями
            achivment_file_path = os.path.join("DataBase\Data\ACHIEVEMENTS", f"{student.id}.json")
            shutil.copy("DataBase\Data\EXAMPLE_ACHIEVEMENT.json", achivment_file_path)

            # Создание записи об оценках
            mark = MarkClass(
                id_student=student.id, 
                id_group=group.id,
                points=0,
                marks=marks_file_path,
                achivment=achivment_file_path
            )
            session.add(mark)
            await session.commit()

            return {
                "status": True, 
                "ERROR": False,
                "info": f"Студент добавлен в базу данных", 
                "id": student.id,
                "name": student.name,
                "surname": student.surname,
                "patronymic": student.patronymic,
                "group": f"{level}-{kvant}-{group_num}",
                "tg_id": tg_id,
                "code": student._code
            }
            
        except Exception as e:
            await session.rollback()
            return {
                "status": False, 
                "ERROR": True, 
                "info": f"Ошибка при добавлении студента в файле {file_name}: {e}"
            }
        
        finally:
            await session.close()

# === ПОЛУЧЕНИЕ КОДА СТУДЕНТА ===
async def get_student_code(tg_id: str = "", name: str = "", surname: str = "", patronymic: str = ""):
    async with session_factory() as session:
        try:
            if tg_id:
                stmt = await session.execute(select(StudentClass).where(
                    StudentClass.tg_id == tg_id
                    ))
            elif name and surname:
                stmt = await session.execute(select(StudentClass).where(
                        StudentClass.name == name,
                        StudentClass.surname == surname,
                        StudentClass.patronymic == patronymic,
                        ))
            Student = stmt.scalars().first()
            
            if not Student:
                return {
                    "status": False, 
                    "ERROR": False, 
                    "info": "Студент не найден"
                    }

            return {
                "status": True, 
                "ERROR": False,
                "info": "Код студента получен", 
                "code": Student._code
            }

        except Exception as e:
            return {
                "status": False, 
                "ERROR": True, 
                "info": f"Ошибка при получении кода студента: {e}"
            }
        finally:
            await session.close()

# === ПОЛУЧЕНИЕ ИНФОРМАЦИИ О СТУДЕНТЕ ===
async def get_student_info(tg_id: str = "", name: str = "", surname: str = "", patronymic: str = ""):
    async with session_factory() as session:
        try:
            # Find student
            if tg_id:
                stmt = await session.execute(select(StudentClass).where(
                    StudentClass.tg_id == tg_id
                    ))
            elif name and surname:
                stmt = await session.execute(select(StudentClass).where(
                    StudentClass.name == name,
                    StudentClass.surname == surname,
                    StudentClass.patronymic == patronymic,
                ))
            student = stmt.scalars().first()
            
            if not student:
                return {
                    "status": False, 
                    "ERROR": False, 
                    "info": "Студент не найден"
                }

            # Get student's marks and group info
            stmt = await session.execute(
                select(MarkClass, GroupClass)
                .join(GroupClass, MarkClass.id_group == GroupClass.id)
                .where(MarkClass.id_student == student.id)
            )
            result = stmt.first()
            
            if not result:
                return {
                    "status": False,
                    "ERROR": False,
                    "info": "Информация о группе студента не найдена"
                }
            
            mark, group = result

            return {
                "status": True, 
                "ERROR": False,
                "info": "Информация о студенте получена", 
                "id": student.id,
                "name": student.name,
                "surname": student.surname,
                "patronymic": student.patronymic,
                "group": f"{group.level.value}-{group.kvant.value}-{group.group_num}",
                "points": mark.points,
                "tg_id": student.tg_id,
                "code": student.code
            }

        except Exception as e:
            return {
                "status": False, 
                "ERROR": True, 
                "info": f"Ошибка при получении информации о студенте: {e}"
            }
        finally:
            await session.close()

# === УДАЛЕНИЕ СТУДЕНТА ===
async def del_student(tg_id: str = "", name: str = "", surname: str = "", patronymic: str = ""):
    async with session_factory() as session:
        try:
            # Удаление связанных файлов и записей
            if tg_id:
                Student = await session.get(StudentClass, tg_id)
            elif name and surname:
                stmt = await session.execute(select(StudentClass).where(
                        StudentClass.name == name,
                        StudentClass.surname == surname,
                        StudentClass.patronymic == patronymic,
                        ))
                Student = stmt.scalars().first()
    
            if not Student:
                return {"status": False, 
                        "ERROR": False, 
                        "info": f"Студент с таким id не найден"
                }
            
            stmt = await session.execute(select(MarkClass).where(
                    MarkClass.id_student == Student.id
                    ))
            marks = stmt.scalars().all()
            for mark in marks:
                if os.path.isfile(mark.achivment):
                    os.unlink(mark.achivment)
                if os.path.isfile(mark.marks):
                    os.unlink(mark.marks)
                await session.delete(mark)


            await session.delete(Student)
            await session.commit()

            return {"status": True, 
                    "ERROR": False, 
                    "info": "Студент удален"
            }

        except Exception as e:
            await session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при удалении студента в файле {file_name}: {e}"
            }
        finally:
            await session.close()

