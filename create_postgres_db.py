import psycopg2
from psycopg2 import sql

def create_database():
    # Database configuration
    ENGINE = "django.db.backends.postgresql"
    DATABASE_NAME = "postgres_private"
    DB_USERNAME = "postgres"
    DB_PASSWORD = "postgres"
    HOST_NAME = "localhost"
    
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            dbname="postgres", user=DB_USERNAME, password=DB_PASSWORD, host=HOST_NAME
        )
        conn.autocommit = True
        
        # Create a cursor
        cur = conn.cursor()
        
        # Create the database
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DATABASE_NAME)))
        print(f"Database '{DATABASE_NAME}' created successfully.")
        
        # Close the cursor and connection
        cur.close()
        conn.close()
    
    except Exception as e:
        print(f"Failed to create database. Error: {e}")

if __name__ == "__main__":
    create_database()
