import psycopg2

# Database connection parameters - update these with your actual values
DB_HOST = "localhost"
DB_NAME = "annapurna"  # or your DB name
DB_USER = "your_username"
DB_PASSWORD = "your_password"

def add_columns():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        # Add transaction_id if not exists
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'payments' AND column_name = 'transaction_id';
        """)
        exists = cursor.fetchone()
        if not exists:
            cursor.execute("""
                ALTER TABLE payments ADD COLUMN transaction_id VARCHAR(255);
            """)
            print("Added transaction_id column.")

        # Add updated_at if not exists
        cursor.execute("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'payments' AND column_name = 'updated_at';
        """)
        exists = cursor.fetchone()
        if not exists:
            cursor.execute("""
                ALTER TABLE payments ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """)
            print("Added updated_at column.")

        conn.commit()
        cursor.close()
        conn.close()
        print("Columns added successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_columns()
