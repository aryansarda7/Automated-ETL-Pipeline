import psycopg2
import pyodbc
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

POSTGRES_CONFIG = {
    "host": os.environ.get("POSTGRES_HOST"),
    "port": int(os.environ.get("POSTGRES_PORT")),
    "dbname": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD")
}


SQLSERVER_CONN_STRING = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={os.environ.get('SQLSERVER_HOST')},{os.environ.get('SQLSERVER_PORT')};"
    f"DATABASE={os.environ.get('SQLSERVER_DB')};"
    f"UID={os.environ.get('SQLSERVER_USER')};"
    f"PWD={os.environ.get('SQLSERVER_PASSWORD')}"
)


def fetch_data_from_postgres():
    conn = psycopg2.connect(**POSTGRES_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transformed_user_posts;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    logging.info(f"✅ Fetched {len(rows)} rows from PostgreSQL.")
    return rows

def insert_into_sqlserver(rows):
    conn = pyodbc.connect(SQLSERVER_CONN_STRING)
    cursor = conn.cursor()

    # Create the target table if it doesn't exist
    cursor.execute(
        "IF OBJECT_ID('FactUserPosts', 'U') IS NULL "
        "CREATE TABLE FactUserPosts ("
        "post_id INT,"
        "post_title NVARCHAR(MAX),"
        "post_body NVARCHAR(MAX),"
        "user_name NVARCHAR(255),"
        "user_email NVARCHAR(255));"
    )

    insert_query = (
        "INSERT INTO FactUserPosts (post_id, post_title, post_body, user_name, user_email) "
        "VALUES (?, ?, ?, ?, ?)"
    )
    cursor.executemany(insert_query, rows)
    conn.commit()
    cursor.close()
    conn.close()
    logging.info(f"✅ Inserted {len(rows)} rows into SQL Server.")

def main():
    rows = fetch_data_from_postgres()
    insert_into_sqlserver(rows)

if __name__ == "__main__":
    main()

