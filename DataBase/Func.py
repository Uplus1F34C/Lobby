import json
import bcrypt
import shutil
import os
import sys
from DataBase.settings.configuration_DB import Base, session_factory, engine
from DataBase.settings.models import GroupClass, StudentClass, TeacherClass, MarkClass, level, kvant

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# =================================================================================
# БАЗОВЫЕ ФУНКЦИИ
# =================================================================================

def reset_base():
    """
    Полный сброс базы данных
    """
    try:
        # Удаление всех таблиц
        Base.metadata.drop_all(engine)
        
        # Очистка папки с оценками
        marks_dir = "DataBase\\DATA\\MARKS"
        if os.path.exists(marks_dir):
            for file in os.listdir(marks_dir):
                file_path = os.path.join(marks_dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        
        # Очистка папки с достижениями
        achivment_dir = "DataBase\\DATA\\ACHIVMENT"
        if os.path.exists(achivment_dir):
            for file in os.listdir(achivment_dir):
                file_path = os.path.join(achivment_dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

        # Создание новых таблиц
        Base.metadata.create_all(engine)
        
        return {"status": True, 
                "error": False, 
                "info": "База данных сброшена"
        }
    
    except Exception as e: 
        return {"status": False, 
                "error": True, 
                "info": f"Ошибка при сбросе базы данных: {e}"
        }

def insert_group():
    """
    Добавление групп в базу данных
    """
    with session_factory() as session:
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
                        
            session.commit()
            return {"status": True, 
                    "error": False, 
                    "info": "Группы добавлены"
            }

        except Exception as e:
            session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при добавлении групп: {e}"
            }

# =================================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С УЧИТЕЛЯМИ
# =================================================================================

def insert_teacher(name: str, surname: str, patronymic: str, tg_id: str = ""):
    """
    Добавление нового учителя в базу данных
    """
    with session_factory() as session:
        try:
            teacher = TeacherClass(
                name=name,
                surname=surname,
                patronymic=patronymic,
                tg_id=tg_id,
                code=""
            )

            session.add(teacher)
            session.commit()

            return {
                "status": True, 
                "error": False,
                "info": f"Учитель {teacher.name} {teacher.patronymic} добавлен в базу данных", 
                "id": teacher.id,
                "name": teacher.name,
                "surname": teacher.surname,
                "patronymic": teacher.patronymic
            }
        except Exception as e:
            session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при добавлении учителя: {e}"
            }

def delete_teacher(teacher_id: int):
    """
    Удаление учителя по ID
    """
    with session_factory() as session:
        try:
            teacher = session.query(TeacherClass).filter(TeacherClass.id == teacher_id).first()
            if not teacher:
                return {"status": False, 
                        "error": False, 
                        "info": f"Учитель с таким id не найден"
                }

            session.delete(teacher)
            session.commit()

            return {"status": True, 
                    "error": False, 
                    "info": "Учитель удален"
            }

        except Exception as e:
            session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при удалении учителя: {e}"
            }

def log_teacher(teacher_tg_id: int):
    """
    Аутентификация учителя по Telegram ID
    """
    with session_factory() as session:
        try:
            teacher = session.query(TeacherClass).filter(TeacherClass.tg_id == teacher_tg_id).first()
            if teacher is None:
                return {"status": False, 
                        "error": False, 
                        "info": f"Учитель с таким TG id не найден"
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
                    "info": f"Ошибка при аутентификации учителя по TG: {e}"
                }

def reg_teacher(teacher_tg_id: int, code: str):
    """
    Регистрация учителя по коду и Telegram ID
    """
    with session_factory() as session:
        try:
            if session.query(TeacherClass).filter_by(tg_id=teacher_tg_id).first():
                return {"status": False, 
                        "error": False, 
                        "info": "Учитель с таким TG id уже существует"
                }

            teacher = session.query(TeacherClass).filter(TeacherClass._code == code).first()
            if not teacher:
                return {"status": False, 
                        "error": False, 
                        "info": "Учитель с таким кодом не найден"}

            teacher.tg_id = teacher_tg_id
            session.commit()

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
            session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при регистрации учителя по TG: {e}"
            }

