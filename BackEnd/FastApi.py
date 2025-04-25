from fastapi import FastAPI, HTTPException, Response, Cookie, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel
import jwt
# from jwt.exceptions import InvalidKeyException

from DataBase import Func ????

app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = "Key"
config.JWT_ACCESS_COOKIE_NAME = "user_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_ALGORITHM = "HS256"

security = AuthX(config=config)

def find_id(token):
    decoded_payload = jwt.decode(token, config.JWT_SECRET_KEY, algorithms=config.JWT_ALGORITHM)
    return decoded_payload['sub']

class UserLoginShema(BaseModel):
    login: str
    password: str

class UserRegisterShema(UserLoginShema):
    code: str



@app.post(summary="Регистрация", 
          path="/register")
def register(creds: UserRegisterShema, response: Response):
    ans = Func.register(code=creds.code, login=creds.login, password=creds.password)
    if ans["status"]:
        id = str(ans["id"])
        token = security.create_access_token(uid=id)
        response.set_cookie(key=config.JWT_ACCESS_COOKIE_NAME, value=token)
    return ans



@app.post(summary="Аутентифицация", 
          path="/login")
def authenticate(creds: UserLoginShema, response: Response):
    ans = Func.authenticate(login=creds.login, password=creds.password)
    if ans["status"]:
        token = security.create_access_token(uid=str(ans["id"]))
        response.set_cookie(key=config.JWT_ACCESS_COOKIE_NAME, value=token)
    return ans



@app.get(summary="Получить достижения",
        path='/get_achivments')
def get_achivments(user_token: str = Cookie(config.JWT_ACCESS_COOKIE_NAME)):  # Получаем cookie\
        try:
            student_id = find_id(user_token)  # Используем функцию для получения student_id
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Токен не найден. Ошибка: {e}")
             
        if student_id:
                return Func.get_achivments(student_id)



@app.get(summary="Получить оценки",
        path='/get_marks')
def get_marks(user_token: str = Cookie(config.JWT_ACCESS_COOKIE_NAME)):  # Получаем cookie\
        try:
            student_id = find_id(user_token)  # Используем функцию для получения student_id
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Токен не найден. Ошибка: {e}")
             
        if student_id:
                return Func.get_marks(student_id)
        

@app.get(summary="Получить рейтинг",
        path='/get_rating')
def get_rating(user_token: str = Cookie(config.JWT_ACCESS_COOKIE_NAME)):  # Получаем cookie\
        try:
            student_id = find_id(user_token)  # Используем функцию для получения student_id
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Токен не найден. Ошибка: {e}")
             
        if student_id:
                return (Func.get_group_rating(student_id), Func.get_kvant_rating(student_id))
        

@app.get(summary="Получить свое ФИО",
        path='/get_FIO')
def get_FIO(user_token: str = Cookie(config.JWT_ACCESS_COOKIE_NAME)):  # Получаем cookie\
        try:
            student_id = find_id(user_token)  # Используем функцию для получения student_id
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Токен не найден. Ошибка: {e}")
             
        if student_id:
                return Func.get_student_FIO(student_id)