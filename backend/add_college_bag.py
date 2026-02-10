
import sys
import os
sys.path.append(os.getcwd())
from config import Config
from sqlalchemy import create_engine, text

def add_college_bag():
    print("Connecting to database...")
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        # First, delete any existing college bag products
        print("Removing any existing college bag products...")
        delete_query = text("DELETE FROM products WHERE name LIKE '%College Bag%'")
        result = conn.execute(delete_query)
        print(f"   Removed {result.rowcount} existing college bag product(s)")
        
        product = {
            'seller_id': 1,
            'name': 'College Bag',
            'description': 'Durable and lightweight college bag suitable for daily student use. Enough space for books, laptop, and accessories.',
            'price': 500,
            'category': 'Accessories',
            'image_path': 'uploads/college_bag.png',
            'status': 'approved'
        }
        
        print("Inserting College Bag Product...")
        insert_query = text("""
            INSERT INTO products (seller_id, name, description, price, category, image_path, status)
            VALUES (:seller_id, :name, :description, :price, :category, :image_path, :status)
        """)
        
        conn.execute(insert_query, product)
        conn.commit()
        print("College Bag Product Added Successfully!")
        print(f"   Name: {product['name']}")
        print(f"   Price: Rs. {product['price']}")
        print(f"   Category: {product['category']}")

if __name__ == "__main__":
    add_college_bag()
