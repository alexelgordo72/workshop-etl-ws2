# Workshop 002 - Pipeline ETL con Airflow

**Estudiante:** Alexander
**Materia:** ETL (G01)

## Descripcion
Pipeline ETL automatizado con Apache Airflow que integra:
- Spotify Tracks Dataset (CSV)
- Grammy Awards Dataset (PostgreSQL)

## Arquitectura
1. Extraccion: CSV + PostgreSQL
2. Validacion: Pandera
3. Transformacion: limpieza de artistas
4. Merge: por nombre de artista
5. Carga: PostgreSQL + CSV

## Stack
- Apache Airflow 2.11.2
- PostgreSQL 16
- Python 3.11
- Pandas 2.2.2
- Pandera 0.20.4
- Docker + Docker Compose
- Google Cloud Storage
- Cloudflare Tunnel

## URLs
- Airflow: https://performs-powder-generic-speaks.trycloudflare.com
- Usuario: admin / admin

## Ejecucion
docker-compose up -d
