import mysql.connector

# Configuración de la conexión (actualiza con tus credenciales y detalles de la base de datos)
config = {
    'user': 'root',
    'password': 'NOcbGRKxrGjJdwrLQIcYrCzDeTezIjFo',
    'host': 'viaduct.proxy.rlwy.net',   # o la dirección IP de tu servidor MySQL
    'database': 'railway',
    'port': '48251',        # el puerto por defecto de MySQL es 3306
    'raise_on_warnings': True
}

# Función para realizar una consulta SELECT básica
def traer_medicamentos(id):
    try:
        # Conectar a la base de datos
        conn = mysql.connector.connect(**config)

        # Crear un cursor para ejecutar consultas
        cursor = conn.cursor()

        query = "SELECT nombre, descripcion, formula, dosis, receta FROM Medicamentos WHERE id_medicamento = %s"
        params = (id,)

        # Ejecutar una consulta
        cursor.execute(query, params)

        # Obtener el primer resultado (asumiendo que solo se espera uno)
        resultado = cursor.fetchone()

        if resultado:
            nombre, descripcion, formula, dosis, receta = resultado
            medicamento = {
                'nombre': nombre,
                'descripcion': descripcion,
                'formula': formula,
                'dosis': dosis,
                'receta': receta
            }
            return medicamento
        else:
            print("No se encontró ningún medicamento con ese ID.")
            return None

    except mysql.connector.Error as err:
        print(f"Error al conectar a MySQL: {err}")
        return None

    finally:
        # Cerrar el cursor y la conexión
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