def del_teacher_tg_id(teacher_tg_id: int):
    """
    Удаление Telegram ID у учителя
    """
    with session_factory() as session:
        try:
            teacher = session.query(TeacherClass).filter(TeacherClass.tg_id == teacher_tg_id).first()
            if not teacher:
                return {"status": False, "error": False, "info": "Учитель не найден"}

            teacher.tg_id = ""
            session.commit()

            return {
                "status": True, 
                "error": False,
                "info": "Tg id учителя удален", 
                "teacher_id": teacher.id
            }

        except Exception as e:
            session.rollback()
            return {"status": False, "error": True, "info": f"Ошибка при удалении Tg id учителя: {e}"}

# =================================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ СО СТУДЕНТАМИ
# =================================================================================

def insert_student(name: str, surname: str, patronymic: str, level: level, 
                 kvant: kvant, group_num: str, login: str = "", 
                 password: str = "", tg_id: str = ""):
    """
    Добавление нового студента в базу данных
    """
    with session_factory() as session:
        try:
            # Проверка уникальности логина
            if login and session.query(StudentClass).filter_by(login=login).first():
                return {"status": False, "error": False, "info": "Студент с таким логином уже существует"}
            
            # Поиск группы
            group = session.query(GroupClass).filter(
                GroupClass.level == level,
                GroupClass.kvant == kvant,
                GroupClass.group_num == group_num,
            ).first()
            
            if not group:
                return {"status": False, "error": False, "info": f"Группа {level}-{kvant}-{group_num} не найдена"}
            
            # Хеширование пароля
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') if password else ""

            # Создание студента
            student = StudentClass(
                name=name,
                surname=surname,
                patronymic=patronymic,
                login=login,
                password=hashed_password,
                tg_id=tg_id,
                code=""
            )

            session.add(student)
            session.commit()

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
            session.commit()

            return {
                "status": True, 
                "error": False,
                "info": f"Студент {student.name} {student.surname} добавлен в БД", 
                "id": student.id
            }
            
        except Exception as e:
            session.rollback()
            return {"status": False, "error": True, "info": f"Ошибка при добавлении студента: {e}"}

def delete_student(name: str = "", surname: str = "", patronymic: str = ""):
    """
    Удаление студента
    """
    with session_factory() as session:
        try:
            # Удаление связанных файлов и записей
            
            Student = session.query(StudentClass).filter(
                StudentClass.name == name,
                StudentClass.surname == surname,
                StudentClass.patronymic == patronymic
                ).first()
            
            
            if not Student:
                return {"status": False, 
                        "error": False, 
                        "info": f"Студент с таким id не найден"
                }
            
            
            marks = session.query(MarkClass).filter(MarkClass.id_student == Student.id).all()
            for mark in marks:
                if os.path.isfile(mark.achivment):
                    os.unlink(mark.achivment)
                if os.path.isfile(mark.marks):
                    os.unlink(mark.marks)
                session.delete(mark)


            session.delete(Student)
            session.commit()

            return {"status": True, 
                    "error": False, 
                    "info": "Студент удален"
            }

        except Exception as e:
            session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при удалении студента: {e}"
            }

def reg_student_login(code: str, login: str, password: str):
    """
    Регистрация студента по коду с использованием логина и пароля
    """
    with session_factory() as session:
        try:
            if session.query(StudentClass).filter_by(login=login).first():
                return {"status": False, 
                        "error": False, 
                        "info": "Студент с таким логином уже существует"
                }

            student = session.query(StudentClass).filter(StudentClass._code == code).first()
            if not student:
                return {"status": False, 
                        "error": False, 
                        "info": "Студент с таким кодом не найден"
                }

            student.login = login
            student.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            session.commit()

            return {
                "status": True, 
                "error": False,
                "info": "Студент зарегистрирован", 
                "student_id": student.id
            }

        except Exception as e:
            session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при регистрации: {e}"
            }

def reg_student_tg(code: str, student_tg_id: int):
    """
    Регистрация студента по коду с использованием Telegram ID
    """
    with session_factory() as session:
        try:
            if session.query(StudentClass).filter_by(tg_id=student_tg_id).first():
                return {"status": False, 
                        "error": False, 
                        "info": "Студент с таким tg_id уже существует"
                }

            student = session.query(StudentClass).filter(StudentClass._code == code).first()
            if not student:
                return {"status": False, 
                        "error": False, 
                        "info": "Студент с таким кодом не найден"
                }

            student.tg_id = student_tg_id
            session.commit()

            return {
                "status": True, 
                "error": False,
                "info": "Студент зарегистрирован по tg", 
                "student_id": student.id
            }

        except Exception as e:
            session.rollback()
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при регистрации по tg: {e}"
            }

