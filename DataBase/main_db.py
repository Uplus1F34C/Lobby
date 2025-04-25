import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import Func 
from tabulate import tabulate

from DataBase.settings.models import level, kvant


while True:
    cmd = input("""\n
reset - Пересоздать БД
                
add - Добавить студента
select - Получить информацию о студенте по ID
delete - Удалить студента
new_code - Создать новый код по ID
                
count - Принудительно пересчитать количство очков у студента по ID
                
log - Провести аутентификацию          
reg - Зарегестрироваться
                
raiting_by_group - Получить рейтинг группы
raiting_by_kvant - Получить рейтинг Кванта \n
->"""
    )

    if cmd == "reset":
        print(Func.reset_base())
        print(Func.insert_group())

    elif cmd == "add":
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

    elif cmd == "test":
        for i in range(1, 17):
            print(
                Func.insert_student(
                name=str("n" * i),
                surname=str("s" * i),
                patronymic=str("p" * i),
                level="Стартовый",
                kvant="IT",
                group_num="1",
                login="",
                password="",
                tg_id=""
                )
            )
        for i in range(1, 17):
            print(
                Func.insert_student(
                name=str("n2" * i),
                surname=str("s2" * i),
                patronymic=str("p2" * i),
                level="Стартовый",
                kvant="IT",
                group_num="3",
                login="",
                password="",
                tg_id=""
                )
            )

    elif cmd == "raiting_by_group":
        print(
            Func.get_group_rating(
                level=input(f"Уровень -> ({', '.join([l.value for l in level])}): "),
                kvant=input(f"Квант -> ({', '.join([l.value for l in kvant])}): "),
                group_num=input("Группа: "),
        ))

    elif cmd == "raiting_by_kvant":
        print(
            Func.get_kvant_rating(
                level=input(f"Уровень -> ({', '.join([l.value for l in level])}): "),
                kvant=input(f"Квант -> ({', '.join([l.value for l in kvant])}): ")
        ))

    elif cmd == "select":
        student_id = int(input("Введите ID студента: "))
        student_info = Func.get_info_about_student(student_id)
        
        if isinstance(student_info, str):
            print(student_info)
        else:
            # Преобразуем данные в формат таблицы
            headers = ["ID", "Имя", "Фамилия", "Отчество", "Группа", "Баллы", "Оценки", "achivment", "Логин", "Пароль", "TG ID", "Код"]
            if student_info[0][11]:
                password = "Зашифрован"
            else:
                password = None
            table_data = [
                [
                    info[0],  # ID
                    info[1],  # Имя
                    info[2],  # Фамилия
                    info[3],  # Отчество
                    f"{info[4].value}-{info[5].value}-{info[6]}",  
                    info[7],  # Баллы
                    info[8], # Оценки
                    info[9], # Оценки
                    info[10],  # Логин
                    password,  # Пароль
                    info[12],  # TG ID
                    info[13]  # Код
                ]
                for info in student_info
            ]
            print(tabulate(table_data, headers=headers, tablefmt="grid"))

    elif cmd == "auth":
        Func.authenticate(
            input("Логин: "),
            input("Пароль: ")
            )
    
    elif cmd == "count":
        print(Func.count_points())

    elif cmd == "register":
        print(Func.register(
            input("CODE: "),
            input("login: "),
            input("password: "),
            )
        )

    elif cmd == "new_code":
        print(Func.new_student_code(int(input("ID студента: "))))

    elif cmd == "delete":
        print(Func.delete_student(int(input("ID студента: "))))

    else: 
        print("Неизвестная команда")