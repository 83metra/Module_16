from fastapi import FastAPI, Path, status, Body, HTTPException
from pydantic import BaseModel
from typing import List, Annotated

app = FastAPI()

command_string = 'python -m uvicorn module_16_4:app'

users = []


class User(BaseModel):
    id: int = None
    username: str
    age: int

# class User(BaseModel):
#     id: int = None
#     username: Annotated[str, Path(min_length=3,
#                          max_length=15,
#                          description='Enter username',
#                          examples='Nick')] = 'User'
#     age: Annotated[int, Path(ge=16,
#                     le = 100,
#                     description = 'Enter age',
#                     examples = '25')] = 25


@app.get('/users')
async def get_all_users() -> List[User]:
    return users

@app.post('/user')
async def create_new_user(user: User) -> str:
    if len(users) == 0:
        user.id = len(users)+1
    else:
        user.id = users[-1].id + 1
    users.append(user)
    print(users[-1].id)
    return 'Новый пользователь {0} (возраст {1}, ID={2}) добавлен'.format(user.username, user.age, user.id)

@app.put('/user/{user_id}')
async def edit_user(user_id: int, user: str = Body(), age: int = Body()) -> str:
    try:
        edit_user = users[user_id-1]
        edit_user.username, edit_user.age = user, age
        print(edit_user)
        return 'Пользователь с ID=%s обновлён' %user_id
    except IndexError:
        raise HTTPException(status_code=404, detail=f'Пользователь с ID={user_id} не найден!')

@app.delete('/user/{user_id}')
async def delete_user(user_id: int) -> str:
    try:
        users.pop(user_id-1)
        return f'Пользователь с ID={user_id} удалён.'
    except IndexError:
        raise HTTPException(status_code=404, detail=f'Пользователь с ID={user_id} не найден!')
