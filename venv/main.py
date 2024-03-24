from venv.dml import DML
import random
from datetime import datetime, timedelta

if __name__ == '__main__':
    instancia = DML("localhost", "root", "xyz", 3306)

    instancia.conectar()
    # instancia.consultar('SELECT * FROM proveedor')
    # # instancia.imprimir()
    # print(instancia.result)

usuarios = [
    ('Juan', 'Perez', 'Activo', 'password123', 'Gerente', 50000, '2022-01-01'),
    ('Maria', 'Rodriguez', 'Activo', 'pass1234', 'Asistente', 30000, '2022-02-15'),
    ('Carlos', 'Gomez', 'Inactivo', 'abc123', 'Analista', 45000, '2021-12-10'),
    ('Laura', 'Martinez', 'Activo', 'pass5678', 'Desarrollador', 55000, '2023-03-20'),
    ('Pedro', 'Diaz', 'Activo', 'abc456', 'Consultor', 48000, '2022-05-05'),
    ('Ana', 'Lopez', 'Inactivo', 'password987', 'Analista', 42000, '2022-04-10'),
    ('Sofia', 'Sanchez', 'Activo', 'pass9876', 'Gerente', 60000, '2021-11-12'),
    ('David', 'Torres', 'Inactivo', 'abc789', 'Asistente', 32000, '2023-01-15'),
    ('Elena', 'Garcia', 'Activo', 'password321', 'Desarrollador', 55000, '2023-02-28'),
    ('Miguel', 'Ruiz', 'Activo', 'pass654', 'Consultor', 50000, '2022-08-20'),
    ('Alejandra', 'Hernandez', 'Activo', 'abc987', 'Analista', 43000, '2021-10-25'),
    ('Diego', 'Gutierrez', 'Inactivo', 'password654', 'Gerente', 58000, '2023-05-10'),
    ('Carolina', 'Fernandez', 'Activo', 'pass789', 'Asistente', 35000, '2022-09-18'),
    ('Pablo', 'Navarro', 'Activo', 'abc321', 'Desarrollador', 60000, '2023-04-05'),
    ('Luis', 'Santos', 'Inactivo', 'password456', 'Consultor', 51000, '2022-11-30'),
    ('Paula', 'Castro', 'Activo', 'pass321', 'Analista', 44000, '2022-07-22'),
    ('Andres', 'Vargas', 'Activo', 'abc654', 'Gerente', 62000, '2021-09-15'),
    ('Monica', 'Mendoza', 'Inactivo', 'password789', 'Asistente', 38000, '2022-10-08'),
    ('Roberto', 'Gonzalez', 'Activo', 'pass456', 'Desarrollador', 58000, '2023-01-25'),
    ('Natalia', 'Perez', 'Activo', 'abc123', 'Consultor', 52000, '2022-12-12')
]

perfiles = [
    ('Administrador', '2024-01-01', 'Encargado de administrar el sistema', 'Juan Perez'),
    ('Analista', '2024-01-01', 'Encargado de análisis de datos', 'Carlos Gomez'),
    ('Asistente', '2024-01-01', 'Asistente administrativo', 'Maria Rodriguez'),
    ('Consultor', '2024-01-01', 'Consultor especializado', 'Pedro Diaz'),
    ('Desarrollador', '2024-01-01', 'Desarrollador de software', 'Laura Martinez'),
    ('Gerente', '2024-01-01', 'Gerente de departamento', 'Sofia Sanchez'),
    ('Supervisor', '2024-01-01', 'Supervisor de operaciones', 'Diego Gutierrez'),
    ('Técnico', '2024-01-01', 'Técnico de soporte', 'David Torres'),
    ('Ingeniero', '2024-01-01', 'Ingeniero de sistemas', 'Elena Garcia'),
    ('Coordinador', '2024-01-01', 'Coordinador de proyectos', 'Miguel Ruiz')
]

# Insertar perfiles
for perfil in perfiles:
    query = f"INSERT INTO Profils (name_prfl, effective_date, descriptin, in_charge) VALUES ('{perfil[0]}', '{perfil[1]}', '{perfil[2]}', '{perfil[3]}')"
    instancia.insertar(query)

# Obtener IDs de perfiles existentes
instancia.cursor.execute("SELECT id FROM Profils")
ids_perfiles = [perfil[0] for perfil in instancia.cursor.fetchall()]

# Insertar usuarios y obtener sus IDs
for usuario in usuarios:
    perfil_id = random.choice(ids_perfiles)
    query = f"INSERT INTO Users (first_name, last_name, statvs, passwrd, job_title, salary, date_entry, id_prfl) VALUES ('{usuario[0]}', '{usuario[1]}', '{usuario[2]}', '{usuario[3]}', '{usuario[4]}', {usuario[5]}, '{usuario[6]}', {perfil_id})"
    instancia.insertar(query)
    usuario_id = instancia.cursor.lastrowid  # Obtener el ID del último usuario insertado

# Obtener IDs de usuarios existentes
instancia.cursor.execute("SELECT id FROM Users")
ids_usuarios = [usuario[0] for usuario in instancia.cursor.fetchall()]

# Verificar que hay al menos un usuario en la base de datos
if not ids_usuarios:
    print("No se encontraron usuarios en la base de datos. Asegúrate de insertar usuarios antes de insertar registros de autenticación y actividades.")
    instancia.cerrar_conex()
    exit()

# Insertar registros de autenticación
for _ in range(100):
    usuario_id = random.choice(ids_usuarios)
    fecha_login = datetime.now() - timedelta(days=random.randint(1, 365))
    query = f"INSERT INTO Logins (id_users, date_login) VALUES ({usuario_id}, '{fecha_login}')"
    instancia.insertar(query)

# Insertar registros de actividades
for _ in range(12):  # 12 meses
    for _ in range(100):  # 100 registros por mes
        # Calcular el mes y el año ajustados
        now = datetime.now()
        target_month = now.month - 12 + _ + 1
        target_year = now.year + (target_month // 12) - 1
        target_month %= 12
        if target_month == 0:
            target_month = 12

        usuario_id = random.choice(ids_usuarios)
        descripcion_actividad = "Actividad " + str(random.randint(1, 10))
        fecha_actividad = datetime(target_year, target_month, random.randint(1, 28))  # Crear la fecha con el mes y año ajustados
        query = f"INSERT INTO Activities (name_act, date_act) VALUES ('{descripcion_actividad}', '{fecha_actividad}')"
        instancia.insertar(query)
        participacion_id = instancia.cursor.lastrowid
        query = f"INSERT INTO Shares (id_users, id_actvs, accmltd_points) VALUES ({usuario_id}, {participacion_id}, {random.randint(1, 10)})"
        instancia.insertar(query)

# Cerrar conexión
instancia.cerrar_conex()

print("Datos insertados exitosamente!")