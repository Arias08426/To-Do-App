"""
Pruebas de Integración - Controllers
"""
import sys
sys.path.insert(0, '..')

import pytest
import json
from app import app, SessionLocal, Base, engine
from models.User import User
from models.Task import Task

@pytest.fixture
def client():
    """Cliente de prueba de Flask"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def db():
    """Base de datos de prueba"""
    Base.metadata.create_all(engine)
    db = SessionLocal()
    
    # Limpiar ANTES de cada test
    try:
        db.query(Task).delete()
        db.query(User).delete()
        db.commit()
    except:
        db.rollback()
    
    yield db
    
    # Limpiar DESPUÉS de cada test
    try:
        db.query(Task).delete()
        db.query(User).delete()
        db.commit()
    except:
        db.rollback()
    finally:
        db.close()


class TestUserController:
    """Tests de endpoints de usuarios"""
    
    def test_create_user(self, client):
        """Test crear usuario vía API"""
        response = client.post('/api/users',
            data=json.dumps({'name': 'Test User', 'email': 'test@test.com'}),
            content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'user' in data
        assert data['user']['name'] == 'Test User'
    
    def test_create_user_missing_fields(self, client):
        """Test crear usuario sin campos requeridos"""
        response = client.post('/api/users',
            data=json.dumps({'name': 'Test'}),
            content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_users(self, client, db):
        """Test listar usuarios"""
        user = User(name='Test', email='test@test.com')
        db.add(user)
        db.commit()
        
        response = client.get('/api/users')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'users' in data
        assert len(data['users']) > 0
    
    def test_get_user_by_id(self, client, db):
        """Test obtener usuario por ID"""
        user = User(name='Test', email='test@test.com')
        db.add(user)
        db.commit()
        db.refresh(user)
        
        response = client.get(f'/api/users/{user.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['user']['id'] == user.id
    
    def test_delete_user(self, client, db):
        """Test eliminar usuario"""
        user = User(name='Test', email='test@test.com')
        db.add(user)
        db.commit()
        db.refresh(user)
        
        response = client.delete(f'/api/users/{user.id}')
        
        assert response.status_code == 200


class TestTaskController:
    """Tests de endpoints de tareas"""
    
    def test_create_task(self, client, db):
        """Test crear tarea vía API"""
        user = User(name='Test', email='test@test.com')
        db.add(user)
        db.commit()
        db.refresh(user)
        
        response = client.post('/api/tasks',
            data=json.dumps({
                'title': 'Tarea Test',
                'description': 'Descripcion',
                'user_id': user.id
            }),
            content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['task']['title'] == 'Tarea Test'
    
    def test_create_task_user_not_exists(self, client):
        """Test crear tarea con usuario inexistente"""
        response = client.post('/api/tasks',
            data=json.dumps({'title': 'Tarea', 'user_id': 999}),
            content_type='application/json')
        
        assert response.status_code == 404
    
    def test_get_user_tasks(self, client, db):
        """Test listar tareas de un usuario"""
        user = User(name='Test', email='test@test.com')
        db.add(user)
        db.commit()
        db.refresh(user)
        
        task = Task(title='Tarea 1', description='Desc', user_id=user.id)
        db.add(task)
        db.commit()
        
        response = client.get(f'/api/tasks/user/{user.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['tasks']) == 1
    
    def test_update_task_status(self, client, db):
        """Test actualizar estado de tarea"""
        user = User(name='Test', email='test@test.com')
        db.add(user)
        db.commit()
        db.refresh(user)
        
        task = Task(title='Tarea', user_id=user.id, is_completed=False)
        db.add(task)
        db.commit()
        db.refresh(task)
        
        response = client.patch(f'/api/tasks/{task.id}/status',
            data=json.dumps({'is_completed': True}),
            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['task']['is_completed'] == True
    
    def test_delete_task(self, client, db):
        """Test eliminar tarea"""
        user = User(name='Test', email='test@test.com')
        db.add(user)
        db.commit()
        db.refresh(user)
        
        task = Task(title='Tarea', user_id=user.id)
        db.add(task)
        db.commit()
        db.refresh(task)
        
        response = client.delete(f'/api/tasks/{task.id}')
        
        assert response.status_code == 200
