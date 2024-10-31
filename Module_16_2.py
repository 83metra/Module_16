from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

command_string = 'python -m uvicorn module_16_2:app'

@app.get('/')
async def welcome() -> dict:
    return {'message': 'Главная страница.'}

@app.get('/user/admin')
async def admin() -> dict:
    return {'message': 'Вы вошли как администратор.'}


@app.get('/user/{user_id}')
async def user(user_id: int = Path(ge=0, le=100, description='Enter user ID', example='12')) -> dict:
    return {'message': f'Вы вошли как пользователь № {user_id}.'}

@app.get('/user/{username}/{age}')
# async def user_info(username: Annotated[(str, Path(min_length = 5, max_length=20, description='Enter your username', example='Artem'))],
#                     age: int = Path(ge=0, le=100, description='Enter your age', example='41')) -> dict:
async def user_info(username: Annotated[(str, Path(min_length = 5, max_length=20, description='Enter your username', example='Artem'))],
                    age: Annotated[int, Path(ge=18, le=120, description='Enter your age', example='41')]) -> dict:
    return {'message': 'Информация о пользователе. Имя: %s Возраст: %s' %(username, age)}
