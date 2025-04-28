import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import Func 
from DataBase.settings.models import level, kvant


while True:
    cmd = input("""
reset - Пересоздать БД
                
add_teacher - Добавить учителя
delete_teacher - Удалить учителя
log_teacher - Аутентифицировать учителя 
reg_teacher - Зарегестрировать учителя    
get_fio_teacher_tg - Получить ФИО учителя по Tg id
                
add_student - Добавить студента
delete_student - Удалить студента
log_student_login - Аутентифицировать студента по логину
log_student_tg - Аутентифицировать студента по tg
reg_student_login - Зарегестрировать студента по логину
reg_student_tg - Зарегестрировать студента по tg
get_FIO_student - Получить ФИО студента
get_FIO_student_tg - Получить ФИО студента по Tg id
get_achivment - Получить достижения
get_mark - Получить оценки

count - Принудительно пересчитать количство очков у студента по ID
raiting_by_group - Получить рейтинг одной группы
raiting_by_kvant - Получить рейтинг одной параллели
                
->"""
    )

    if cmd == "reset":
        print(Func.reset_base())
        print(Func.insert_group())

# Учитель ----------------------------------------------------------------------
    elif cmd == "add_teacher":
        print(
            Func.insert_teacher(
                name=input("Имя: "),
                surname=input("Фамилия: "),
                patronymic=input("Отчество: "),
                tg_id=input("Tg id (не обязательно): "),
            )
        )
    elif cmd == "delete_teacher":
        print(
            Func.delete_teacher(
                teacher_id=input("id: ")
            )
        )
    elif cmd == "reg_teacher":
        print(Func.reg_teacher(
            code = input("CODE: "),
            teacher_tg_id = input("Tg id: "),
            )
        )
    elif cmd == "log_teacher":
        print(Func.log_teacher(
            teacher_tg_id=input("Tg id: ")
            )
        )
    elif cmd == "get_fio_teacher_tg":
        print(Func.get_FIO_teacher(
            teacher_tg_id=input("Tg id: ")
            )
        )
# Учитель ----------------------------------------------------------------------


# Студент ----------------------------------------------------------------------
    elif cmd == "add_student":
        print(
            Func.insert_student(
                name=input("Имя: "),
                surname=input("Фамилия: "),
                patronymic=input("Отчество: "),
                level=input(f"Уровень -> ({', '.join([l.value for l in level])}): "),
                kvant=input(f"Квант -> ({', '.join([l.value for l in kvant])}): "),
                group_num=input("Группа: "),
                login=input("Логин (не обязательно): "),
                password=input("Пароль (не обязательно): "),
                tg_id=input("TG id (не обязательно): "),
            )
        )
    elif cmd == "delete_student":
        print(
            Func.delete_student(
                student_id = input("if: ")
                )
        )
    elif cmd == "reg_student_login":
        print(Func.reg_student(
            code = input("CODE: "),
            login = input("Логин: "),
            password = input("Пароль: "),
            )
        )
    elif cmd == "reg_student_tg":
        print(Func.reg_student_tg(
            code = input("CODE: "),
            student_tg_id = input("Tg id: "),
            )
        )
    elif cmd == "log_student_login":
        print(Func.log_student_login(
                login = input("Логин: "),
                password = input("Пароль: ")
            )
        )
    elif cmd == "log_student_tg":
        print(Func.log_student_tg(
                tg_id = input("Tg id: ")
            )
        )
    elif cmd == "get_FIO_student":
        print(Func.get_FIO_student(
            student_id=input("id: ")
            )
        )
    elif cmd == "get_FIO_student_tg":
        print(Func.get_FIO_student_tg(
            student_tg_id=input("Tg id: ")
            )
        )
    elif cmd == "get_achivment":
        print(Func.get_achivments(
            student_id=input("id: ")
            )
        )
    elif cmd == "get_mark":
        print(Func.get_marks(
            student_id=input("id: ")
            )
        )
# Студент ----------------------------------------------------------------------


# Остальное ----------------------------------------------------------------------
    elif cmd == "count":
            print(Func.count_points())
    elif cmd == "raiting_by_group":
        print(
            Func.get_group_rating(
                student_id=input("id:")
            )
        )
    elif cmd == "raiting_by_kvant":
        print(
            Func.get_kvant_rating(
                student_id=input("id: ")
        ))
# Остальное ----------------------------------------------------------------------

    else: 
        print("Неизвестная команда")