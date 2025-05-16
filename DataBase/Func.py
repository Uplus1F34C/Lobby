import shutil, json, os, sys, aiofiles

from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload

from DataBase.settings.configuration_DB import Base, session_factory, engine
from DataBase.settings.models import GroupClass, StudentClass, TeacherClass, MarkClass, level, kvant

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =================================================================================
# БАЗОВЫЕ ФУНКЦИИ
# =================================================================================

async def reset_base():
    """
    Полный сброс базы данных
    """
    try:
        # Удаление всех таблиц
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        
         # Очистка файлов (синхронный код)
        marks_dir = "DataBase\\DATA\\MARKS"
        achivment_dir = "DataBase\\DATA\\ACHIVMENT"
        
        for directory in [marks_dir, achivment_dir]:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)

        return {"status": True, 
                "error": False, 
                "info": "База данных сброшена"
        }
    
    except Exception as e: 
        return {"status": False, 
                "error": True, 
                "info": f"Ошибка при сбросе базы данных: {e}"
        }

async def insert_group():
    """
    Добавление групп в базу данных
    """
    async  with session_factory() as session:
        try:
            for k in kvant:
                for l in level:
                    for g in range(1, 5):
                        group = GroupClass(
                            year="25/26",
                            level=l,
                            kvant=k,
                            group_num=g,
                            topics=f"DataBase/DATA/TOPICS/{k.name}/{l.name}.json",
                        )
                        session.add(group)
                        
            await session.commit()
            return {"status": True, 
                    "error": False, 
                    "info": "Группы добавлены"
            }

        except Exception as e:
            await  session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при добавлении групп: {e}"
            }

# =================================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С УЧИТЕЛЯМИ
# =================================================================================

async def insert_teacher(name: str, surname: str, patronymic: str, tg_id = ""):
    """
    Добавление нового учителя в базу данных
    """
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
                "error": False,
                "info": f"Учитель добавлен в базу данных", 
                "id": teacher.id,
                "name": teacher.name,
                "surname": teacher.surname,
                "patronymic": teacher.patronymic,
                "Tg_id": teacher.tg_id,
                "code": teacher.code  # Возвращаем сгенерированный код
            }
        except Exception as e:
            await  session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при добавлении учителя: {e}"
            }
        finally:
            # Явно закрываем сессию
            await session.close()

async def delete_teacher(teacher_id = "", name: str = "", surname: str = "", patronymic: str = "",):
    """
    Удаление учителя по ID
    """
    async with session_factory() as session:
        try:
            if teacher_id:
                teacher = await session.get(TeacherClass, teacher_id)
            elif name and surname:
                stmt = await session.execute(select(TeacherClass).where(
                    TeacherClass.name == name,
                    TeacherClass.surname == surname,
                    TeacherClass.patronymic == patronymic,
                    ))
                teacher = stmt.scalars().first()

            if not teacher:
                return {"status": False, 
                        "error": False, 
                        "info": f"Учитель с такими данными не найден"
                }

            await session.delete(teacher)
            await session.commit()

            return {"status": True, 
                    "error": False, 
                    "info": "Учитель удален"
            }

        except Exception as e:
            await session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при удалении учителя: {e}"
            }
        finally:
            await session.close()

async def log_teacher(teacher_tg_id):
    """
    Аутентификация учителя по Telegram ID
    """
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(TeacherClass).where(
                    TeacherClass.tg_id == teacher_tg_id
                    ))
            teacher = stmt.scalars().first()

            if teacher is None:
                return {"status": False, 
                        "error": False, 
                        "info": f"Учитель с таким tg id не найден"
                }
            return {
                "status": True, 
                "error": False,
                "info": "Учитель аутентифицирован", 
                "id": teacher.id,
                "name": teacher.name,
                "surname": teacher.surname,
                "patronymic": teacher.patronymic
            }
        except Exception as e:
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при аутентификации учителя по tg id: {e}"
                }
        finally:
            await session.close()

