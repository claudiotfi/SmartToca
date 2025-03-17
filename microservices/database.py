import psycopg2
from psycopg2 import sql
import os

# Configuração do banco de dados
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "home_automation")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# Função para conectar ao banco
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

# Função para inserir leituras de sensores
def insert_sensor_data(sensor_name, value):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO sensor_data (sensor_name, value, timestamp)
            VALUES (%s, %s, NOW())
        ""
        )
        cursor.execute(query, (sensor_name, value))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao inserir dados do sensor {sensor_name}: {e}")

# Função para buscar a última leitura de um sensor
def get_last_sensor_data(sensor_name):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            SELECT value, timestamp FROM sensor_data
            WHERE sensor_name = %s
            ORDER BY timestamp DESC LIMIT 1
        ""
        )
        cursor.execute(query, (sensor_name,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result if result else None
    except Exception as e:
        print(f"Erro ao buscar última leitura do sensor {sensor_name}: {e}")
        return None

# Função para registrar ações executadas
def log_action(action, details):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = sql.SQL("""
            INSERT INTO action_logs (action, details, timestamp)
            VALUES (%s, %s, NOW())
        ""
        )
        cursor.execute(query, (action, details))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erro ao registrar ação {action}: {e}")
