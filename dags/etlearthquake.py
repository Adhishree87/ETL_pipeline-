from airflow import DAG
from airflow.decorators import task
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from datetime import datetime
import json

# Connection IDs
HTTP_CONN_ID = 'usgs_earthquake_api'
POSTGRES_CONN_ID = 'postgres_default'

# Default args
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1)
}

# DAG Definition
with DAG(
    dag_id='earthquake_etl_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='ETL pipeline to fetch earthquake data from USGS and store in Postgres'
) as dag:

    @task()
    def extract_data():
        """Extract earthquake data from USGS API."""
        http_hook = HttpHook(http_conn_id=HTTP_CONN_ID, method='GET')
        endpoint = 'all_day.geojson'  # Relative endpoint to the Host
        response = http_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    @task()
    def transform_data(raw_data):
        """Transform earthquake data."""
        features = raw_data['features']
        transformed = []

        for feature in features:
            props = feature['properties']
            geom = feature['geometry']
            quake = {
                'id': feature['id'],
                'magnitude': props['mag'],
                'place': props['place'],
                'time': datetime.utcfromtimestamp(props['time'] / 1000.0),
                'longitude': geom['coordinates'][0],
                'latitude': geom['coordinates'][1],
                'depth': geom['coordinates'][2]
            }
            transformed.append(quake)

        return transformed

    @task()
    def load_data(transformed_data):
        """Load transformed data into PostgreSQL."""
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        # Create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS earthquake_data (
                id TEXT PRIMARY KEY,
                magnitude FLOAT,
                place TEXT,
                time TIMESTAMP,
                longitude FLOAT,
                latitude FLOAT,
                depth FLOAT
            );
        """)

        # Insert data
        for quake in transformed_data:
            cursor.execute("""
                INSERT INTO earthquake_data (id, magnitude, place, time, longitude, latitude, depth)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (
                quake['id'],
                quake['magnitude'],
                quake['place'],
                quake['time'],
                quake['longitude'],
                quake['latitude'],
                quake['depth']
            ))

        conn.commit()
        cursor.close()

    # DAG Flow
    raw = extract_data()
    processed = transform_data(raw)
    load_data(processed)
