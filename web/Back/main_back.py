from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from DataBase.Services import get_service, student_service

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене замените на конкретный домен фронта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get(summary="Получить информацию о ученике",
        path='/get_student/{tg_id}')
async def get_achivments(tg_id: int):
    try:
        return await student_service.get_student_info(tg_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ошибка: {e}")

@app.get(summary="Получить достижения",
        path='/get_achivments/{tg_id}')
async def get_achivments(tg_id: int):
    try:
        return await get_service.get_achievements(tg_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ошибка: {e}")
    
@app.get(summary="Получить оценки",
        path='/get_marks/{tg_id}')
async def get_achivments(tg_id: int):
    try:
        return await get_service.get_marks(tg_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ошибка: {e}")

@app.get(summary="Получить рейтинг группы",
        path='/get_group_raiting/{tg_id}')
async def get_achivments(tg_id: int):
    try:
        return await get_service.get_group_rating(tg_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ошибка: {e}")
    
@app.get(summary="Получить рейтинг паралели",
        path='/get_kvant_raiting/{tg_id}')
async def get_achivments(tg_id: int):
    try:
        return await get_service.get_kvant_rating(tg_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ошибка: {e}")