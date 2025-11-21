import pymysql

print("Creando DB...")

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=''  # pon tu password si tienes
    )
    
    cursor = connection.cursor()
    
    # Crear base de datos
    cursor.execute("CREATE DATABASE IF NOT EXISTS todo_app CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("✓ Base de datos 'todo_app' creada exitosamente")
    
    # Verificar
    cursor.execute("SHOW DATABASES LIKE 'todo_app'")
    result = cursor.fetchone()
    if result:
        print("✓ Base de datos verificada")
    
    cursor.close()
    connection.close()
    
    print("\n¡Listo! Ahora puedes ejecutar: python app.py")
    
except pymysql.err.OperationalError as e:
    print(f"❌ Error de conexión: {e}")
    print("\nVerifica que:")
    print("1. MySQL esté ejecutándose")
    print("2. El usuario 'root' existe")
    print("3. La contraseña sea correcta (edita línea 14 si tienes contraseña)")
except Exception as e:
    print(f"❌ Error: {e}")
