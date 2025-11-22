"""
Pruebas Unitarias - Services
"""
import pytest
from unittest.mock import Mock
from services.UserService import UserService
from services.TaskService import TaskService
from models.User import User
from models.Task import Task

class TestUserService:
    
    def test_create_user(self):
        """Test crear usuario correctamente"""
        db = Mock()
        db.commit = Mock()
        db.refresh = Mock()
        
        user = UserService.create_user(db, "Juan", "juan@test.com")
        
        assert user.name == "Juan"
        assert user.email == "juan@test.com"
        db.add.assert_called_once()
        db.commit.assert_called_once()
    
    def test_get_all_users(self):
        """Test obtener todos los usuarios"""
        db = Mock()
        db.query().all.return_value = [
            User(id=1, name="User1", email="u1@test.com"),
            User(id=2, name="User2", email="u2@test.com")
        ]
        
        users = UserService.get_all_users(db)
        
        assert len(users) == 2
        assert users[0].name == "User1"
    
    def test_delete_user(self):
        """Test eliminar usuario"""
        db = Mock()
        user_mock = User(id=1, name="Test", email="test@test.com")
        db.query().get.return_value = user_mock
        db.delete = Mock()
        db.commit = Mock()
        
        result = UserService.delete_user(db, 1)
        
        assert result == True
        db.delete.assert_called_once()
        db.commit.assert_called_once()


class TestTaskService:
    
    def test_create_task(self):
        """Test crear tarea correctamente"""
        db = Mock()
        db.query().get.return_value = User(id=1, name="Test", email="test@test.com")
        db.commit = Mock()
        db.refresh = Mock()
        
        task = TaskService.create_task(db, "Tarea 1", "Descripcion", 1)
        
        assert task.title == "Tarea 1"
        assert task.user_id == 1
        db.add.assert_called_once()
        db.commit.assert_called_once()
    
    def test_create_task_user_not_exists(self):
        """Test crear tarea con usuario inexistente"""
        db = Mock()
        db.get.return_value = None
        
        with pytest.raises(ValueError, match="Usuario no existe"):
            TaskService.create_task(db, "Tarea 1", "Desc", 999)
    
    def test_update_task_status(self):
        """Test actualizar estado de tarea"""
        db = Mock()
        task_mock = Task(id=1, title="Tarea", user_id=1, is_completed=False)
        db.query().get.return_value = task_mock
        db.commit = Mock()
        db.refresh = Mock()
        
        result = TaskService.update_task_status(db, 1, True)
        
        assert result.is_completed == True
        db.commit.assert_called_once()
