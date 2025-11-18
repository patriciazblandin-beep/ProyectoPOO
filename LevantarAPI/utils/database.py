import json
import logging
import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

import pyodbc 
from fastapi import HTTPException, status

# Configuración de Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- CARGAR VARIABLES DE ENTORNO ---
load_dotenv()

# Nombre del driver fijo.
# Esto SOLUCIONA el error 'IM002' que ocurre al intentar leerlo desde .env
DRIVER_NAME = "ODBC Driver 17 for SQL Server" 

# Obtener variables del .env (Solo las credenciales y el servidor)
server: str = os.getenv("SQL_SERVER")
database: str = os.getenv("SQL_DATABASE")
username: str = os.getenv("SQL_USERNAME")
password: str = os.getenv("SQL_PASSWORD")

# --- CONSTRUCCIÓN DE LA CADENA DE CONEXIÓN FINAL ---
# Usamos DRIVER_NAME fijo en lugar de os.getenv("SQL_DRIVER")
connection_string = (
    f"DRIVER={{{DRIVER_NAME}}};"
    f"SERVER={server},1433;"  # Servidor con puerto explícito
    f"DATABASE={database};"
    f"UID={username};"
    f"PWD={password};"
    f"Encrypt=yes;"
    f"TrustServerCertificate=no;"
    f"Connection Timeout=30;"
)
# ----------------------------------------------------

# --- LOG DE DEPURACIÓN (TEMPORAL) ---
logger.warning(f"DEBUG: Cadena de conexión generada con DRIVER fijo: {connection_string}")
# ------------------------------------

async def get_db_connection():
    """Crea y devuelve una conexión a la base de datos de forma asíncrona."""
    try:
        logger.info(f"Intentando conectar a la base de datos...")
        conn = pyodbc.connect(connection_string)
        logger.info("Conexión exitosa a la base de datos.")
        return conn
    except pyodbc.Error as e:
        sqlstate = e.args[0]
        logger.error(f"Error de conexión a la base de datos (SQLSTATE: {sqlstate}): {str(e)}")
        # Log específico si es el error del driver
        if 'IM002' in sqlstate:
             logger.critical(f"El sistema operativo NO encuentra el driver: {DRIVER_NAME}. Verifique la instalación de 'ODBC Driver 17 for SQL Server'.")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Error de conexión a la base de datos: {str(e)}"
        ) from e


async def execute_query_json(
    sql_query: str, 
    params: Optional[List[Any]] = None, 
    fetch_one: bool = False, 
    fetch_all: bool = False,
    needs_commit: bool = False
) -> Any:
    """
    Ejecuta una consulta SQL y devuelve los resultados como objetos Python.
    """
    conn = None
    cursor = None
    results = None
    
    try:
        conn = await get_db_connection()
        cursor = conn.cursor()
        
        param_info = "(sin parámetros)" if not params else f"(con {len(params)} parámetros)"
        logger.info(f"Ejecutando consulta {param_info}: {sql_query.strip().splitlines()[0]}")

        # Ejecutar la consulta
        if params:
            cursor.execute(sql_query, params)
        else:
            cursor.execute(sql_query)

        # Proceso de obtención de resultados (SELECT)
        if cursor.description:
            columns = [column[0] for column in cursor.description]
            
            if fetch_one:
                row = cursor.fetchone()
                if row:
                    # Conversión de tipos (ej. bytes a str)
                    processed_row = [str(item) if isinstance(item, (bytes, bytearray)) else item for item in row]
                    results = dict(zip(columns, processed_row))
                else:
                    results = None
            elif fetch_all:
                rows = cursor.fetchall()
                results = []
                for row in rows:
                    # Conversión de tipos (ej. bytes a str)
                    processed_row = [str(item) if isinstance(item, (bytes, bytearray)) else item for item in row]
                    results.append(dict(zip(columns, processed_row)))
            else:
                 logger.info("La consulta devolvió columnas, pero no se especificó fetch_one o fetch_all.")
                 results = []
        
        # Realizar commit si es necesario (INSERT, UPDATE, DELETE)
        if needs_commit:
            logger.info("Realizando commit de la transacción.")
            conn.commit()
            
        # Si no hubo retorno de datos, retornar el conteo de filas afectadas o True
        if results is None and not fetch_one and not fetch_all:
             results = cursor.rowcount if cursor.rowcount is not None else True

        # Retornamos el objeto Python (lista o dict)
        return results

    except pyodbc.Error as e:
        sqlstate = e.args[0]
        logger.error(f"Error ejecutando la consulta (SQLSTATE: {sqlstate}): {str(e)}")
        
        if conn and needs_commit:
            try:
                logger.warning("Realizando rollback debido a error.")
                conn.rollback()
            except pyodbc.Error as rb_e:
                logger.error(f"Error durante el rollback: {rb_e}")

        # Manejo específico del error de restricción UNIQUE (SQLSTATE 23000)
        if '23000' in sqlstate: 
             # Lanza HTTPException 409 para que el controlador lo gestione.
             raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Conflicto de recurso: El registro ya existe.") from e

        # Para otros errores, se propaga
        raise Exception(f"Error ejecutando consulta: {str(e)}") from e
    
    except Exception as e:
        # Propaga HTTPException si viene de la conexión
        if isinstance(e, HTTPException):
            raise
        logger.error(f"Error inesperado durante la ejecución de la consulta: {str(e)}")
        raise
    
    finally:
        # Cerrar recursos
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            logger.info("Conexión cerrada.")
