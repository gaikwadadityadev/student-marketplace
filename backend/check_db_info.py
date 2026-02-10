
import sys
import os
sys.path.append(os.getcwd())
from config import Config
from sqlalchemy import create_engine, text

def check_db_info():
    print("Connecting to database...")
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        # Check existing categories
        print("\n=== EXISTING CATEGORIES ===")
        categories = conn.execute(text("SELECT DISTINCT category FROM products ORDER BY category")).fetchall()
        for cat in categories:
            print(f"  - {cat[0]}")
        
        # Check sellers
        print("\n=== EXISTING SELLERS ===")
        sellers = conn.execute(text("SELECT user_id, full_name, email FROM users LIMIT 10")).fetchall()
        for seller in sellers:
            print(f"  ID: {seller[0]}, Name: {seller[1]}, Email: {seller[2]}")
        
        # Check if Student Essentials category exists
        print("\n=== CHECKING 'Student Essentials' CATEGORY ===")
        student_essentials = conn.execute(text("SELECT COUNT(*) FROM products WHERE category = 'Student Essentials'")).fetchone()
        print(f"  Products in 'Student Essentials': {student_essentials[0]}")

if __name__ == "__main__":
    check_db_info()
