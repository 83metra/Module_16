from fastapi import FastAPI

app = FastAPI()

command_string = 'python -m uvicorn module_16_1:app'

@app.get('/')
async def welcome() -> dict:
    return {'message': 'Главная страница.'}

@app.get('/user/admin')
async def admin() -> dict:
    return {'message': 'Вы вошли как администратор.'}


@app.get('/user/{user_id}')
async def user(user_id: int) -> dict:
    return {'message': f'Вы вошли как пользователь № {user_id}.'}

@app.get('/user')
async def user_info(username: str = 'Artem', age: int = 41) -> dict:
    return {'message': 'Информация о пользователе. Имя: %s Возраст: %s' %(username, age)}