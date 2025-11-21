from models.User import User
from sqlalchemy.exc import IntegrityError

class UserService:
    
    @staticmethod
    def create_user(db, name, email):
        try:
            user = User(name=name, email=email)
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
        except IntegrityError:
            db.rollback()
            raise ValueError("El email ya existe")
    
    @staticmethod
    def get_all_users(db):
        return db.query(User).all()
    
    @staticmethod
    def get_user_by_id(db, user_id):
        return db.get(User, user_id)
    
    @staticmethod
    def delete_user(db, user_id):
        user = db.get(User, user_id)
        if user:
            db.delete(user)
            db.commit()
            return True
        return False
