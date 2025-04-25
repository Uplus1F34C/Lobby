import json, bcrypt, shutil, os

# from settings.database import Base, session_factory, engine
from settings.database import Base, session_factory, engine
from models import GroupClass, StudentClass, MarkClass, level, kvant

# Сброс таблиц --------------------------------------------------------------------------
def reset_base():
    try:
        # Сброс БД
        Base.metadata.drop_all(engine)
        
        # Очистка папки MARKS
        marks_dir = "DATA\MARKS"
        if os.path.exists(marks_dir):
            for file in os.listdir(marks_dir):
                file_path = os.path.join(marks_dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        
        # Очистка папки ACHIVMENT
        marks_dir = "DATA\ACHIVMENT"
        if os.path.exists(marks_dir):
            for file in os.listdir(marks_dir):
                file_path = os.path.join(marks_dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

        # Создание БД
        Base.metadata.create_all(engine)
        
        return "> База данных сброшена <"
    
    except Exception as e: 
        return f"Ошибка при сбросе БД: {e}"
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
                                topics=f"DATA\TOPICS\{k.name}\{l.name}.json",
                            )
                            session.add(group)
                            
                session.commit()
                return "> Группы добавлены <"

            except Exception as e:
                session.rollback()
                return f"Ошибка при добавлении групп: {e}"
# Добавление группы --------------------------------------------------------------------------


# Добавление студента --------------------------------------------------------------------------
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

        # обращение к группе
        group = session.query(GroupClass).filter(
            GroupClass.level == level,
            GroupClass.kvant == kvant,
            GroupClass.group_num == group_num,
            ).first()
            
        if not group:
            return f"> Группа {level}-{kvant}-{group_num} не найдена <"
        
        if session.query(StudentClass).filter_by(login=login).first():
            if login != "":
                return "> Студент с таким login уже существует <"
            
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

            if login and password and tg_id:
                Student._code = 'Использован'

            session.add(Student)
            session.commit()

            # Подключение оценок ------------------------------------------------
            marks_file_path = os.path.join("DATA\MARKS", f"{Student.id}.json")
            shutil.copy(topics, marks_file_path)

            with open(marks_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)

            with open(marks_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            # Подключение оценок ------------------------------------------------

            # Подключение достижений ------------------------------------------------
            achivment_file_path = os.path.join("DATA\ACHIVMENT", f"{Student.id}.json")
            shutil.copy("DATA/EXEMPLE_ACHIVMENT.json", achivment_file_path)
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

            return f"> Студент {Student.name} {Student.surname} добавлен(а) в БД, ему присвоен id: {Student.id} <"
            
        except Exception as e:
            session.rollback()
            return f"Ошибка при добавлении студента: {e}"
# Добавление студента --------------------------------------------------------------------------


# Получение информации о студенте --------------------------------------------------------------------------
def get_info_about_student(student_id: int):
    with session_factory() as session:
        try:
            student_info = session.query(
                StudentClass.id,
                StudentClass.name,
                StudentClass.surname,
                StudentClass.patronymic,
                GroupClass.level,
                GroupClass.kvant,
                GroupClass.group_num,
                MarkClass.points,
                MarkClass.marks,
                MarkClass.achivment,
                StudentClass.login,
                StudentClass.password,
                StudentClass.tg_id,
                StudentClass._code.label("code"),
            ).join(
                MarkClass, StudentClass.id == MarkClass.id_student
            ).join(
                GroupClass, MarkClass.id_group == GroupClass.id
            ).filter(
                StudentClass.id == student_id
            ).all()

            if student_info:
                return student_info
            else:
                return f"> Студент с ID={student_id} не найден. <"

        except Exception as e:
            return f"Ошибка при получении обработанной информации о студенте: {e}"
# Получение информации о студенте --------------------------------------------------------------------------


# Пересчет очков студента --------------------------------------------------------------------------
def count_points():
    with session_factory() as session:
        try:
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
                                print("Установлена некоректная оценка")


                with open(Mark.achivment, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                for achivka in list(data.keys()):
                    if data[achivka]["status"]:
                        points += data[achivka]["point"]

                Mark.points = points
                session.commit()
            return "Баллы высчитаны"


        except Exception as e:
            return f"Ошибка при пересчете баллов: {e}"
# Пересчет очков студента --------------------------------------------------------------------------


# Созданеи нового кода студента --------------------------------------------------------------------------
def new_student_code(student_id: int):
    with session_factory() as session:
        try:
            Student = session.query(StudentClass).filter(
            StudentClass.id == student_id).first()

            if not Student:
                session.rollback()
                return f"> Студент с ID={student_id} не найден <"
            
            from models import generate_random_code
            code = generate_random_code()
            Student._code = code

            session.commit()

            return f"> Новый код: {code} <"
        
        except Exception as e:
            session.rollback()
            return f"Ошибка при создании нового кода: {e}"
# Созданеи нового кода студента --------------------------------------------------------------------------


# Удалить студента --------------------------------------------------------------------------
def delete_student(student_id: int):
     with session_factory() as session:
        try:
            Marks = session.query(MarkClass).filter(MarkClass.id_student == student_id).all()  # Изменено на all()

            for mark in Marks:  # Проходим по всем оценкам
                if os.path.isfile(mark.achivment):
                    os.unlink(mark.achivment)
                if os.path.isfile(mark.marks):
                    os.unlink(mark.marks)
                session.delete(mark)  # Удаляем оценку


            Student = session.query(StudentClass).filter(StudentClass.id == student_id).first()
            if not Student:
                session.rollback()
                return f"> Студент с ID={student_id} не найден <"

            session.delete(Student)
            session.commit()

            return f"> Студент удален <"

        except Exception as e:
            session.rollback()
            return f"Ошибка при удалении студента: {e}"
# Удалить студента --------------------------------------------------------------------------






# Регистрация студента --------------------------------------------------------------------------
def register(code: str, login: str, password: str):
    with session_factory() as session:
        try:
            if not session.query(StudentClass).filter_by(login=login).first():
                Student = session.query(StudentClass).filter(
                StudentClass._code == code).first()

                if not Student:
                    return {"status": False, "info": "Студент с таким кодом не найден"}

                Student.login = login
                
                Student.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

                Student._code = "Использован"

                session.commit()

                return {"status": True, "info": "Студент зарегестрирован", "id": Student.id}
            else:
                return {"status": False, "info": "Студент с таким логином уже существует"}

        except Exception as e:
            session.rollback()
            return {"status": False, "info": f"Ошибка при регистрации: {e}"}
# Регистрация студента --------------------------------------------------------------------------


# Авторизация студента --------------------------------------------------------------------------
def authenticate(login: str, password: str):
    # Проверяет правильность логина и пароля
    with session_factory() as session:
        try:
            Student = session.query(StudentClass).filter(StudentClass.login == login).first()
            if Student is None:
                return {"status": False, "info": f"Студент с login={login} не найден"}
            return Student.check_password(password)
        except Exception as e:
            return {"status": False, "info": f"Ошибка при аутентификации: {e}"}
# Авторизация студента --------------------------------------------------------------------------


# Получить достижения --------------------------------------------------------------------------
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



# Получить темы --------------------------------------------------------------------------
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
# Получить темы --------------------------------------------------------------------------


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


# Получить рейтинг кванта --------------------------------------------------------------------------
def get_student_FIO(student_id: int):
    with session_factory() as session:
        try:
            # Получаем информацию о студенте
            student = session.query(StudentClass).filter(StudentClass.id == student_id).first()
            if not student:
                return {"status": False, "info": "Студент не найден"}

            return {"status": True, "name": student.name, "surname": student.surname, "patronymic": student.patronymic}

        except Exception as e:
            return  {"status": False, "info": f"Ошибка при получении ФИО студента: {e}"}
# Получить рейтинг кванта --------------------------------------------------------------------------