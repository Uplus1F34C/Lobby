from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from DataBase import Func

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене замените на конкретный домен фронта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get(summary="Получить ученика",
        path='/get_student_info/{tg_id}')
async def get_achivments(tg_id: int):
    try:
        return await Func.get_student_info(tg_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ошибка: {e}")

@app.get(summary="Получить достижения",
        path='/get_achivments/{tg_id}')
async def get_achivments(tg_id: int):
    try:
        return await Func.get_achivments(tg_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ошибка: {e}")
    
@app.get(summary="Получить оценки",
        path='/get_marks/{tg_id}')
async def get_achivments(tg_id: int):
    try:
        return await Func.get_marks(tg_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ошибка: {e}")

@app.get(summary="Получить рейтинг",
        path='/get_group_raiting/{tg_id}')
async def get_achivments(tg_id: int):
    try:
        return await Func.get_group_rating(tg_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ошибка: {e}")
    
@app.get(summary="Получить рейтинг паралели",
        path='/get_kvant_raiting/{tg_id}')
async def get_achivments(tg_id: int):
    try:
        return await Func.get_kvant_rating(tg_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ошибка: {e}")