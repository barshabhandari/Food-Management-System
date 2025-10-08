from app.database import engine
from sqlalchemy import text

def add_missing_columns():
    with engine.connect() as conn:
        # Add transaction_id if not exists
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'payments' AND column_name = 'transaction_id';
        """))
        exists = result.fetchone()
        if not exists:
            conn.execute(text("""
                ALTER TABLE payments ADD COLUMN transaction_id VARCHAR(255);
            """))
            print("Added transaction_id column.")

        # Add updated_at if not exists
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'payments' AND column_name = 'updated_at';
        """))
        exists = result.fetchone()
        if not exists:
            conn.execute(text("""
                ALTER TABLE payments ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            """))
            print("Added updated_at column.")

        conn.commit()
        print("Columns added successfully.")

if __name__ == "__main__":
    add_missing_columns()
