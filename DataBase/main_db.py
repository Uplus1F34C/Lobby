import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import Func 
from DataBase.settings.models import level, kvant


while True:
    cmd = input("""
reset - Пересоздать БД
                
insert_teacher - Добавить учителя
delete_teacher - Удалить учителя
reg_teacher - Зарегестрировать учителя по TG id
log_teacher - Аутентифицировать учителя по TG id
get_teacher_info - Получить информацию учителя по Tg id
                
insert_student - Добавить студента
delete_student - Удалить студента
reg_student_login - Зарегестрировать студента по логину
reg_student_tg - Зарегестрировать студента по tg
log_student_login - Аутентифицировать студента по логину
log_student_tg - Аутентифицировать студента по tg
get_student_info - Получить ФИО студента
get_student_info_tg - Получить ФИО студента по Tg id
get_achivments - Получить достижения
get_marks - Получить оценки

count_points - Принудительно пересчитать количство очков у студента по ID
get_group_rating - Получить рейтинг одной группы
get_kvant_rating - Получить рейтинг одной параллели
                
->"""
    )

    if cmd == "reset":
        print(Func.reset_base())
        print(Func.insert_group())

# Учитель ----------------------------------------------------------------------
    elif cmd == "insert_teacher":
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
    elif cmd == "get_teacher_info":
        print(Func.get_teacher_info(
            teacher_tg_id=input("Tg id: ")
            )
        )
# Учитель ----------------------------------------------------------------------


# Студент ----------------------------------------------------------------------
    elif cmd == "insert_student":
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
        print(Func.reg_student_login(
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
    elif cmd == "get_student_info":
        print(Func.get_student_info(
            student_id=input("id: ")
            )
        )
    elif cmd == "get_student_info_tg":
        print(Func.get_student_info_tg(
            student_tg_id=input("Tg id: ")
            )
        )
    elif cmd == "get_achivments":
        print(Func.get_achivments(
            student_id=input("id: ")
            )
        )
    elif cmd == "get_marks":
        print(Func.get_marks(
            student_id=input("id: ")
            )
        )
# Студент ----------------------------------------------------------------------


# Остальное ----------------------------------------------------------------------
    elif cmd == "count_points":
            print(Func.count_points())
    elif cmd == "get_group_rating":
        print(
            Func.get_group_rating(
                student_id=input("id:")
            )
        )
    elif cmd == "get_kvant_rating":
        print(
            Func.get_kvant_rating(
                student_id=input("id: ")
        ))
# Остальное ----------------------------------------------------------------------

    else: 
        print("Неизвестная команда")