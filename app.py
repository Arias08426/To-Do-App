from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.User import Base
from controllers.UserController import user_bp
from controllers.TaskController import task_bp
import os

# config de DB
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')  # nosec B105
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'todo_app')

DB_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)

# App
app = Flask(__name__)
app.register_blueprint(user_bp)
app.register_blueprint(task_bp)

@app.route('/')
def home():
    return jsonify({
        'message': 'API To-Do', 
        'endpoints': {
            'users': '/api/users',
            'tasks': '/api/tasks'
        }
    })

if __name__ == '__main__':
    print("\nIniciando API...")
    try:
        Base.metadata.create_all(engine)
        print("DB lista")
        print("Servidor corriendo en http://localhost:5000\n")
        debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
        app.run(debug=debug_mode, port=5000)
    except Exception as e:
        print(f"Error: {e}")