def log_student_login(login: str, password: str):
    """
    Аутентификация студента по логину и паролю
    """
    with session_factory() as session:
        try:
            student = session.query(StudentClass).filter(StudentClass.login == login).first()
            if student is None:
                return {"status": False, 
                        "error": False, 
                        "info": "Студент с таким логином не найден"
                }
            
            if not student.password:
                return {"status": False, 
                        "error": False, 
                        "info": "У студента не установлен пароль"
                }
            
            if bcrypt.checkpw(password.encode('utf-8'), student.password.encode('utf-8')):
                return {
                    "status": True, 
                    "error": False,
                    "info": "Аутентификация успешна", 
                    "student_id": student.id
                }
            else:
                return {"status": False, 
                        "error": False, 
                        "info": "Неверный пароль"
                }

        except Exception as e:
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при аутентификации: {e}"
            }

def log_student_tg(tg_id: int):
    """
    Аутентификация студента по Telegram ID
    """
    with session_factory() as session:
        try:
            student = session.query(StudentClass).filter(StudentClass.tg_id == tg_id).first()
            if student is None:
                return {"status": False, 
                        "error": False, 
                        "info": "Студент не найден"
                }
            
            return {
                "status": True, 
                "error": False,
                "info": "Успешная аутентификация", 
                "student_id": student.id
            }
            
        except Exception as e:
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при аутентификации: {e}"
            }

def get_student_info(student_id: int):
    """
    Получение ФИО студента по ID
    """
    with session_factory() as session:
        try:
            student = session.query(StudentClass).filter(StudentClass.id == student_id).first()
            if not student:
                return {"status": False, 
                        "error": False, 
                        "info": "Студент не найден"
                }

            return {
                "status": True, 
                "error": False,
                "info": "Данные студента получены",
                "name": student.name, 
                "surname": student.surname, 
                "patronymic": student.patronymic
            }

        except Exception as e:
            return {"status": False, 
                    "error": True, 
                    "info": f"Ошибка при получении ФИО студента: {e}"
            }

def get_student_info_tg(student_tg_id: int):
    """
    Получение ФИО студента по Telegram ID
    """
    with session_factory() as session:
        try:
            student = session.query(StudentClass).filter(StudentClass.tg_id == student_tg_id).first()
            if not student:
                return {"status": False, "error": False, "info": "Студент не найден"}

            return {
                "status": True, 
                "error": False,
                "info": "Данные студента получены",
                "name": student.name, 
                "surname": student.surname, 
                "patronymic": student.patronymic
            }

        except Exception as e:
            return {"status": False, "error": True, "info": f"Ошибка при получении ФИО студента: {e}"}
        
def get_student_code(name: str, surname: str, patronymic: str):
    """
    Получение кода студента по ФИО
    """
    with session_factory() as session:
        try:
            student = session.query(StudentClass).filter(
                StudentClass.name == name, 
                StudentClass.surname == surname, 
                StudentClass.patronymic == patronymic
            ).first()
            
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

def del_student_tg_id(student_tg_id: int):
    """
    Удаление Telegram ID у студента
    """
    with session_factory() as session:
        try:
            student = session.query(StudentClass).filter(StudentClass.tg_id == student_tg_id).first()
            if not student:
                return {"status": False, "error": False, "info": "Студент не найден"}

            student.tg_id = ""
            session.commit()

            return {
                "status": True, 
                "error": False,
                "info": "Tg id студента удален", 
                "student_id": student.id
            }

        except Exception as e:
            session.rollback()
            return {"status": False, "error": True, "info": f"Ошибка при удалении Tg id студента: {e}"}

# =================================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ОЦЕНКАМИ И РЕЙТИНГАМИ
# =================================================================================

def count_points():
    """
    Пересчет баллов для всех студентов на основе оценок и достижений
    """
    with session_factory() as session:
        try:
            marks = session.query(MarkClass).all()
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
                                points += topic[str(topic_mark)]
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
                session.commit()
                
            return {"status": True, "error": False, "info": "Баллы успешно пересчитаны"}

        except Exception as e:
            return {"status": False, "error": True, "info": f"Ошибка при пересчете баллов: {e}"}

