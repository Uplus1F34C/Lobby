import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio

import Func 
from DataBase.settings.models import level, kvant


print("""
reset - Пересоздать БД
                
insert_teacher - Добавить учителя
delete_teacher - Удалить учителя
reg_teacher - Зарегестрировать учителя по TG id
log_teacher - Аутентифицировать учителя по TG id
del_teachers_tg_id - Удалить Tg id учителя
                
insert_student - Добавить студента
delete_student - Удалить студента
reg_student_tg - Зарегестрировать студента по tg
log_student_tg - Аутентифицировать студента по tg
del_students_tg_id - Удалить Tg id учителя
get_achivments - Получить достижения
get_marks - Получить оценки

count_points - Принудительно пересчитать количство очков у студента по ID
get_group_rating - Получить рейтинг одной группы
get_kvant_rating - Получить рейтинг одной параллели
""")

async def main():
    while True:
        try:
            cmd = input("\n->")

            if cmd == "reset":
                reset_result = await Func.reset_base()
                insert_result = await Func.insert_group()
                result = reset_result, insert_result

        # Учитель ----------------------------------------------------------------------
            elif cmd == "insert_teacher":
                result = await Func.insert_teacher(
                        name=input("Имя: "),
                        surname=input("Фамилия: "),
                        patronymic=input("Отчество: "),
                        tg_id=input("Tg id (не обязательно): "),
                )
            elif cmd == "delete_teacher":
                result = await Func.delete_teacher(
                        teacher_id=input("id (ничего не вводите для поиска по ФИО): "),
                        name=input("name: "),
                        surname=input("surname: "),
                        patronymic=input("patronymic: ")
                )
            elif cmd == "reg_teacher":
                result = await Func.reg_teacher(
                    code = input("CODE: "),
                    teacher_tg_id = input("Tg id: "),
                    )
            elif cmd == "log_teacher":
                result = await Func.log_teacher(
                    teacher_tg_id=input("Tg id: ")
                )
            elif cmd == "del_teachers_tg_id":
                result = await Func.del_teachers_tg_id(
                    teacher_tg_id = input("Tg id: "),
                    )
        # Учитель ----------------------------------------------------------------------


        # Студент ----------------------------------------------------------------------
            elif cmd == "insert_student":
                result = await Func.insert_student(
                        name=input("Имя: "),
                        surname=input("Фамилия: "),
                        patronymic=input("Отчество: "),
                        level=input(f"Уровень -> ({', '.join([l.value for l in level])}): "),
                        kvant=input(f"Квант -> ({', '.join([l.value for l in kvant])}): "),
                        group_num=input("Группа: "),
                        tg_id=input("TG id (не обязательно): "),
                )
            elif cmd == "delete_student":
                result = await Func.delete_student(
                        student_id=input("id: "),
                        name=input("name: "),
                        surname=input("surname: "),
                        patronymic=input("patronymic: ")
                     )
            # elif cmd == "reg_student_login":
            #     result = await Func.reg_student_login(
            #         code = input("CODE: "),
            #         login = input("Логин: "),
            #         password = input("Пароль: "),
            #         )
            elif cmd == "reg_student_tg":
                result = await Func.reg_student_tg(
                    code = input("CODE: "),
                    student_tg_id = input("Tg id: "),
                    )
            # elif cmd == "log_student_login":
            #     print(Func.log_student_login(
            #             login = input("Логин: "),
            #             password = input("Пароль: ")
            #         )
            #     )
            elif cmd == "log_student_tg":
                result = await Func.log_student_tg(
                    student_tg_id = input("Tg id: ")
                    )
            # elif cmd == "get_student_info":
            #     print(Func.get_student_info(
            #         student_id=input("id: ")
            #         )
            #     )
            elif cmd == "del_students_tg_id":
                result = await Func.del_students_tg_id(
                    teacher_tg_id = input("Tg id: "),
                    )
                
            elif cmd == "get_achivments":
                result = await Func.get_achivments(
                    student_id=input("id: ")
                    )
            elif cmd == "get_marks":
                result = await Func.get_marks(
                    student_id=input("id: ")
                    )
        # Студент ----------------------------------------------------------------------


        # Остальное ----------------------------------------------------------------------
            elif cmd == "count_points":
                result = await Func.count_points()
            elif cmd == "get_group_rating":
                result = await Func.get_group_rating(
                        student_id=input("id:")
                    )
            elif cmd == "get_kvant_rating":
                result = await Func.get_kvant_rating(
                        student_id=input("id: "))
        # Остальное ----------------------------------------------------------------------

            else: 
                result = "Неизвестная команда"

            print(result)

        except KeyboardInterrupt:
            print("\nЗавершение работы...")
            break
        
        except Exception as e:
            return  f"Ошибка: {e}"

if __name__ == "__main__":
    # Создаем новую event loop для всего приложения
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("\nЗавершение работы...")
    finally:
        # Правильно закрываем все соединения
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()