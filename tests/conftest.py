"""
Configuración de pytest para tests
"""
import os
import sys
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configurar las variables de entorno ANTES de importar app
os.environ.setdefault('DB_HOST', '127.0.0.1')
os.environ.setdefault('DB_USER', 'root')
os.environ.setdefault('DB_PASSWORD', 'root')
os.environ.setdefault('DB_NAME', 'todo_app_test')

# Ahora importar app con las variables configuradas
import app as app_module
from models.User import Base

# Reemplazar el engine de app con uno de pruebas
DB_URL = f"mysql+pymysql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}"
app_module.engine = create_engine(DB_URL, pool_pre_ping=True)
app_module.SessionLocal = sessionmaker(bind=app_module.engine)

@pytest.fixture(scope='session')
def test_app():
    """App de Flask para pruebas"""
    app_module.app.config['TESTING'] = True
    Base.metadata.create_all(app_module.engine)
    yield app_module.app
    Base.metadata.drop_all(app_module.engine)

@pytest.fixture
def client(test_app):
    """Cliente de prueba de Flask"""
    with test_app.test_client() as client:
        yield client

@pytest.fixture
def db():
    """Sesión de base de datos para pruebas"""
    from sqlalchemy import delete
    from models.Task import Task
    from models.User import User
    
    Base.metadata.create_all(app_module.engine)
    session = app_module.SessionLocal()
    
    # Limpiar ANTES
    try:
        session.execute(delete(Task))
        session.execute(delete(User))
        session.commit()
    except:
        session.rollback()
    
    yield session
    
    # Limpiar DESPUÉS
    try:
        session.execute(delete(Task))
        session.execute(delete(User))
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
