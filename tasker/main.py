import uvicorn
from fastapi import FastAPI, Form, Request, Depends
from sqlalchemy.orm import Session
from pydantic import ValidationError
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from starlette.templating import Jinja2Templates
from starlette.staticfiles import StaticFiles

from database import get_db
import service as TaskService
import dto as TaskDTO


app = FastAPI()
app.mount(path='/static', app=StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.get('/')
def home(request: Request, db: Session = Depends(get_db), er: str = ''):
    tasks = TaskService.get_task_all(db)
    return templates.TemplateResponse('tasks/index.html',
                                      {'request': request,
                                       'app_name': 'Tasker_FastAPI',
                                       'tasks': tasks,
                                       'er': er}
                                      )


@app.post('/add')
def add(title: str = Form(...), primary: bool = Form(False), db: Session = Depends(get_db)):
    try:
        data = TaskDTO.Task(title=title, primary=primary)
    except ValidationError as e:
        er = 'Название задачи должно быть от 1 до 90 символов'
        url = app.url_path_for('home') + f'?er={er}'
        return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)
    TaskService.create_task(data, db)
    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.get('/update/{id}')
async def update(id: int = None, db: Session = Depends(get_db)):
    TaskService.update_task(db, id)
    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.get('/delete/{id}', tags=["task"])
async def delete(id: int = None, db: Session = Depends(get_db)):
    TaskService.delete_task(id, db)
    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
