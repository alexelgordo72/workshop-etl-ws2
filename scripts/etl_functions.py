"""Funciones ETL simples para pipeline Spotify + Grammys."""
import pandas as pd
import pandera as pa
from pandera import Column, Check
from sqlalchemy import create_engine

# Configuracion de conexion
DB_USER = "ws2_admin"
DB_PASSWORD = "Ws2SecurePass2026!"
DB_HOST = "postgres_ws2"
DB_PORT = "5432"
DB_NAME = "workshop_ws2"

def get_engine():
    conn_str = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(conn_str)

# ============================================
# SPOTIFY
# ============================================
def extraer_spotify():
    """Lee el CSV de Spotify."""
    df = pd.read_csv('/opt/airflow/data/spotify_tracks.csv')
    print(f"Spotify: {len(df)} registros extraidos")
    df.to_pickle('/opt/airflow/data/spotify_raw.pkl')
    return len(df)

def validar_spotify():
    """Valida la calidad del DataFrame de Spotify (tolerando nulos)."""
    df = pd.read_pickle('/opt/airflow/data/spotify_raw.pkl')
    
    # Limpiar nulos ANTES de validar
    df = df.dropna(subset=['artists', 'track_id', 'popularity'])
    print(f"Despues de limpiar nulos: {len(df)} registros")
    
    schema = pa.DataFrameSchema({
        "track_id": Column(str, nullable=False),
        "artists": Column(str, nullable=False),
        "popularity": Column(int, Check.in_range(0, 100), nullable=False),
    })
    
    try:
        schema.validate(df, lazy=True)
        print("Validacion Spotify exitosa")
    except pa.errors.SchemaErrors as e:
        print(f"Validacion fallida: {e.failure_cases}")
        raise
    
    df.to_pickle('/opt/airflow/data/spotify_validated.pkl')
    return len(df)

def transformar_spotify():
    """Limpia el DataFrame de Spotify."""
    df = pd.read_pickle('/opt/airflow/data/spotify_validated.pkl')
    
    df['artists'] = df['artists'].astype(str).str.lower().str.strip()
    df = df[['track_id', 'artists', 'track_name', 'popularity', 'track_genre']]
    df = df.dropna(subset=['artists'])
    df = df.drop_duplicates(subset=['track_id'])
    
    print(f"Spotify transformado: {len(df)} registros")
    df.to_pickle('/opt/airflow/data/spotify_transformed.pkl')
    return len(df)

# ============================================
# GRAMMYS
# ============================================
def extraer_grammys():
    """Lee la tabla grammys de PostgreSQL."""
    engine = get_engine()
    df = pd.read_sql("SELECT * FROM grammys", engine)
    print(f"Grammys: {len(df)} registros extraidos")
    df.to_pickle('/opt/airflow/data/grammys_raw.pkl')
    return len(df)

def transformar_grammys():
    """Limpia el DataFrame de Grammys."""
    df = pd.read_pickle('/opt/airflow/data/grammys_raw.pkl')
    
    df['artist'] = df['artist'].astype(str).str.lower().str.strip()
    df = df[['artist', 'title', 'year', 'category', 'winner']]
    df = df.dropna(subset=['artist'])
    df = df.drop_duplicates()
    
    print(f"Grammys transformado: {len(df)} registros")
    df.to_pickle('/opt/airflow/data/grammys_transformed.pkl')
    return len(df)

# ============================================
# MERGE Y CARGA
# ============================================
def unir_datasets():
    """Une Spotify y Grammys por nombre de artista."""
    df_spotify = pd.read_pickle('/opt/airflow/data/spotify_transformed.pkl')
    df_grammys = pd.read_pickle('/opt/airflow/data/grammys_transformed.pkl')
    
    df_merged = pd.merge(
        df_spotify, df_grammys,
        left_on='artists', right_on='artist',
        how='inner'
    )
    
    print(f"Merge completado: {len(df_merged)} registros unidos")
    df_merged.to_pickle('/opt/airflow/data/merged.pkl')
    return len(df_merged)

def cargar_a_db():
    """Carga el DataFrame mergeado a PostgreSQL."""
    df = pd.read_pickle('/opt/airflow/data/merged.pkl')
    engine = get_engine()
    
    with engine.connect() as conn:
        df.to_sql('spotify_grammys_merged', conn, if_exists='replace', index=False)
    
    print(f"Cargados {len(df)} registros a spotify_grammys_merged")
    return len(df)

def guardar_csv():
    """Guarda el DataFrame mergeado como CSV."""
    df = pd.read_pickle('/opt/airflow/data/merged.pkl')
    df.to_csv('/opt/airflow/data/merged_spotify_grammys.csv', index=False)
    print(f"CSV guardado: {len(df)} registros")
    return len(df)