async def reg_teacher(teacher_tg_id: int, code: str):
    """
    Регистрация учителя по коду и Telegram ID
    """
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(TeacherClass).where(
                    TeacherClass.tg_id == teacher_tg_id
                    ))
            teacher = stmt.scalars().first()
            if teacher:
                return {"status": False, 
                        "error": False, 
                        "info": "Учитель с таким Tg id уже существует"
                }

            stmt = await session.execute(select(TeacherClass).where(
                    TeacherClass._code == code
                    ))
            teacher = stmt.scalars().first()

            if not teacher:
                return {"status": False, 
                        "error": False, 
                        "info": "Учитель с таким кодом не найден"}
            
            if teacher.tg_id:
                return {"status": False, 
                        "error": False, 
                        "info": "Учитель с таким кодом уже зарегестрирован на другом устройстве"}


            teacher.tg_id = teacher_tg_id
            await session.commit()

            return {
                "status": True, 
                "error": False,
                "info": "Учитель зарегистрирован",
                "id": teacher.id,
                "name": teacher.name,
                "surname": teacher.surname,
                "patronymic": teacher.patronymic
            }
            
        except Exception as e:
            await session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при регистрации учителя по TG: {e}"
            }
        finally:
            await session.close()

async def del_teachers_id(teacher_tg_id: int):
    """
    Удаление Telegram ID у учителя
    """
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(TeacherClass).where(
                    TeacherClass.tg_id == teacher_tg_id
                    ))
            teacher = stmt.scalars().first()
            if not teacher:
                return {"status": False, "error": False, "info": "Учитель не найден"}

            teacher.tg_id = ""
            await session.commit()

            return {
                "status": True, 
                "error": False,
                "info": "Tg id учителя удален"
            }

        except Exception as e:
            await session.rollback()
            return {"status": False, "error": True, "info": f"Ошибка при удалении Tg id учителя: {e}"}
        finally:
            await session.close()

# =================================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ СО СТУДЕНТАМИ
# =================================================================================

async def insert_student(name: str, surname: str, patronymic: str, level: level, 
                 kvant: kvant, group_num: str, tg_id: str = ""):
    """
    Добавление нового студента в базу данных
    """
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
                return {"status": False, "error": False, "info": f"Группа {level}-{kvant}-{group_num} не найдена"}

            # Создание студента
            student = StudentClass(
                name=name,
                surname=surname,
                patronymic=patronymic,
                login="",
                password="",
                tg_id=tg_id,
                code=""
            )

            session.add(student)
            await student.generate_and_set_code()
            await session.commit()
            await session.refresh(student)

            # Создание файла с оценками
            marks_file_path = os.path.join("DataBase/DATA/MARKS", f"{student.id}.json")
            shutil.copy(group.topics, marks_file_path)

            # Создание файла с достижениями
            achivment_file_path = os.path.join("DataBase/DATA/ACHIVMENT", f"{student.id}.json")
            shutil.copy("DataBase/DATA/EXEMPLE_ACHIVMENT.json", achivment_file_path)

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
                "error": False,
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
            return {"status": False, "error": True, "info": f"Ошибка при добавлении студента: {e}"}
        
        finally:
            await session.close()

async def delete_student(student_id = "", name: str = "", surname: str = "", patronymic: str = ""):
    """
    Удаление студента
    """
    async with session_factory() as session:
        try:
            # Удаление связанных файлов и записей
            if student_id:
                Student = await session.get(StudentClass, student_id)
            elif name and surname:
                stmt = await session.execute(select(StudentClass).where(
                        StudentClass.name == name,
                        StudentClass.surname == surname,
                        StudentClass.patronymic == patronymic,
                        ))
                Student = stmt.scalars().first()
    
            if not Student:
                return {"status": False, 
                        "error": False, 
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
                    "error": False, 
                    "info": "Студент удален"
            }

        except Exception as e:
            await session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при удалении студента: {e}"
            }
        finally:
            await session.close()

# def reg_student_login(code: str, login: str, password: str):
#     """
#     Регистрация студента по коду с использованием логина и пароля
#     """
#     with session_factory() as session:
#         try:
#             if session.query(StudentClass).filter_by(login=login).first():
#                 return {"status": False, 
#                         "error": False, 
#                         "info": "Студент с таким логином уже существует"
#                 }

#             student = session.query(StudentClass).filter(StudentClass._code == code).first()
#             if not student:
#                 return {"status": False, 
#                         "error": False, 
#                         "info": "Студент с таким кодом не найден"
#                 }

