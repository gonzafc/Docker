import os
import time
import sys
import logging
import psycopg2
from flask import Flask, jsonify

# 1. Configuración del sistema de Logging para Docker
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout) # Envía los logs directamente a la salida estándar
    ]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            logger.info("Intentando conectar a la base de datos PostgreSQL...")
            conn = psycopg2.connect(
                host=os.environ.get('DB_HOST'),
                database=os.environ.get('DB_NAME'),
                user=os.environ.get('DB_USER'),
                password=os.environ.get('DB_PASSWORD'),
                port=os.environ.get('DB_PORT')
            )
            logger.info("¡Conexión establecida con éxito con PostgreSQL!")
            return conn
        except psycopg2.OperationalError as e:
            retries -= 1
            logger.warning(f"La base de datos aún no está lista. Reintentos restantes: {retries}. Error: {e}")
            time.sleep(2)
            
    logger.error("Error crítico: No se pudo conectar a la base de datos después de varios intentos.")
    raise Exception("No se pudo establecer conexión con PostgreSQL")

def init_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        logger.info("Verificando existencia de la tabla 'productos'...")
        cur.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                precio DECIMAL(10, 2) NOT NULL
            );
        ''')
        
        cur.execute('SELECT COUNT(*) FROM productos;')
        cantidad = cur.fetchone()[0]
        
        if cantidad == 0:
            logger.info("La tabla está vacía. Insertando datos de ejemplo iniciales...")
            cur.execute("INSERT INTO productos (nombre, precio) VALUES ('Notebook Intel i7', 1450.00);")
            cur.execute("INSERT INTO productos (nombre, precio) VALUES ('Teclado Mecánico RGB', 85.50);")
            cur.execute("INSERT INTO productos (nombre, precio) VALUES ('Monitor Curvo 27\"', 320.00);")
            conn.commit()
            logger.info("Datos de ejemplo insertados correctamente.")
        else:
            logger.info(f"La tabla ya contiene {cantidad} registros. No se requiere inicialización.")
            
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error durante la inicialización de la base de datos: {e}")

@app.route('/')
def home():
    logger.info("Endpoint raíz '/' accedido.")
    return jsonify({
        "status": "online",
        "message": "Navega a /productos para listar la información de la BD."
    })

@app.route('/productos', methods=['GET'])
def listar_productos():
    logger.info("Endpoint '/productos' solicitado de forma remota.")
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, nombre, precio FROM productos;')
        rows = cur.fetchall()
        
        lista_productos = []
        for row in rows:
            lista_productos.append({
                "id": row[0],
                "nombre": row[1],
                "precio": float(row[2])
            })
            
        cur.close()
        conn.close()
        logger.info(f"Se listaron {len(lista_productos)} productos exitosamente.")
        return jsonify(lista_productos)
    except Exception as e:
        logger.error(f"Error al listar productos de la base de datos: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    logger.info("Iniciando servidor web Flask en el puerto 5000...")
    app.run(host='0.0.0.0', port=5000)