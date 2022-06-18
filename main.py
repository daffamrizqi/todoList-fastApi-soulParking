from asyncio.windows_events import NULL
from fastapi import FastAPI, HTTPException
from uuid import UUID, uuid4
from typing import List
from models import Todo
from models import Status, TodoUpdateReq
from datetime import datetime

# instance of fastApi
app = FastAPI(title="Todo API SoulParking")


def dateGenerator():
    return datetime.utcnow().strftime('%d-%b-%Y %H:%M:%S')


# initial database
db: List[Todo] = [
    Todo(
        id=uuid4(),
        title="coding",
        description="coding task for college",
        created_at=dateGenerator()
    ),
    Todo(
        id=uuid4(),
        title="main bola",
        description="latihan lawan messi",
        created_at=dateGenerator()
    ),
]


@app.get('/')
async def root():
    return{"mMssage": "Hello Soul Parking!"}


# get all todos
@app.get('/api/v1/todos')
async def all_todos():
    if len(db) == 0:
        return {"Message": "You haven't added any todos for today!"}
    return db


# get todo by id
@app.get('/api/v1/todo/{todo_id}')
async def get_todo(todo_id: UUID):
    for todo in db:
        if todo.id == todo_id:
            return todo
    raise HTTPException(
        status_code=404,
        detail=f"Todo with id {todo_id} does not exist!"
    )


# add new todo
@app.post('/api/v1/todo')
async def add(todo: Todo):
    db.append(todo)
    for item in db:
        if item.title == todo.title:
            item.created_at = dateGenerator()
            item.id = uuid4()
    return {"Success": f"{todo.title} has been added to list!", "id": todo.id}


# finish todo (update status)
@app.put('/api/v1/finish/{todo_id}')
async def finish_todo(todo_id: UUID):
    for todo in db:
        if todo.id == todo_id:
            if todo.deleted_at is not None:
                return {"Error": f"Todo with id {todo.id} has already been deleted earlier and the status cannot be updated!"}
            if todo.status == Status.on_process:
                todo.status = Status.finished
                todo.finished_at = dateGenerator()
                return {"Finished": f"You have finished task: {todo.title}", f"{todo.title}": todo}
            todo.status = Status.on_process
            todo.finished_at = None
            return {"un-finished task": f"{todo.title} status is set again to ON PROCESS!", "task": todo}
    raise HTTPException(
        status_code=404,
        detail=f"Todo with id {todo_id} does not exist!"
    )


# update todo
@app.put('/api/v1/update/{todo_id}')
async def update(todo_id: UUID, todo_update: TodoUpdateReq):
    for todo in db:
        if todo.deleted_at is not None:
            raise HTTPException(
                status_code=404,
                detail=f"{todo.title} has been deleted earlier and cannot be updated!"
            )
        if todo.id == todo_id:
            if todo_update.title is not None:
                todo.title = todo_update.title
            if todo_update.description is not None:
                todo.description = todo_update.description
            if todo_update.created_at is not None:
                todo.created_at = todo_update.created_at
            if todo_update.finished_at is not None:
                todo.finished_at = todo_update.finished_at
            if todo_update.updated_at is not None:
                todo.updated_at = todo_update.updated_at
            if todo_update.deleted_at is not None:
                todo.deleted_at = todo_update.deleted_at
            if todo_update.status is not None:
                todo.status = todo_update.status
            todo.updated_at = dateGenerator()
            return {"Message": f"{todo.title} has been updated!", f"{todo.title}": todo}
    raise HTTPException(
        status_code=404,
        detail=f"Todo with id {todo_id} does not exist"
    )


# delete todo soft (soft delete)
@app.delete('/api/v1/soft-delete/{todo_id}')
async def soft_delete(todo_id: UUID):
    for todo in db:
        if todo.id == todo_id:
            if todo.deleted_at is not None:
                todo.deleted_at = None
                return {"Task recovered": f"{todo.title} has been recovered!"}
            todo.deleted_at = dateGenerator()
            return {"Updated": f"{todo.title} has been deleted!", "deleted_at": todo.deleted_at}


# delete todo (hard delete)
@app.delete('/api/v1/hard-delete/{todo_id}')
async def hard_delete(todo_id: UUID):
    for todo in db:
        if todo.id == todo_id:
            db.remove(todo)
            return {"Success": f"Task {todo.title} successfully removed!"}
    raise HTTPException(
        status_code=404,
        detail=f"Todo with id {todo_id} does not exist!"
    )
