import aiofiles, json

from sqlalchemy import select, desc
from sqlalchemy.orm import joinedload

from DataBase.Settings.configuration_DB import session_factory
from DataBase.Settings.models import StudentClass, MarkClass, GroupClass

file_name = "get_service"

# === ПОЛУЧЕНИЕ ДОСТИЖЕНИЙ ===
async def get_achievements(tg_id: str = ""):
    async with session_factory() as session:
        try:
            stmt = select(StudentClass.id).where(StudentClass.tg_id == tg_id)
            result = await session.execute(stmt)
            student_id = result.scalar()

            if not student_id:
                return {
                    "status": False, 
                    "ERROR": False, 
                    "info": "Студент не найден"
                }

            stmt = select(MarkClass.achivment).where(MarkClass.id_student == student_id)
            result = await session.execute(stmt)
            achievements = result.scalars().first()
            
            if not achievements:
                return {
                    "status": True, 
                    "ERROR": False, 
                    "info": "Достижения не найдены"
                }

            async with aiofiles.open(achievements, 'r', encoding='utf-8') as file:
                content = await file.read()
                data = json.loads(content)
                
            return {
                "status": True, 
                "ERROR": False,
                "info": "Достижения получены",
                "achivments": data
            }

        except FileNotFoundError:
            return {
                "status": False, 
                "ERROR": False,
                "info": "Файл с достижениями не найден"
            }
        except json.JSONDecodeError:
            return {
                "status": False,
                "ERROR": False,
                "info": "Ошибка формата файла достижений"
            }
        except Exception as e:
            return {
                "status": False, 
                "ERROR": True, 
                "info": f"Ошибка при получении достижений в файле {file_name}: {str(e)}"
            }

# === ПОЛУЧЕНИЕ ОЦЕНОК ===
async def get_marks(tg_id: str = ""):
    async with session_factory() as session:
        try:
            # Асинхронный запрос к БД
            stmt = select(StudentClass.id).where(StudentClass.tg_id == tg_id)
            result = await session.execute(stmt)
            student_id = result.scalar()

            if not student_id:
                return {
                    "status": False, 
                    "ERROR": False, 
                    "info": "Студент не найден"
                }

            stmt = select(MarkClass.marks).where(MarkClass.id_student == student_id)
            result = await session.execute(stmt)
            marks = result.scalars().first()
            
            if not marks:
                return {
                    "status": True, 
                    "ERROR": False, 
                    "info": "Оценки не найдены"
                }

            async with aiofiles.open(marks, 'r', encoding='utf-8') as file:
                content = await file.read()
                marks = json.loads(content)
                
            return {
                "status": True, 
                "ERROR": False,
                "info": "Оценки получены",
                "topics": marks
            }

        except FileNotFoundError:
            return {
                "status": False, 
                "ERROR": False,
                "info": "Файл с оценками не найден"
            }
        except json.JSONDecodeError:
            return {
                "status": False,
                "ERROR": False,
                "info": "Ошибка формата файла оценок"
            }
        except Exception as e:
            return {
                "status": False, 
                "ERROR": True, 
                "info": f"Ошибка при получении оценок в файле {file_name}: {str(e)}"
            }

# === ПОЛУЧЕНИЕ ГРУППОВОГО РЕЙТИНГА ===  
async def get_group_rating(tg_id: str = ""):
    async with session_factory() as session:
        try:
            stmt = (
                select(MarkClass)
                .join(MarkClass.student)
                .where(StudentClass.tg_id == tg_id)
                .options(joinedload(MarkClass.group))
            )
            result = await session.execute(stmt)
            student_mark = result.scalars().first()

            if not student_mark:
                return {
                    "status": False, 
                    "ERROR": False, 
                    "info": "Студент не найден"}
            
            group = student_mark.group
                
            if not group:
                return {
                    "status": False, 
                    "error": False, 
                    "info": "Группа не найдена"
                }

            stmt = (
                select(StudentClass, MarkClass.points)
                .join(StudentClass.marks)
                .join(MarkClass.group)
                .where(
                    GroupClass.id == group.id 
                )
                .order_by(desc(MarkClass.points))
            )
            result = await session.execute(stmt)
            students_data = result.all()

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
                "ERROR": False,
                "info": "Рейтинг группы получен",
                "group_rating": rating
            }

        except Exception as e:
            return {
                "status": False,
                "ERROR": True,
                "info": f"Ошибка при получении группового рейтинга в файле {file_name}: {str(e)}"
            }

# === ПОЛУЧЕНИЕ РЕЙТИНГА КВАНТА ===    
async def get_kvant_rating(tg_id: str = ""):
    async with session_factory() as session:
        try:
            stmt = (
                select(MarkClass)
                .join(MarkClass.student)
                .where(StudentClass.tg_id == tg_id)
                .options(joinedload(MarkClass.group)))
            
            result = await session.execute(stmt)
            student_data = result.scalars().first()
            
            if not student_data:
                return {
                    "status": False, 
                    "ERROR": False, 
                    "info": "Студент не найден"
                }
            
            group = student_data.group
            
            if not group:
                return {
                    "status": False, 
                    "ERROR": False, 
                    "info": "Группа не найдена"
                }
            
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
                "ERROR": False,
                "info": "Рейтинг направления получен",
                "kvant_rating": rating,
            }

        except Exception as e:
            return {
                "status": False, 
                "ERROR": True, 
                "info": f"Ошибка при получении рейтинга кванта в файле {file_name}: {str(e)}"
            }