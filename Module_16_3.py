from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

users = {'1': 'Имя: Example, возраст: 18'}

command_string = 'python -m uvicorn module_16_3:app'

@app.get('/users')
async def get_all_users() -> dict:
    return users

@app.post('/users/{username}/{age}')
async def create_new_user(username: Annotated[str, Path(min_length=3, 
                                                        max_length=15, 
                                                        description='Enter username', 
                                                        examples='Nick')],
                          age: int=Path(ge=16, 
                                        le=100, 
                                        description='Enter age', 
                                        examples='25')) -> str:
    index = str(int(max(users, key=int)) + 1)
    users[index] = f'Имя: {username}, возраст: {age}'
    return 'User {0} is registered'.format(index)

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1,
                                                   le=100,
                                                   description='Enter ID', 
                                                   examples='3')],
                      username: Annotated[str, Path(min_length=3, 
                                                    max_length=15, 
                                                    description='Enter username',
                                                    examples='Nick')],
                      age: int = Path(ge=16, 
                                      le=100, 
                                      description='Enter age', 
                                      examples='25')) -> str:
    users[user_id] = f'Имя: {username}, возраст: {age}'
    return f'User {user_id} has been updated'


@app.delete('/user/{user_id}')
async def delete_user(user_id: int = Path(ge=1,
                                          le=100,
                                          description='Enter ID',
                                          examples='3')) -> str:
        users.pop(str(user_id))
        return f'User {user_id} has been deleted'
