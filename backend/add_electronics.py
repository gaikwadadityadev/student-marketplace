
import sys
import os
sys.path.append(os.getcwd())
from config import Config
from sqlalchemy import create_engine, text

def add_electronics():
    print("Connecting...")
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        products = [
            {
                'seller_id': 1,
                'name': 'Used Laptop (Dell Latitude)',
                'description': 'Good condition Dell Latitude laptop. i5 processor, 8GB RAM, 256GB SSD. Perfect for coding.',
                'price': 18500,
                'category': 'Electronics',
                'image_path': 'uploads/elec_laptop.png',
                'status': 'approved'
            },
            {
                'seller_id': 1,
                'name': 'Wireless Optical Mouse',
                'description': 'Smooth wireless mouse with USB receiver. Battery included. Works on all surfaces.',
                'price': 350,
                'category': 'Electronics',
                'image_path': 'uploads/elec_mouse.png',
                'status': 'approved'
            },
            {
                'seller_id': 1,
                'name': 'Standard USB Keyboard',
                'description': 'Durable USB keyboard with comfortable keys. Ideal for long typing sessions.',
                'price': 450,
                'category': 'Electronics',
                'image_path': 'uploads/elec_keyboard.png',
                'status': 'approved'
            },
            {
                'seller_id': 1,
                'name': '32GB Pendrive',
                'description': 'Fast USB 3.0 Pendrive. 32GB storage for your projects and notes.',
                'price': 400,
                'category': 'Electronics',
                'image_path': 'uploads/elec_pendrive.png',
                'status': 'approved'
            },
            {
                'seller_id': 1,
                'name': 'Wired Headphones (with Mic)',
                'description': 'Clear sound quality with noise cancellation mic. Great for online classes and music.',
                'price': 650,
                'category': 'Electronics',
                'image_path': 'uploads/elec_headphones.png',
                'status': 'approved'
            }
        ]
        
        print("Inserting Electronics Products...")
        insert_query = text("""
            INSERT INTO products (seller_id, name, description, price, category, image_path, status)
            VALUES (:seller_id, :name, :description, :price, :category, :image_path, :status)
        """)
        
        for p in products:
            conn.execute(insert_query, p)
            
        conn.commit()
        print("✅ Electronics Products Added Successfully!")

if __name__ == "__main__":
    add_electronics()
