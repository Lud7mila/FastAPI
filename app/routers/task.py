from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session  # Сессия БД
from app.backend.db_depends import get_db  # Функция подключения к БД
from typing import Annotated  # Аннотации, Модели БД и Pydantic.
from sqlalchemy import insert, select, update, delete  # Функции работы с записями.
from slugify import slugify  # Функция создания slug-строки

from app.models.user import User
from app.models.task import Task
from app.schemas import CreateTask, UpdateTask

router = APIRouter(prefix="/task", tags=['task'])

@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task was not found")
    return task

@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")
    task = db.scalar(select(Task).where(Task.slug == slugify(create_task.title)))
    if task is not None:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                            detail="Task with such title already exists")
    db.execute(insert(Task).values(title=create_task.title,
                                   content=create_task.content,
                                   priority=create_task.priority,
                                   slug=slugify(create_task.title),
                                   user_id=user_id))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, task: UpdateTask):
    cur_task = db.scalar(select(Task).where(Task.id == task_id))
    if cur_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task was not found")
    task_slug = db.scalar(select(Task).where(Task.slug == slugify(task.title)))
    if task_slug is not None:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,
                            detail="Task with such title already exists")
    db.execute(update(Task).where(Task.id == task_id).values(
            title=task.title,
            content=task.content,
            priority=task.priority,
            slug=slugify(task.title)))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task update is successful!'}

@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Task was not found")
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful!'}



