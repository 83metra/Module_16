from fastapi import FastAPI, Path, status, Body, HTTPException, Form, Request
from pydantic import BaseModel, validator
from fastapi.responses import HTMLResponse
from typing import List, Annotated
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory='templates')

app = FastAPI()

command_string = 'python -m uvicorn module_16_5:app'

users = []


class User(BaseModel):
    id: int = None
    username: str = 'Новый пользователь'
    age: int = 25

    @validator('username')
    def check_username(cls, username):
        assert len(username) in range(3, 16), "Имя должно быть от 3 до 16 символов!"
        return username

    @validator('age')
    def check_age(cls, age):
        assert age in range(18, 100), "Возраст с 18 лет до 100 лет!"
        return age



# class User(BaseModel):
#     id: int = None
#     username: str = Field(default=None, min_length=3,
#                          max_length=15,
#                          description='Enter username',
#                          examples='Nick')
#     age: int = Field(default= None, ge=16,
#                     le = 100,
#                     description = 'Enter age',
#                     examples = '25')


@app.get('/')
def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})

@app.get('/user/{user_id}')
async def get_user(request: Request, user_id: int) -> HTMLResponse:
    try:
        return templates.TemplateResponse('users.html', {'request': request, 'user': users[user_id-1]})
    except IndexError:
        raise HTTPException(status_code=404, detail='Пользователь не найден.')


@app.post('/user')
async def create_new_user(user: User) -> str:
    if len(users) == 0:
        user.id = len(users)+1
    else:
        user.id = users[-1].id + 1
    try:
        users.append(user)
        print(users[-1].id)
        return 'Новый пользователь {0} (возраст {1}, ID={2}) добавлен'.format(user.username, user.age, user.id)
    except IndexError:
        raise HTTPException(status_code=422, detail=f'Введены неверные данные!')

@app.put('/users/{user_id}/{username}/{age}')
async def edit_user(user_id: int, user: str, age: int) -> str:
    try:
        edit_user = users[user_id-1]
        edit_user.username, edit_user.age = user, age
        print(edit_user)
        return 'Пользователь с ID=%s обновлён' %user_id
    except IndexError:
        raise HTTPException(status_code=404, detail=f'Пользователь с ID={user_id} не найден!')

@app.delete('/users/{user_id}')
async def delete_user(user_id: int) -> str:
    try:
        users.pop(user_id-1)
        return f'Пользователь с ID={user_id} удалён.'
    except IndexError:
        raise HTTPException(status_code=404, detail=f'Пользователь с ID={user_id} не найден!')
