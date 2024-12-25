from fastapi import FastAPI
from app.routers import task, user


app = FastAPI(debug=True, swagger_ui_parameters={"tryItOutEnabled": True})

@app.get('/')
async def welcome():
    return {"message": "Welcome to Taskmanager"}

app.include_router(task.router)
app.include_router(user.router)