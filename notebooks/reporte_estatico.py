"""Reporte estatico - Analisis desde la base de datos."""
import pandas as pd
from sqlalchemy import create_engine
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

conn_str = "postgresql+psycopg2://ws2_admin:Ws2SecurePass2026!@localhost:5435/workshop_ws2"
engine = create_engine(conn_str)

query = """
SELECT artists, COUNT(*) as total_grammys, AVG(popularity) as popularidad_promedio
FROM spotify_grammys_merged
GROUP BY artists
ORDER BY total_grammys DESC
LIMIT 10;
"""
df_top = pd.read_sql(query, engine)
print(df_top)

plt.figure(figsize=(10, 6))
plt.barh(df_top['artists'], df_top['total_grammys'], color='skyblue')
plt.xlabel('Cantidad de Grammys')
plt.ylabel('Artista')
plt.title('Top 10 Artistas con mas Grammys')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('/opt/airflow/data/grafico_top_artistas.png')
print("Grafico guardado")
