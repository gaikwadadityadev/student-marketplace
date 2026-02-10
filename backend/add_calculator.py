
import sys
import os
sys.path.append(os.getcwd())
from config import Config
from sqlalchemy import create_engine, text

def add_calculator():
    print("Connecting to database...")
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        # First, delete any existing calculator products
        print("Removing any existing calculator products...")
        delete_query = text("DELETE FROM products WHERE name LIKE '%Calculator%'")
        result = conn.execute(delete_query)
        print(f"   Removed {result.rowcount} existing calculator product(s)")
        
        product = {
            'seller_id': 1,
            'name': 'Scientific Calculator',
            'description': 'A scientific calculator suitable for BSc and engineering students. Supports mathematical and scientific calculations useful for exams and assignments.',
            'price': 500,
            'category': 'Student Essentials',
            'image_path': 'uploads/calculator.png',
            'status': 'approved'
        }
        
        print("Inserting Calculator Product...")
        insert_query = text("""
            INSERT INTO products (seller_id, name, description, price, category, image_path, status)
            VALUES (:seller_id, :name, :description, :price, :category, :image_path, :status)
        """)
        
        conn.execute(insert_query, product)
        conn.commit()
        print("✅ Calculator Product Added Successfully!")
        print(f"   Name: {product['name']}")
        print(f"   Price: ₹{product['price']}")
        print(f"   Category: {product['category']}")

if __name__ == "__main__":
    add_calculator()
