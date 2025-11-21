from flask import Blueprint, request, jsonify
from services.UserService import UserService

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

def get_db():
    from app import SessionLocal
    return SessionLocal()

@user_bp.route('', methods=['POST'])
def create_user():
    db = get_db()
    try:
        data = request.json
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({'error': 'faltan datos'}), 400
        
        user = UserService.create_user(db, data['name'], data['email'])
        return jsonify({'user': user.to_dict()}), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    finally:
        db.close()

@user_bp.route('', methods=['GET'])
def get_users():
    db = get_db()
    try:
        users = UserService.get_all_users(db)
        return jsonify({'users': [u.to_dict() for u in users]}), 200
    finally:
        db.close()

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()
    try:
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return jsonify({'user': user.to_dict()}), 200
    finally:
        db.close()

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db()
    try:
        if UserService.delete_user(db, user_id):
            return jsonify({'message': 'Usuario eliminado'}), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
    finally:
        db.close()
