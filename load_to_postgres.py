import psycopg2
import json
import logging
import time
import os


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_CONFIG = {
    'host': os.environ.get('POSTGRES_HOST'),
    'port': int(os.environ.get('POSTGRES_PORT')),
    'dbname': os.environ.get('POSTGRES_DB'),
    'user': os.environ.get('POSTGRES_USER'),
    'password': os.environ.get('POSTGRES_PASSWORD')
}

def connect_to_postgres(retries=5, delay=3):
    for i in range(retries):
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            logging.info("Connected to PostgreSQL successfully.")
            return conn
        except Exception as e:
            logging.warning(f"Connection failed (attempt {i+1}/{retries}): {e}")
            time.sleep(delay)
    logging.error("All connection attempts failed.")
    raise Exception("PostgreSQL connection failed after retries.")

def create_table(cursor):
    cursor.execute("""

        CREATE TABLE IF NOT EXISTS staging_users(
                    id INTEGER PRIMARY KEY,
                    name VARCHAR,
                    username VARCHAR,
                    email VARCHAR,
                    phone VARCHAR,
                    website VARCHAR,
                    company_name VARCHAR,
                    address_city VARCHAR
                   );
""")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS staging_posts (
            id INTEGER PRIMARY KEY,
            userId INTEGER,
            title text,
            body TEXT                   
                   );
""")
    
    logging.info("Tables created or verified successfully.")

def insert_user(cursor, users):
    for user in users:
        cursor.execute(
            """
            INSERT INTO staging_users (id, name, username, email, phone, website, company_name, address_city)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
""", (
            user.get("id"),
            user.get("name"),
            user.get("username"),
            user.get("email"),
            user.get("phone"),
            user.get("website"),
            user.get("company", {}).get("name"),
            user.get("address", {}).get("city")
))
    logging.info(f"Inserted {len(users)} users into staging_users.")

def insert_posts(cursor, posts):
    for post in posts:
        cursor.execute("""
            INSERT INTO staging_posts (id, userId, title, body)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING;
""", (
            post.get("id"),
            post.get("userId"),
            post.get("title"),
            post.get("body")
))
    logging.info(f"Inserted {len(posts)} posts into staging_posts.")

def main():

    with open("user.json", "r", encoding="utf-8") as f:
        users = json.load(f)
    
    with open("posts.json", "r", encoding = "utf-8") as f:
        posts = json.load(f)

    conn = connect_to_postgres()
    cursor = conn.cursor()

    try:
        create_table(cursor)
        insert_user(cursor, users)
        insert_posts(cursor, posts)
        conn.commit()
        logging.info("All data committed successfully.")
    
    except Exception as e:
        conn.rollback()
        logging.error(f"Transaction failed: {e}")
    
    finally:
        cursor.close()
        conn.close()
        logging.info("Database connection closed.")

if __name__ == "__main__":
    main()