#             student.login = login
#             student.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#             session.commit()

#             return {
#                 "status": True, 
#                 "error": False,
#                 "info": "Студент зарегистрирован", 
#                 "student_id": student.id
#             }

#         except Exception as e:
#             session.rollback()
#             return {"status": False, 
#                     "error": True, 
#                     "info": f"Ошибка при регистрации: {e}"
#             }

async def reg_student(code: str, student_tg_id: int):
    """
    Регистрация студента по коду с использованием Telegram ID
    """
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(StudentClass).where(
                    StudentClass.tg_id == student_tg_id
                    ))
            student = stmt.scalars().first()

            if student:
                return {"status": False, 
                        "error": False, 
                        "info": "Студент с таким tg id уже существует"
                }

            stmt = await session.execute(select(StudentClass).where(
                    StudentClass._code == code
                    ))
            student = stmt.scalars().first()
            if not student:
                return {"status": False, 
                        "error": False, 
                        "info": "Студент с таким кодом не найден"
                }
            
            if student.tg_id == "":

                student.tg_id = student_tg_id
                await session.commit()

                return {
                    "status": True, 
                    "error": False,
                    "info": "Студент зарегистрирован по tg", 
                    "student_id": student.id,
                    "name": student.name,
                    "surname": student.surname,
                    "patronymic": student.patronymic
                }
            else: 
                return {
                    "status": False, 
                    "error": False,
                    "info": "Студент c таким кодом зарегестрирован на другом устройсвте",
                }

        except Exception as e:
            await session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при регистрации по tg: {e}"
            }
        finally:
            await session.close()

# def log_student_login(login: str, password: str):
#     """
#     Аутентификация студента по логину и паролю
#     """
#     with session_factory() as session:
#         try:
#             student = session.query(StudentClass).filter(StudentClass.login == login).first()
#             if student is None:
#                 return {"status": False, 
#                         "error": False, 
#                         "info": "Студент с таким логином не найден"
#                 }
            
#             if not student.password:
#                 return {"status": False, 
#                         "error": False, 
#                         "info": "У студента не установлен пароль"
#                 }
            
#             if bcrypt.checkpw(password.encode('utf-8'), student.password.encode('utf-8')):
#                 return {
#                     "status": True, 
#                     "error": False,
#                     "info": "Аутентификация успешна", 
#                     "student_id": student.id
#                 }
#             else:
#                 return {"status": False, 
#                         "error": False, 
#                         "info": "Неверный пароль"
#                 }

#         except Exception as e:
#             return {"status": False, 
#                     "error": True, 
#                     "info": f"Ошибка при аутентификации: {e}"
#             }

async def log_student(student_tg_id: int):
    """
    Аутентификация студента по Telegram ID
    """
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(StudentClass).where(
                    StudentClass.tg_id == student_tg_id
                    ))
            student = stmt.scalars().first()
            if student is None:
                return {"status": False, 
                        "error": False, 
                        "info": "Студент не найден"

                }
            
            return {
                "status": True, 
                "error": False,
                "info": "Успешная аутентификация", 
                "id": student.id,
                "name": student.name,
                "surname": student.surname,
                "patronymic": student.patronymic
            }
        
        except Exception as e:
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при аутентификации: {e}"
            }
        finally:
            await session.close()

# def get_student_info(student_id: int):
#     """
#     Получение ФИО студента по ID
#     """
#     with session_factory() as session:
#         try:
#             student = session.query(StudentClass).filter(StudentClass.id == student_id).first()
#             if not student:
#                 return {"status": False, 
#                         "error": False, 
#                         "info": "Студент не найден"
#                 }

#             return {
#                 "status": True, 
#                 "error": False,
#                 "info": "Данные студента получены",
#                 "name": student.name, 
#                 "surname": student.surname, 
#                 "patronymic": student.patronymic
#             }

#         except Exception as e:
#             return {"status": False, 
#                     "error": True, 
#                     "info": f"Ошибка при получении ФИО студента: {e}"
#             }
  
