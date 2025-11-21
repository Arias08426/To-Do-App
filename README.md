# API REST - To-Do App

Proyecto de gestión de tareas con Flask y MySQL.

## Estructura del proyecto

```
models/          # modelos de base de datos
services/        # lógica de negocio
controllers/     # endpoints de la API
tests/           # tests
```

## Stack

- Flask
- SQLAlchemy
- MySQL
- pytest

## Setup

```bash
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python crear_db.py
```

## Correr el servidor

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
# todos los tests
pytest tests/ -v

# tests específicos
pytest tests/test_unitarias.py -v
pytest tests/test_integracion.py -v
pytest tests/test_e2e.py -v
```

 Base de Datos

**users:** id, name, email (unique)
**tasks:** id, title, description, is_completed, user_id (FK con CASCADE)
