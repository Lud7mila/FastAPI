from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # Сессия БД
from app.backend.db_depends import get_db  # Функция подключения к БД
from typing import Annotated  # Аннотации, Модели БД и Pydantic.
from sqlalchemy import insert, select, update, delete  # Функции работы с записями.
from slugify import slugify  # Функция создания slug-строки

from app.models.user import User
from app.models.task import Task
from app.schemas import CreateUser, UpdateUser


router = APIRouter(prefix="/user", tags=['user'])

@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

@router.get("/user_id/tasks")
async def tasks_by_user_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    tasks = db.scalars(select(Task).where(Task.user_id == user_id)).all()
    if not tasks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tasks was not found")
    return tasks

@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User was not found")
    return user


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    user = db.scalar(select(User).where(User.slug == slugify(create_user.username)))
    if user is not None:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="User with such username already exists")
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age,
                                   slug=slugify(create_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, user: UpdateUser):
    cur_user = db.scalar(select(User).where(User.id == user_id))
    if cur_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")
    db.execute(update(User).where(User.id == user_id).values(
            firstname=user.firstname,
            lastname=user.lastname,
            age=user.age))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User update is successful!'}

@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")
    db.execute(delete(User).where(User.id == user_id))
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'User delete is successful!'}