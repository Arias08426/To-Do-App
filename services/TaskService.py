from models.Task import Task
from models.User import User

class TaskService:
    
    @staticmethod
    def create_task(db, title, description, user_id):
        if not db.get(User, user_id):
            raise ValueError("Usuario no existe")
        
        task = Task(title=title, description=description, user_id=user_id)
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    
    @staticmethod
    def get_tasks_by_user(db, user_id):
        return db.query(Task).filter(Task.user_id == user_id).all()
    
    @staticmethod
    def update_task_status(db, task_id, is_completed):
        task = db.get(Task, task_id)
        if task:
            task.is_completed = is_completed
            db.commit()
            db.refresh(task)
            return task
        return None
    
    @staticmethod
    def delete_task(db, task_id):
        task = db.get(Task, task_id)
        if task:
            db.delete(task)
            db.commit()
            return True
        return False
