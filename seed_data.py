from app import engine, SessionLocal, Base
from models.User import User
from models.Task import Task

def seed_database():
    print("\nInsertando datos iniciales en la base de datos...")
    
    # Crear tablas
    Base.metadata.create_all(engine)
    
    # Crear sesión
    db = SessionLocal()
    
    try:
        # Verificar si ya hay datos
        existing_users = db.query(User).count()
        if existing_users > 0:
            print(f"✓ La base de datos ya tiene {existing_users} usuarios")
            return
        
        # Crear usuarios
        user1 = User(name="Juan Esteban Perez", email="juan@gmail.com")
        user2 = User(name="Maria Jose Naranjo", email="maria@gmail.com")
        user3 = User(name="Carlos Arias", email="carlos@gmail.com")
        
        db.add(user1)
        db.add(user2)
        db.add(user3)
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
        db.refresh(user3)
        
        print(f"✓ Usuarios creados:")
        print(f"  - {user1.name} (ID: {user1.id})")
        print(f"  - {user2.name} (ID: {user2.id})")
        print(f"  - {user3.name} (ID: {user3.id})")
        
        # Crear tareas
        tasks = [
            Task(title="Completar documentación del proyecto", 
                 description="Escribir README y guías de uso", 
                 user_id=user1.id, 
                 is_completed=False),
            
            Task(title="Revisar código del módulo de usuarios", 
                 description="Code review del PR #123", 
                 user_id=user1.id, 
                 is_completed=True),
            
            Task(title="Implementar tests de integración", 
                 description="Agregar tests para los nuevos endpoints", 
                 user_id=user2.id, 
                 is_completed=False),
            
            Task(title="Actualizar dependencias del proyecto", 
                 description="Verificar y actualizar paquetes en requirements.txt", 
                 user_id=user2.id, 
                 is_completed=False),
            
            Task(title="Configurar pipeline de CI/CD", 
                 description="Setup GitHub Actions para tests automáticos", 
                 user_id=user3.id, 
                 is_completed=True),
            
            Task(title="Optimizar consultas a la base de datos", 
                 description="Agregar índices y mejorar queries", 
                 user_id=user3.id, 
                 is_completed=False),
        ]
        
        for task in tasks:
            db.add(task)
        
        db.commit()
        
        print(f"✓ {len(tasks)} tareas creadas")
        print("\n=== BASE DE DATOS INICIALIZADA ===")
        print(f"Total: {len([user1, user2, user3])} usuarios y {len(tasks)} tareas")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == '__main__':
    seed_database()
