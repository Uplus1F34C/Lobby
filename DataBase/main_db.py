import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

from DataBase.Services import auth_service, db_services, student_service, teacher_service, get_service
from DataBase.Settings.models import level, kvant

print(
"""
__RESET_DB__ - Сброс БД
add_group - Добавление групп

add_teacher - Добавление учителя
del_teacher - Удаление учителя

reg_teacher - Регистрация учителя
log_teacher - Аутентификация учителя
logout_teacher - Удаление tg_id учителя

add_student - Добавление студента
get_student_code - Полечение кода студента
get_student_info - Получение информации о студенте
del_student - Удаление студента

reg_student - Регистрация студента
log_student - Аутентификация студента
logout_student - Удаление tg_id студента

get_achievements - Получить достижения
get_marks - Получение оценок
get_group_rating - Получение группового рейтинга
get_kvant_rating - Получение рейтинга кванта

test_pull - Заполнить таблицу для теста
"""
)

async def main():
    while True:
        try:
            cmd = input("\n-> ")

            # === ФУНКЦИИ БД ===
            if cmd == "__RESET_DB__":
                result = await db_services.reset_db()
            elif cmd == "add_group":
                result = await db_services.add_group()

            # === ФУНКЦИИ УЧИТЕЛЯ ===
            elif cmd == "add_teacher":
                result = await teacher_service.add_teacher(
                    name = input("name: "),
                    surname = input("surname: "),
                    patronymic = input("patronymic: "),
                    tg_id = input("tg_id (не обязательно): ")
                )
            elif cmd == "del_teacher":
                result = await teacher_service.del_teacher(                    
                    tg_id = input("tg_id (оставить пустым если удаление по ФИО): "),
                    name = input("name: "),
                    surname = input("surname: "),
                    patronymic = input("patronymic: "),
                )

            # === ФУНКЦИИ АВТОРИЗАЦИИ УЧИТЕЛЯ===
            elif cmd == "reg_teacher":
                result = await auth_service.reg_teacher(
                    tg_id = input("tg_id: "),
                    code = input("code: ")
                )
            elif cmd == "log_teacher":
                result = await auth_service.log_teacher(
                    tg_id = input("tg_id: ")
                )
            elif cmd == "logout_teacher":
                result = await auth_service.logout_teacher(
                    tg_id = input("tg_id: ")
                )

            # === ФУНКЦИИ СТУДЕНТЫ ===
            elif cmd == "add_student":
                result = await student_service.add_student(
                    name = input("name: "),
                    surname = input("surname: "),
                    patronymic = input("patronymic: "),
                    level=input(f"Уровень -> ({', '.join([l.value for l in level])}): "),
                    kvant=input(f"Квант -> ({', '.join([l.value for l in kvant])}): "),
                    group_num=input("Группа: "),
                    tg_id = input("tg_id (не обязательно): ")
                )
            elif cmd == "get_student_code":
                result = await student_service.get_student_code(
                        tg_id=input("id: "),
                        name=input("name: "),
                        surname=input("surname: "),
                        patronymic=input("patronymic: ")
                     )
                
            elif cmd == "get_student_info":
                result = await student_service.get_student_info(
                        tg_id=input("id: "),
                        name=input("name: "),
                        surname=input("surname: "),
                        patronymic=input("patronymic: ")
                     )
            elif cmd == "del_student":
                result = await student_service.del_student(
                        tg_id=input("id: "),
                        name=input("name: "),
                        surname=input("surname: "),
                        patronymic=input("patronymic: ")
                     )
    
            # === ФУНКЦИИ АВТОРИЗАЦИИ СТУДЕНТА ===
            elif cmd == "reg_student":
                result = await auth_service.reg_student(
                    tg_id = input("tg_id: "),
                    code = input("code: ")
                )
            elif cmd == "log_student":
                result = await auth_service.log_student(
                    tg_id = input("tg_id: ")
                )
            elif cmd == "logout_student":
                result = await auth_service.logout_student(
                    tg_id = input("tg_id: ")
                )
         
            # === ФУНКЦИИ ПОЛУЧЕНИЯ ИНФОРМАЦИИ ДЛЯ LOBBY ===
            elif cmd == "get_achievements":
                result = await get_service.get_achievements(
                    tg_id = input("tg_id: ")
                )
            elif cmd == "get_marks":
                result = await get_service.get_marks(
                    tg_id = input("tg_id: ")
                )
            elif cmd == "get_group_rating":
                result = await get_service.get_group_rating(
                    tg_id = input("tg_id: ")
                )
            elif cmd == "get_kvant_rating":
                result = await get_service.get_kvant_rating(
                    tg_id = input("tg_id: ")
                )

            elif cmd == "test_pull":
                for i in range(1,4):
                    for j in range(15):
                        result = await student_service.add_student(
                            name = "Иван",
                            surname = "Иванов",
                            patronymic = "Иванович",
                            level = "С",
                            kvant = "IT",
                            group_num = i,
                            tg_id = ""
                        )
                        if not result['status']:
                            break
                    
                    if not result['status']:
                        break
                    
                if result['status']:
                    result = {
                        "status": True, 
                        "ERROR": False,
                        "info": "Таблица заполнена"
                    }
            
            else:
                result = "Неизвестная команда"

            print(f"\nРезультат: {result}")
        
        except Exception as e:
            return  f"Ошибка в файле main_db: {e}"
        

# === ЗАПУСК ===
if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(main())

    except KeyboardInterrupt:
        print("\nЗавершение работы...")

    except Exception as e:
        print(f"Ошибка в файле main_db: {e}")

    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()