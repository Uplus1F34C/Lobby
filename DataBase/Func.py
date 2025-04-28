import json, bcrypt, shutil, os

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from settings.database import Base, session_factory, engine
from DataBase.settings.configuration_DB import Base, session_factory, engine
from DataBase.settings.models import GroupClass, StudentClass, TeacherClass, MarkClass, level, kvant

# Сброс таблиц --------------------------------------------------------------------------
def reset_base():
    try:
        # Сброс БД
        Base.metadata.drop_all(engine)
        
        # Очистка папки MARKS
        marks_dir = "DataBase\DATA\MARKS"
        if os.path.exists(marks_dir):
            for file in os.listdir(marks_dir):
                file_path = os.path.join(marks_dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        
        # Очистка папки ACHIVMENT
        marks_dir = "DataBase\DATA\ACHIVMENT"
        if os.path.exists(marks_dir):
            for file in os.listdir(marks_dir):
                file_path = os.path.join(marks_dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

        # Создание БД
        Base.metadata.create_all(engine)
        
        return {"status": True, "info": "База данных успешно сброшена"}
    
    except Exception as e: 
        return {"status": False, "info": f"Ошибка при сбросе БД: {e}"}
# Сброс таблиц --------------------------------------------------------------------------


# Добавление групп --------------------------------------------------------------------------
def insert_group():
    with session_factory() as session:
            try:
                for k in kvant:
                    for l in level:
                        for g in range(1,5):
                            group = GroupClass(
                                year="25/26",
                                level=l,
                                kvant=k,
                                group_num=g,
                                topics=f"DataBase/DATA/TOPICS/{k.name}/{l.name}.json",
                            )
                            session.add(group)
                            
                session.commit()
                return {"status": True, "info": "Группы успешно добавлены"}

            except Exception as e:
                session.rollback()
                return {"status": False, "info": f"Ошибка при добавлении групп: {e}"}
# Добавление группы --------------------------------------------------------------------------


# Учитель -------------------------------------------------------------------------------------------------------------------------------------------
# Добавление учителя ------------------------------------------------------------------------------
def insert_teacher(
    name: str,
    surname: str,
    patronymic: str,
    tg_id: str = "",
    ):

    with session_factory() as session:
        try:
            # Созданеи студента
            Teacher = TeacherClass(
                name=name,
                surname=surname,
                patronymic=patronymic,
                tg_id=tg_id,
                code=""
            )

            session.add(Teacher)
            session.commit()

            return {"status": True, "info": f"Учитель {Teacher.name} {Teacher.patronymic} добавлен(а) в БД", "id": Teacher.id}
        except Exception as e:
            session.rollback()
            return {"status": False, "info": f"Ошибка при добавлении учителя: {e}"}
# Добавление учителя ------------------------------------------------------------------------------

# Удалить студента --------------------------------------------------------------------------------
def delete_teacher(teacher_id: int):
     with session_factory() as session:
        try:
            Teacher = session.query(TeacherClass).filter(TeacherClass.id == teacher_id).first()
            if not Teacher:
                session.rollback()
                return {"status": False, "info": f"Учитель с id={teacher_id} не найден"}

            session.delete(Teacher)
            session.commit()

            return {"status": True, "info": f"Учитель удален"}

        except Exception as e:
            session.rollback()
            return {"status": False, "info": f"Ошибка при удалении учителя: {e}"}
# Удалить студента --------------------------------------------------------------------------------

# Аутентификация учителя --------------------------------------------------------------------------
def log_teacher(teacher_tg_id: int):
    # Проверяет правильность логина и пароля
    with session_factory() as session:
        try:
            Teacher = session.query(TeacherClass).filter(TeacherClass.tg_id == teacher_tg_id).first()
            if Teacher is None:
                return {"status": False, "info": f"Учитель с tg_id={teacher_tg_id} не найден"}
            return {"status": True, "info": f"Учитель аутентифицирован", "id": Teacher.id}
        except Exception as e:
            return {"status": False, "info": f"Ошибка при аутентификации учителя: {e}"}
# Аутентификация учителя --------------------------------------------------------------------------

# Регистрация учителя -----------------------------------------------------------------------------
def reg_teacher(teacher_tg_id: int, code: str):
    with session_factory() as session:
        try:
            if not session.query(TeacherClass).filter_by(tg_id=teacher_tg_id).first():

                Teacher = session.query(TeacherClass).filter(
                TeacherClass._code == code).first()

                if not Teacher:
                    return {"status": False, "info": "Учитель с таким кодом не найден"}

                Teacher.tg_id = teacher_tg_id

                session.commit()

                return {"status": True, "info": "Учитель зарегестрирован", "id": Teacher.id}
            else:
                return {"status": False, "info": "Учитель с таким tg_id уже существует"}
            
        except Exception as e:
            session.rollback()
            return {"status": False, "info": f"Ошибка при регистрации учителя: {e}"}
# Регистрация учителя -----------------------------------------------------------------------------

# Получение информации об учителе -----------------------------------------------------------------
def get_FIO_teacher(teacher_tg_id: int):
    with session_factory() as session:
        try:
            student_info = session.query(
                TeacherClass.name,
                TeacherClass.surname,
                TeacherClass.patronymic,
            ).filter(
                TeacherClass.tg_id == teacher_tg_id
            ).first()

            return {"status": True, "name": student_info[0], "surname": student_info[1], "patronymic": student_info[2]}
            
        except Exception as e:
            session.rollback()
            return {"status": False, "info": f"Ошибка при получении информации о учителе: {e}"}
# Получение информации об учителе -----------------------------------------------------------------

# Удалить tg id учителя ---------------------------------------------------------------------
def del_tg_id_teacher(teacher_tg_id: int):
    with session_factory() as session:
        try:
            Teacher = session.query(TeacherClass).filter(
            TeacherClass.tg_id == teacher_tg_id).first()


            Teacher.tg_id = ""

            session.commit()

            return {"status": True, "info": "Tg id учителя удален", "id": Teacher.id}


        except Exception as e:
            session.rollback()
            return {"status": False, "info": f"Ошибка при удалении Tg id учителя: {e}"}
# Удалить tg id учителя ---------------------------------------------------------------------
# Учитель -------------------------------------------------------------------------------------------------------------------------------------------


# Студент -------------------------------------------------------------------------------------------------------------------------------------------
# Добавление студента -----------------------------------------------------------------------------
def insert_student(
    name: str,
    surname: str,
    patronymic: str,
    level: level,
    kvant: kvant,
    group_num: str,
    login: str = "",
    password: str = "",
    tg_id: str = "",
    ):
    with session_factory() as session:
        # кодирование пароля
        if password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        else: 
            hashed_password = ""

        # Обращение к группе
        group = session.query(GroupClass).filter(
            GroupClass.level == level,
            GroupClass.kvant == kvant,
            GroupClass.group_num == group_num,
            ).first()
            
        if not group:
            return {"status": False, "info": f'Группа {level}-{kvant}-{group_num} не найдена'}
        
        if session.query(StudentClass).filter_by(login=login).first():
            if login != "":
                return {"status": False, "info": f'Студент с таким login уже существуе'}
            
        group_id = group.id
        topics = group.topics
        
        try:
            # Созданеи студента
            Student = StudentClass(
                name=name,
                surname=surname,
                patronymic=patronymic,
                login=login,
                password=hashed_password,
                tg_id=tg_id,
                code=""
            )

            session.add(Student)
            session.commit()

            # Подключение оценок ------------------------------------------------
            marks_file_path = os.path.join("DataBase/DATA/MARKS", f"{Student.id}.json")
            shutil.copy(topics, marks_file_path)

            with open(marks_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            with open(marks_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            # Подключение оценок ------------------------------------------------

            # Подключение достижений ------------------------------------------------
            achivment_file_path = os.path.join("DataBase\DATA\ACHIVMENT", f"{Student.id}.json")
            shutil.copy("DataBase\DATA\EXEMPLE_ACHIVMENT.json", achivment_file_path)
            # Подключение достижений ------------------------------------------------

            # Создание оценок
            Mark = MarkClass(
                id_student=Student.id, 
                id_group=group_id,
                points=0,
                marks=marks_file_path,
                achivment=achivment_file_path
            )
            session.add(Mark)
            session.commit()

            return {"status": True, "info": f"Студент {Student.name} {Student.surname} добавлен(а) в БД", "id": Student.id}
            
        except Exception as e:
            session.rollback()
            return {"status": False, "info": f"Ошибка при добавлении студента: {e}"}
# Добавление студента -----------------------------------------------------------------------------

# Удалить студента --------------------------------------------------------------------------------
def delete_student(student_id: int):
     with session_factory() as session:
        try:
            Marks = session.query(MarkClass).filter(MarkClass.id_student == student_id).all() 

            for mark in Marks:  # Проходим по всем оценкам
                if os.path.isfile(mark.achivment):
                    os.unlink(mark.achivment)
                if os.path.isfile(mark.marks):
                    os.unlink(mark.marks)
                session.delete(mark)  # Удаляем оценку

            Student = session.query(StudentClass).filter(StudentClass.id == student_id).first()
            if not Student:
                session.rollback()
                return {"status": False, "info": f"Студент с id={student_id} не найден"}

            session.delete(Student)
            session.commit()

            return {"status": True, "info": f"Студент удален"}

        except Exception as e:
            session.rollback()
            return {"status": False, "info": f"Ошибка при удалении студента: {e}"}
# Удалить студента --------------------------------------------------------------------------------

# Регистрация студента через login ----------------------------------------------------------------
def reg_student(code: str, login: str, password: str):
    with session_factory() as session:
        try:
            if not session.query(StudentClass).filter_by(login=login).first():
                Student = session.query(StudentClass).filter(
                StudentClass._code == code).first()

                if not Student:
                    return {"status": False, "info": f"Студент с code={code} не найден"}

                Student.login = login
                
                Student.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                session.commit()

                return {"status": True, "info": "Студент зарегестрирован", "id": Student.id}
            else:
                return {"status": False, "info": f"Студент с login={login} уже существует"}

        except Exception as e:
            session.rollback()
            return {"status": False, "info": f"Ошибка при регистрации: {e}"}
# Регистрация студента через login ----------------------------------------------------------------

# Регистрация студента через Tg--------------------------------------------------------------------
def reg_student_tg(code: str, student_tg_id: int):
    with session_factory() as session:
        try:
            if not session.query(StudentClass).filter_by(tg_id=student_tg_id).first():
                Student = session.query(StudentClass).filter(
                StudentClass._code == code).first()

                if not Student:
                    return {"status": False, "info": "Студент с таким кодом не найден"}

                Student.tg_id = student_tg_id

                session.commit()

                return {"status": True, "info": "Студент зарегестрирован по tg", "id": Student.id}
            else:
                return {"status": False, "info": f"Студент с tg_id={student_tg_id} уже существует"}

        except Exception as e:
            session.rollback()
            return {"status": False, "info": f"Ошибка при регистрации по tg: {e}"}
# Регистрация студента через Tg -------------------------------------------------------------------

# Авторизация студента через login ----------------------------------------------------------------
def log_student_login(login: str, password: str):
    # Проверяет правильность логина и пароля
    with session_factory() as session:
        try:
            Student = session.query(StudentClass).filter(StudentClass.login == login).first()
            if Student is None:
                return {"status": False, "info": f"Студент с login={login} не найден"}
            return Student.check_password(password)
        except Exception as e:
            return {"status": False, "info": f"Ошибка при аутентификации: {e}"}
# Авторизация студента через login ----------------------------------------------------------------

# Авторизация студента через Tg -------------------------------------------------------------------
def log_student_tg(tg_id: int):
    with session_factory() as session:
        try:
            Student = session.query(StudentClass).filter(StudentClass.tg_id == tg_id).first()
            if Student is None:
                return {"status": False, "info": f"Студент не найден"}
            else:
                return {"status": True, "info": f"Успешная утентификация", "id": Student.id}
        except Exception as e:
            print(f"Ошибка при аутентификации студента по ТГ id: {e}")
            return {"status": False, "info": f"Ошибка"}
# Авторизация студента через Tg -------------------------------------------------------------------

# Получить ФИО студента ---------------------------------------------------------------------------
def get_FIO_student(student_id: int):
    with session_factory() as session:
        try:
            # Получаем информацию о студенте
            student = session.query(StudentClass).filter(StudentClass.id == student_id).first()
            if not student:
                return {"status": False, "info": "Студент не найден"}

            return {"status": True, "name": student.name, "surname": student.surname, "patronymic": student.patronymic}

        except Exception as e:
            return  {"status": False, "info": f"Ошибка при получении ФИО студента: {e}"}
# Получить ФИО студента ---------------------------------------------------------------------------

# Получить код студента по фио ---------------------------------------------------------------------------
def get_code_student(name: str, surname: str, patronymic: str):
    with session_factory() as session:
        try:
            # Получаем информацию о студенте
            student  = session.query(StudentClass).filter(StudentClass.name == name, StudentClass.surname == surname, StudentClass.patronymic == patronymic,).first()
            if not student:
                return {"status": False, "info": "Студент не найден", "code": ""}

            return {"status": True, "info": "Студент найден", "code": student._code}

        except Exception as e:
            return  {"status": False, "info": f"Ошибка при получении кода студента: {e}"}
# Получить код студента по фио ---------------------------------------------------------------------------

# Получить ФИО студента по id ---------------------------------------------------------------------
def get_FIO_student_tg(student_tg_id: int):
    with session_factory() as session:
        try:
            # Получаем информацию о студенте
            student = session.query(StudentClass).filter(StudentClass.tg_id == student_tg_id).first()
            if not student:
                return {"status": False, "info": "Студент не найден"}

            return {"status": True, "name": student.name, "surname": student.surname, "patronymic": student.patronymic}

        except Exception as e:
            return  {"status": False, "info": f"Ошибка при получении ФИО студента: {e}"}
# Получить ФИО студента по id ---------------------------------------------------------------------


# Удалить tg id студента ---------------------------------------------------------------------
def del_tg_id_student(student_tg_id: int):
    with session_factory() as session:
        try:
            Student = session.query(StudentClass).filter(
            StudentClass.tg_id == student_tg_id).first()


            Student.tg_id = ""

            session.commit()

            return {"status": True, "info": "Tg id студента удален", "id": Student.id}


        except Exception as e:
            session.rollback()
            return {"status": False, "info": f"Ошибка при удалении Tg id студента: {e}"}
# Удалить tg id студента ---------------------------------------------------------------------
# Студент -------------------------------------------------------------------------------------------------------------------------------------------


# Сайт -------------------------------------------------------------------------------------------------------------------------------------------
# Пересчет очков студентов ------------------------------------------------------------------------
def count_points():
    with session_factory() as session:
        # try:
            Mark_list = session.query(MarkClass).all()
            for Mark in Mark_list:
                
                points = 0

                with open(Mark.marks, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                
                for vetka in range(1, len(data)+1):
                    for topic in range(1, len(data[str(vetka)]) + 1):
                        mark = data[str(vetka)]["topics"][str(topic)]["mark"]
                        if mark != 0:
                            if mark < 4:
                                points += data[str(vetka)]["topics"][str(topic)][str(mark)]
                            else:
                                return {"status": False, "info": f'В файле "{Mark.marks}", в ветке "{str(vetka)}", у темы "{str(topic)}" установлена некоректная оценка - "{str(mark)}"'}


                with open(Mark.achivment, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                for achivka in list(data.keys()):
                    if data[achivka]["status"]:
                        points += data[achivka]["point"]

                Mark.points = points
                session.commit()
            return {"status": True, "info": "Баллы успешно пересчитаны"}


        # except Exception as e:
        #     return {"status": False, "info": f"Ошибка при пересчете баллов: {e}"}
# Пересчет очков студента -------------------------------------------------------------------------

# Получить достижения -----------------------------------------------------------------------------
def get_achivments(student_id: int):
    with session_factory() as session:
        try:
            ach = session.query(MarkClass).filter(MarkClass.id_student == student_id).first()


            with open(ach.achivment, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            return {"status": True, "achivments": data}

        except Exception as e:
            session.rollback()
            return  {"status": False, "info": f"Ошибка при получении достижений: {e}"}
# Получить достижения --------------------------------------------------------------------------

# Получить оценки --------------------------------------------------------------------------
def get_marks(student_id: int):
    with session_factory() as session:
        try:
            mark = session.query(MarkClass).filter(MarkClass.id_student == student_id).first()

            with open(mark.marks, 'r', encoding='utf-8') as file:
                data = json.load(file)
                
            return {"status": True, "topics": data}

        except Exception as e:
            session.rollback()
            return  {"status": False, "info": f"Ошибка при получении достижений: {e}"}
# Получить оценки --------------------------------------------------------------------------

# Получить рейтинг группы --------------------------------------------------------------------------
def get_group_rating(student_id: int):
    with session_factory() as session:
        try:
            # Получаем информацию о студенте
            student = session.query(MarkClass).filter(MarkClass.id_student == student_id).first()
            group = session.query(GroupClass).filter(GroupClass.id == student.id_group).first()
            if not group:
                return {"status": False, "info": "Студент не найден"}

            # Получаем рейтинг группы
            students = session.query(StudentClass).join(MarkClass).join(GroupClass).filter(
                GroupClass.level == group.level,
                GroupClass.kvant == group.kvant,
                GroupClass.group_num == group.group_num
            ).order_by(MarkClass.points.desc()).all()  # Сортировка по очкам

            student_info = []
            
            for student in students:
                mark = session.query(MarkClass).filter(MarkClass.id_student == student.id).first()  # Получаем оценки

                student_info.append(
                    {"id": student.id,
                     "name": student.name,
                     "surname": student.surname,
                     "point": mark.points})
                
            return {"status": True, "group_raiting": student_info}

        except Exception as e:
            return  {"status": False, "info": f"Ошибка при получении рейтинга группы: {e}"}
# Получить рейтинг группы --------------------------------------------------------------------------

# Получить рейтинг кванта --------------------------------------------------------------------------
def get_kvant_rating(student_id: int):
    with session_factory() as session:
        try:
            # Получаем информацию о студенте
            student = session.query(MarkClass).filter(MarkClass.id_student == student_id).first()
            group_ = session.query(GroupClass).filter(GroupClass.id == student.id_group).first()
            if not group_:
                return {"status": False, "info": "Студент не найден"}

            # Получаем рейтинг кванта
            students = session.query(StudentClass).join(MarkClass).join(GroupClass).filter(
                GroupClass.level == group_.level,
                GroupClass.kvant == group_.kvant
            ).order_by(MarkClass.points.desc()).limit(4).all()  # Сортировка по очкам

            student_info = []
            
            for student in students:
                mark = session.query(MarkClass).filter(MarkClass.id_student == student.id).first()  # Получаем оценки
                group = session.query(GroupClass).filter(GroupClass.id == mark.id_group).first()  
                group = f"{group.level.name}-{group.kvant.name}-{group.group_num}"

                student_info.append(
                    {"id": student.id,
                     "name": student.name,
                     "surname": student.surname,
                     "group": group,
                     "point": mark.points})
                
            return {"status": True, "kvant_raiting": student_info}

        except Exception as e:
            return  {"status": False, "info": f"Ошибка при получении рейтинга паралели: {e}"}
# Получить рейтинг кванта --------------------------------------------------------------------------
# Сайт -------------------------------------------------------------------------------------------------------------------------------------------