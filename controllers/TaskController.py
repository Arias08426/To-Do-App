from flask import Blueprint, request, jsonify
from services.TaskService import TaskService

task_bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

def get_db():
    from app import SessionLocal
    return SessionLocal()

@task_bp.route('', methods=['POST'])
def create_task():
    db = get_db()
    try:
        data = request.json
        if not data or 'title' not in data or 'user_id' not in data:
            return jsonify({'error': 'faltan datos'}), 400
        
        task = TaskService.create_task(db, data['title'], data.get('description'), data['user_id'])
        return jsonify({'task': task.to_dict()}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    finally:
        db.close()

@task_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_tasks(user_id):
    db = get_db()
    try:
        tasks = TaskService.get_tasks_by_user(db, user_id)
        return jsonify({'tasks': [t.to_dict() for t in tasks]}), 200
    finally:
        db.close()

@task_bp.route('/<int:task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    db = get_db()
    try:
        data = request.json
        if not data or 'is_completed' not in data:
            return jsonify({'error': 'Falta is_completed'}), 400
        
        task = TaskService.update_task_status(db, task_id, data['is_completed'])
        if not task:
            return jsonify({'error': 'Tarea no encontrada'}), 404
        return jsonify({'task': task.to_dict()}), 200
    finally:
        db.close()

@task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    db = get_db()
    try:
        if TaskService.delete_task(db, task_id):
            return jsonify({'message': 'Tarea eliminada'}), 200
        return jsonify({'error': 'Tarea no encontrada'}), 404
    finally:
        db.close()