async def get_student_code(name: str, surname: str, patronymic: str):
    """
    Получение кода студента по ФИО
    """
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(StudentClass).where(
                    StudentClass.name == name, 
                    StudentClass.surname == surname, 
                    StudentClass.patronymic == patronymic
                    ))
            student = stmt.scalars().first()
            
            if not student:
                return {"status": False, "error": False, "info": "Студент не найден", "code": ""}

            return {
                "status": True, 
                "error": False,
                "info": "Код студента получен", 
                "code": student._code
            }

        except Exception as e:
            return {"status": False, "error": True, "info": f"Ошибка при получении кода студента: {e}"}
        finally:
            await session.close()

async def del_students_id(student_tg_id: int):
    """
    Удаление Telegram ID у студента
    """
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(StudentClass).where(
                    StudentClass.tg_id == student_tg_id
                    ))
            student = stmt.scalars().first()
            if not student:
                return {"status": False, "error": False, "info": "Студент не найден"}

            student.tg_id = ""
            await session.commit()

            return {
                "status": True, 
                "error": False,
                "info": "Tg id студента удален", 
                "student_id": student.id
            }

        except Exception as e:
            await session.rollback()
            return {"status": False, "error": True, "info": f"Ошибка при удалении Tg id студента: {e}"}
        finally:
            await session.close()

# =================================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ОЦЕНКАМИ И РЕЙТИНГАМИ
# =================================================================================