def get_achivments(student_id: int):
    """
    Получение списка достижений студента
    """
    with session_factory() as session:
        try:
            mark = session.query(MarkClass).filter(MarkClass.id_student == student_id).first()
            if not mark:
                return {"status": False, "error": False, "info": "Студент не найден"}

            with open(mark.achivment, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            return {
                "status": True, 
                "error": False,
                "info": "Достижения получены",
                "achivments": data
            }

        except Exception as e:
            return {"status": False, "error": True, "info": f"Ошибка при получении достижений: {e}"}

def get_marks(student_id: int):
    """
    Получение оценок студента
    """
    with session_factory() as session:
        try:
            mark = session.query(MarkClass).filter(MarkClass.id_student == student_id).first()
            if not mark:
                return {"status": False, "error": False, "info": "Студент не найден"}

            with open(mark.marks, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            return {
                "status": True, 
                "error": False,
                "info": "Оценки получены",
                "topics": data
            }

        except Exception as e:
            return {"status": False, "error": True, "info": f"Ошибка при получении оценок: {e}"}

def get_group_rating(student_id: int):
    """
    Получение рейтинга группы студента
    """
    with session_factory() as session:
        try:
            # Получаем информацию о студенте и его группе
            student_mark = session.query(MarkClass).filter(MarkClass.id_student == student_id).first()
            if not student_mark:
                return {"status": False, "error": False, "info": "Студент не найден"}

            group = session.query(GroupClass).filter(GroupClass.id == student_mark.id_group).first()
            if not group:
                return {"status": False, "error": False, "info": "Группа не найдена"}

            # Получаем всех студентов группы, отсортированных по баллам
            students = session.query(StudentClass)\
                .join(MarkClass)\
                .join(GroupClass)\
                .filter(
                    GroupClass.level == group.level,
                    GroupClass.kvant == group.kvant,
                    GroupClass.group_num == group.group_num
                )\
                .order_by(MarkClass.points.desc())\
                .all()

            rating = []
            for student in students:
                mark = session.query(MarkClass).filter(MarkClass.id_student == student.id).first()
                rating.append({
                    "student_id": student.id,
                    "name": student.name,
                    "surname": student.surname,
                    "points": mark.points
                })
                
            return {
                "status": True, 
                "error": False,
                "info": "Рейтинг группы получен",
                "group_rating": rating
            }

        except Exception as e:
            return {"status": False, "error": True, "info": f"Ошибка при получении рейтинга группы: {e}"}

def get_kvant_rating(student_id: int):
    """
    Получение рейтинга по направлению (кванту)
    """
    with session_factory() as session:
        try:
            # Получаем информацию о студенте и его группе
            student_mark = session.query(MarkClass).filter(MarkClass.id_student == student_id).first()
            if not student_mark:
                return {"status": False, "error": False, "info": "Студент не найден"}

            group = session.query(GroupClass).filter(GroupClass.id == student_mark.id_group).first()
            if not group:
                return {"status": False, "error": False, "info": "Группа не найдена"}

            # Получаем топ студентов направления
            students = session.query(StudentClass)\
                .join(MarkClass)\
                .join(GroupClass)\
                .filter(
                    GroupClass.level == group.level,
                    GroupClass.kvant == group.kvant
                )\
                .order_by(MarkClass.points.desc())\
                .limit(4)\
                .all()

            rating = []
            for student in students:
                mark = session.query(MarkClass).filter(MarkClass.id_student == student.id).first()
                student_group = session.query(GroupClass).filter(GroupClass.id == mark.id_group).first()
                
                rating.append({
                    "student_id": student.id,
                    "name": student.name,
                    "surname": student.surname,
                    "group": f"{student_group.level.name}-{student_group.kvant.name}-{student_group.group_num}",
                    "points": mark.points
                })
                
            return {
                "status": True, 
                "error": False,
                "info": "Рейтинг направления получен",
                "kvant_rating": rating
            }

        except Exception as e:
            return {"status": False, "error": True, "info": f"Ошибка при получении рейтинга направления: {e}"}