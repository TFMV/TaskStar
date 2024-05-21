from typing import List, Dict, Any, Union
from litestar import get, post, put, delete, Router, Request, Response
from pydantic import BaseModel

# Task model
class Task(BaseModel):
    id: int
    title: str
    completed: bool

# In-memory task store
tasks: List[Task] = []
next_id = 1

@get("/tasks")
async def list_tasks() -> Dict[str, Any]:
    return {"tasks": tasks}

@post("/tasks")
async def create_task(request: Request) -> Dict[str, Any]:
    global next_id
    task_data = await request.json()
    task = Task(id=next_id, **task_data)
    tasks.append(task)
    next_id += 1
    return task.dict(), 201

@get("/tasks/{task_id:int}")
async def get_task(task_id: int) -> Union[Dict[str, Any], Response]:
    for task in tasks:
        if task.id == task_id:
            return task.dict()
    return Response(json={"error": "Task not found"}, status_code=404)

@put("/tasks/{task_id:int}")
async def update_task(task_id: int, request: Request) -> Union[Dict[str, Any], Response]:
    task_data = await request.json()
    for task in tasks:
        if task.id == task_id:
            task.title = task_data.get("title", task.title)
            task.completed = task_data.get("completed", task.completed)
            return task.dict()
    return Response(json={"error": "Task not found"}, status_code=404)

@delete("/tasks/{task_id:int}")
async def delete_task(task_id: int) -> Response:
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)
            return Response(status_code=204)  # No Content
    return Response(json={"error": "Task not found"}, status_code=404)

def create_router() -> List[Router]:
    return [
        Router(path="/", route_handlers=[list_tasks, create_task, get_task, update_task, delete_task])
    ]
