# Домашнее задание по теме "CRUD Запросы: Get, Post, Put Delete.

# импорт библиотеки FastAPI, Path, Annotated
from fastapi import FastAPI,status, Body, HTTPException, Path
from typing import Annotated
from pydantic import BaseModel

# Создано приложение(объект) FastAPI
app = FastAPI()

# Создайте пустой список
users = []

# Создание класса(модели) User, наследованный от BaseModel, который содержит поля id, username, age
class User(BaseModel):
    id: int
    username: str
    age: int

# get запрос по маршруту '/users', который возвращает список users
@app.get('/users')
async def get_users() -> List[User]:
    return users

# post запрос по маршруту '/user/{username}/{age}',
# Добавляет в список users объект User.
# id этого объекта будет на 1 больше, чем у последнего в списке users. Если список users пустой, то 1.
# Все остальные параметры объекта User - переданные в функцию username и age соответственно.
# В конце возвращает созданного пользователя.
@app.post('/user/{username}/{age}')
async def post_user(
        username: Annotated[str,
            Path(max_length=30, description='Введите имя', example='Vasay')],
        age: Annotated[int,
            Path(le=2000, description='Введите возраст', example='200')]):
    # присвоение следующего id пользователю
    user_id = len(users) + 1
    # присвоение значений переменной user
    user = User(id=user_id, username=username, age=age)
    # добавление новой записи в конец списка users
    users.append(user)
    return f'Пользователь {user.username} id={user.id} возраст {user.age} зарегестрирован'

# put запрос по маршруту '/user/{user_id}/{username}/{age}',
#     Обновляет username и age пользователя, если пользователь
#     с таким user_id есть в списке users и возвращает его.
#     В случае отсутствия пользователя выбрасывается исключение
#     HTTPException с описанием "User was not found" и кодом 404.
@app.put('/user/{user_id}/{username}/{age}')
async def put_user(user_id: Annotated[int, Path(description='Введите ID', example='1')],
                   username: Annotated[str, Path(max_length=30, description='Введите имя', example='Vasay')],
                   age: Annotated[int, Path(le=1000, description='Введите возраст', example='200')]):
    # цикл перебора списка users
    for i in users:
        # сравнение id списка с введенным для коррекции id
        if i.id == user_id:
            # присвоение новых значений
            i.username = username
            i.age = age
            # возврат списка обновленного списка users
            return users
    # исключение в случае отсутствия пользователя с введенным id
    raise HTTPException(status_code=404, detail="Пользователь не найден")

# delete запрос по маршруту '/user/{user_id}'
# Удаляет пользователя, если пользователь с таким user_id есть в списке users и возвращает его.
# В случае отсутствия пользователя выбрасывается исключение HTTPException с описанием "User was not found" и кодом 404.
@app.delete("/user/{user_id}")
def delete_user(user_id: Annotated[int, Path(description='Введите ID', example='1')]):
    # цикл итерации по извлечению кортежа из индекса (i) и элемента (user) списка users
    for i, user in enumerate(users):
        # сравнение введенного id с id users
        if user.id == user_id:
            # удаление записи в списке users по найденному id
            del users[i]
            # возврат измененного списка users
            return users
    # исключение в случае отсутствия пользователя с введенным id
    raise HTTPException(status_code=404, detail=f"Пользователь с ID {user_id} отсутствует")
