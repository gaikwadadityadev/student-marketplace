
import sys
import os
import traceback
sys.path.append(os.getcwd())
from config import Config
from sqlalchemy import create_engine, text

def test_insert():
    print("Connecting...")
    try:
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
        with engine.connect() as conn:
            print("Connected. Checking Schema...")
            # Check columns
            columns = conn.execute(text("SHOW COLUMNS FROM orders")).fetchall()
            col_names = [c[0] for c in columns]
            print(f"Columns: {col_names}")
            
            print("Attempting INSERT...")
            try:
                # Transact
                trans = conn.begin()
                query = text("INSERT INTO orders (buyer_id, total_amount, status) VALUES (:uid, :amt, :st)")
                result = conn.execute(query, {'uid': 1, 'amt': 100, 'st': 'pending'})
                print(f"Success! Inserted ID: {result.lastrowid}")
                trans.rollback()
                print("Rolled back.")
            except Exception as e:
                print("INSERT FAILED!")
                traceback.print_exc()
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    test_insert()
