"""
Script para cargar el dataset de Grammys a PostgreSQL.
Compatible con SQLAlchemy 1.4.x (que es la versión que usa Airflow 2.11.2).
"""
import pandas as pd
from sqlalchemy import create_engine
import os

# Configuración de conexión
DB_USER = os.getenv("POSTGRES_USER", "ws2_admin")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Ws2SecurePass2026!")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5435")
DB_NAME = os.getenv("POSTGRES_DB", "workshop_ws2")

def cargar_grammys():
    print("Cargando dataset de Grammys a PostgreSQL...")
    
    # Leer el CSV
    df = pd.read_csv('/opt/airflow/data/grammys.csv')
    print(f"  - Registros leídos: {len(df)}")
    print(f"  - Columnas: {list(df.columns)}")
    
    # Conectar a PostgreSQL con SQLAlchemy 1.4
    conn_str = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(conn_str)
    
    # Usar conexión directa (compatible con SQLAlchemy 1.4)
    with engine.connect() as conn:
        df.to_sql('grammys', conn, if_exists='replace', index=False)
    print(f"  - Tabla 'grammys' creada exitosamente con {len(df)} registros")
    
    # Verificar
    df_check = pd.read_sql("SELECT COUNT(*) as total FROM grammys", engine)
    print(f"  - Verificación: {df_check['total'][0]} registros en la tabla")

if __name__ == "__main__":
    cargar_grammys()
