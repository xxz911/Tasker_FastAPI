from models import Task
from sqlalchemy.orm import Session
import dto


def create_task(data: dto.Task, db: Session):
    task = Task(title=data.title,
                is_complete=data.is_complete,
                primary=data.primary
                )
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
    except Exception as e:
        print(e)

    return task


def get_task_all(db: Session):
    return db.query(Task).order_by(Task.primary.desc()).all()


def update_task(db: Session, id: int):
    task = db.query(Task).filter(Task.id == id).first()
    task.is_complete = not task.is_complete
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(id: int, db: Session):
    task = db.query(Task).filter(Task.id == id).first()
    db.delete(task)
    db.commit()
    return task
