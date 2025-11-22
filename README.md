# API REST - To-Do App

Proyecto de gestión de tareas con Flask y MySQL.

## Estructura

```
models/          # modelos de base de datos
services/        # lógica de negocio
controllers/     # endpoints de la API
tests/           # tests unitarios, integración y E2E
```

## Stack

- Flask 3.0.0
- SQLAlchemy 2.0.23
- MySQL 8.0
- pytest

## Setup

```bash
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python crear_db.py
```

## Ejecutar

```bash
python app.py
```

La API corre en `http://localhost:5000`

## API Endpoints

**Usuarios:**
- POST `/api/users` - crear usuario
- GET `/api/users` - listar usuarios
- GET `/api/users/{id}` - ver usuario
- DELETE `/api/users/{id}` - borrar usuario

**Tareas:**
- POST `/api/tasks` - crear tarea
- GET `/api/tasks/user/{id}` - tareas de un usuario
- PATCH `/api/tasks/{id}/status` - marcar como completada
- DELETE `/api/tasks/{id}` - borrar tarea

## Tests

```bash
pytest tests/ -v

# tests específicos
pytest tests/test_unitarias.py -v
pytest tests/test_integracion.py -v
pytest tests/test_e2e.py -v

# análisis de seguridad
bandit -r models/ services/ controllers/ app.py
```

## Base de Datos

**users:** id, name, email (unique)
**tasks:** id, title, description, is_completed, user_id (FK con CASCADE)
