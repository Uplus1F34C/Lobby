import os

from DataBase.Settings.configuration_DB import Base, session_factory, engine
from DataBase.Settings.models import GroupClass, level, kvant

file_name = "bd_services"

# === Сброс БД ===
async def reset_db():
    try:
        # Удаление всех таблиц
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        
        # Очистка файлов
        marks_dir = "DataBase\\DATA\\MARKS"
        achivment_dir = "DataBase\\DATA\\ACHIEVEMENTS"
        
        for directory in [marks_dir, achivment_dir]:
            if os.path.exists(directory):
                for file in os.listdir(directory):
                    file_path = os.path.join(directory, file)
                    if os.path.isfile(file_path):
                        os.unlink(file_path)

        return {
                "status": True, 
                "ERROR": False, 
                "info": "БД сброшена"
        }
    
    except Exception as e: 
        return {
                "status": False, 
                "ERROR": True, 
                "info": f"Ошибка при сбросе БД в файле {file_name}: {e}"
        }

# === ДОБАВЛЕНИЕ ГРУПП ===
async def add_group():
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
            return {
                    "status": True, 
                    "ERROR": False, 
                    "info": "Группы добавлены"
            }

        except Exception as e:
            await  session.rollback()
            return {
                    "status": False, 
                    "ERROR": True, 
                    "info": f"Ошибка при добавлении групп в файле {file_name}: {e}"
            }