async def count_points():
    """
    Пересчет баллов для всех студентов на основе оценок и достижений
    """
    async with session_factory() as session:
        try:
            stmt = await session.execute(select(MarkClass))
            marks = stmt.scalars().all()
            for mark in marks:
                points = 0

                # Обработка оценок из файла
                with open(mark.marks, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                for branch in data.values():
                    for topic in branch["topics"].values():
                        topic_mark = topic["mark"]
                        if topic_mark != 0:
                            if topic_mark < 4:
                                points +=  topic_mark*topic["X"]
                            else:
                                return {
                                    "status": False, 
                                    "error": False,
                                    "info": f'Некорректная оценка {topic_mark} в файле {mark.marks}'
                                }

                # Обработка достижений
                with open(mark.achivment, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                for achivment in data.values():
                    if achivment["status"]:
                        points += achivment["point"]

                mark.points = points
                await session.commit()
                
            return {"status": True, "error": False, "info": "Баллы успешно пересчитаны"}

        except Exception as e:
            await session.rollback()
            return {"status": False, "error": True, "info": f"Ошибка при пересчете баллов: {e}"}
        finally:
            await session.close()

async def get_achivments(student_tg_id: int):
    """
    Асинхронное получение списка достижений студента
    """
    async with session_factory() as session:
        try:
            # Асинхронный запрос к БД
            stmt = select(StudentClass.id).where(StudentClass.tg_id == student_tg_id)
            result = await session.execute(stmt)
            student_id = result.scalar()

            if not student_id:
                return {"status": False, "error": False, "info": "Студент не найден"}

            stmt = select(MarkClass.achivment).where(MarkClass.id_student == student_id)
            result = await session.execute(stmt)
            achivments = result.scalars().first()
            
            if not achivments:
                return {
                    "status": True, 
                    "error": False, 
                    "info": "Достижения не найдены"
                }

            # Асинхронное чтение файла
            async with aiofiles.open(achivments, 'r', encoding='utf-8') as file:
                content = await file.read()
                data = json.loads(content)
                
            return {
                "status": True, 
                "error": False,
                "info": "Достижения получены",
                "achivments": data
            }

        except FileNotFoundError:
            return {
                "status": False, 
                "error": False,
                "info": "Файл с достижениями не найден"
            }
        except json.JSONDecodeError:
            return {
                "status": False,
                "error": True,
                "info": "Ошибка формата файла достижений"
            }
        except Exception as e:
            return {
                "status": False, 
                "error": True, 
                "info": f"Ошибка при получении достижений: {str(e)}"
            }

async def get_marks(student_tg_id: int):
    """
    Асинхронное получение оценок студента
    """
    async with session_factory() as session:
        try:
            # Асинхронный запрос к БД
            stmt = select(StudentClass.id).where(StudentClass.tg_id == student_tg_id)
            result = await session.execute(stmt)
            student_id = result.scalar()

            if not student_id:
                return {"status": False, "error": False, "info": "Студент не найден"}

            stmt = select(MarkClass.marks).where(MarkClass.id_student == student_id)
            result = await session.execute(stmt)
            marks = result.scalars().first()
            
            if not marks:
                return {
                    "status": True, 
                    "error": False, 
                    "info": "Оценки не найдены"
                }

            # Асинхронное чтение файла
            async with aiofiles.open(marks, 'r', encoding='utf-8') as file:
                content = await file.read()
                data = json.loads(content)
                
            return {
                "status": True, 
                "error": False,
                "info": "Оценки получены",
                "topics": data
            }

        except FileNotFoundError:
            return {
                "status": False, 
                "error": False,
                "info": "Файл с оценками не найден"
            }
        except json.JSONDecodeError:
            return {
                "status": False,
                "error": True,
                "info": "Ошибка формата файла оценок"
            }
        except Exception as e:
            return {
                "status": False, 
                "error": True, 
                "info": f"Ошибка при получении оценок: {str(e)}"
            }

async def get_group_rating(student_tg_id: int):
    """
    Получение рейтинга группы студента (асинхронная версия)
    """
    async with session_factory() as session:
        try:
            # 1. Находим студента и его группу
            stmt = (
                select(MarkClass)
                .join(MarkClass.student)
                .where(StudentClass.tg_id == student_tg_id)
                .options(joinedload(MarkClass.group))
            )
            result = await session.execute(stmt)
            student_mark = result.scalars().first()

            if not student_mark:
                return {"status": False, "error": False, "info": "Студент не найден"}
                
            if not student_mark.group:
                return {"status": False, "error": False, "info": "Группа не найдена"}

            group = student_mark.group

            # 2. Получаем всех студентов группы с их оценками
            stmt = (
                select(StudentClass, MarkClass.points)
                .join(StudentClass.marks)
                .join(MarkClass.group)
                .where(
                    GroupClass.id == group.id  # Проще фильтровать по id группы
                )
                .order_by(desc(MarkClass.points))
            )
            result = await session.execute(stmt)
            students_data = result.all()

            # 3. Формируем рейтинг
            rating = [
                {
                    "id": student.id,
                    "name": student.name,
                    "surname": student.surname,
                    "points": points
                }
                for student, points in students_data
            ]

            return {
                "status": True,
                "error": False,
                "info": "Рейтинг группы получен",
                "group_rating": rating
            }

        except Exception as e:
            return {
                "status": False,
                "error": True,
                "info": f"Ошибка: {str(e)}"
            }
        
async def get_kvant_rating(student_tg_id: int):
    """
    Асинхронное получение рейтинга по направлению (кванту)
    """
    async with session_factory() as session:
        try:
            # 1. Получаем информацию о студенте и его группе за один запрос
            
            stmt = (
                select(MarkClass)
                .join(MarkClass.student)
                .where(StudentClass.tg_id == student_tg_id)
                .options(joinedload(MarkClass.group)))
            
            result = await session.execute(stmt)
            student_mark = result.scalars().first()
            
            if not student_mark:
                return {"status": False, "error": False, "info": "Студент не найден"}
            
            if not student_mark.group:
                return {"status": False, "error": False, "info": "Группа не найдена"}
            
            group = student_mark.group

            # 2. Получаем топ студентов направления с их оценками и группами за один запрос
            stmt = (
                select(
                    StudentClass,
                    MarkClass.points,
                    GroupClass.level,
                    GroupClass.kvant,
                    GroupClass.group_num
                )
                .join(StudentClass.marks)
                .join(MarkClass.group)
                .where(
                    GroupClass.level == group.level,
                    GroupClass.kvant == group.kvant
                )
                .order_by(desc(MarkClass.points))
                .limit(4)
            )
            
            result = await session.execute(stmt)
            rows = result.all()
            
            # 3. Формируем рейтинг
            rating = [
                {
                    "student_id": student.id,
                    "name": student.name,
                    "surname": student.surname,
                    "group": f"{level.name}-{kvant.name}-{group_num}",
                    "points": points
                }
                for student, points, level, kvant, group_num in rows
            ]
            
            return {
                "status": True, 
                "error": False,
                "info": "Рейтинг направления получен",
                "kvant_rating": rating,
            }

        except Exception as e:
            return {
                "status": False, 
                "error": True, 
                "info": f"Ошибка при получении рейтинга направления: {str(e)}"
            }