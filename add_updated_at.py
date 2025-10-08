import psycopg2
from psycopg2 import sql

# Database connection parameters
DB_HOST = "localhost"
DB_NAME = "your_database_name"
DB_USER = "your_username"
DB_PASSWORD = "your_password"

def add_updated_at_column():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Check if the column exists
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'payments' AND column_name = 'updated_at';
        """)
        exists = cursor.fetchone()

        if not exists:
            # Add the column
            cursor.execute("""
                ALTER TABLE payments ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """)
            conn.commit()
            print("Added updated_at column to payments table.")
        else:
            print("updated_at column already exists.")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_updated_at_column()
