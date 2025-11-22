"""
Prueba End-to-End (E2E) - Flujo completo de la aplicación
"""
import pytest
import json
from sqlalchemy import delete
from app import app, SessionLocal, Base, engine
from models.User import User
from models.Task import Task

@pytest.fixture
def client():
    """Cliente de prueba"""
    app.config['TESTING'] = True
    Base.metadata.create_all(engine)
    with app.test_client() as client:
        yield client
    
    # Limpiar
    db = SessionLocal()
    db.execute(delete(Task))
    db.execute(delete(User))
    db.commit()
    db.close()


class TestE2EWorkflow:
    """Pruebas End-to-End del flujo completo"""
    
    def test_complete_workflow(self, client):
        """
        Test E2E: Flujo completo de la aplicación
        
        1. Crear usuario
        2. Crear tareas
        3. Listar tareas
        4. Completar tarea
        5. Eliminar tarea
        6. Eliminar usuario
        """
        
        print("\n--- FLUJO E2E COMPLETO ---")
        
        # 1. Crear usuario
        response = client.post('/api/users',
            data=json.dumps({'name': 'Juan Perez', 'email': 'juan@test.com'}),
            content_type='application/json')
        
        assert response.status_code == 201
        user = json.loads(response.data)['user']
        user_id = user['id']
        print(f"✓ Usuario creado: ID={user_id}")
        
        # 2. Crear tareas
        tasks_data = [
            {'title': 'Comprar víveres', 'description': 'Leche, pan'},
            {'title': 'Hacer ejercicio', 'description': '30 min'},
            {'title': 'Estudiar', 'description': 'Python'}
        ]
        
        task_ids = []
        for task_data in tasks_data:
            response = client.post('/api/tasks',
                data=json.dumps({**task_data, 'user_id': user_id}),
                content_type='application/json')
            
            assert response.status_code == 201
            task = json.loads(response.data)['task']
            task_ids.append(task['id'])
            print(f"✓ Tarea creada: {task['title']}")
        
        # 3. Listar tareas
        response = client.get(f'/api/tasks/user/{user_id}')
        assert response.status_code == 200
        tasks = json.loads(response.data)['tasks']
        assert len(tasks) == 3
        print(f"✓ Listadas {len(tasks)} tareas")
        
        # 4. Completar primera tarea
        response = client.patch(f'/api/tasks/{task_ids[0]}/status',
            data=json.dumps({'is_completed': True}),
            content_type='application/json')
        
        assert response.status_code == 200
        assert json.loads(response.data)['task']['is_completed'] == True
        print(f"✓ Tarea completada")
        
        # 5. Eliminar segunda tarea
        response = client.delete(f'/api/tasks/{task_ids[1]}')
        assert response.status_code == 200
        print(f"✓ Tarea eliminada")
        
        # Verificar quedan 2 tareas
        response = client.get(f'/api/tasks/user/{user_id}')
        tasks = json.loads(response.data)['tasks']
        assert len(tasks) == 2
        
        # 6. Eliminar usuario (cascada)
        response = client.delete(f'/api/users/{user_id}')
        assert response.status_code == 200
        print(f"✓ Usuario eliminado")
        
        # Verificar tareas eliminadas en cascada
        response = client.get(f'/api/tasks/user/{user_id}')
        assert len(json.loads(response.data)['tasks']) == 0
        print(f"✓ Tareas eliminadas en cascada")
        
        print(f"✓ FLUJO E2E COMPLETADO")
