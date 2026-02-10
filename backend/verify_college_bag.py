
import sys
import os
sys.path.append(os.getcwd())
from config import Config
from sqlalchemy import create_engine, text

def verify_college_bag():
    print("Connecting to database...")
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        print("\n=== COLLEGE BAG PRODUCT DETAILS ===")
        query = text("""
            SELECT p.product_id, p.name, p.description, p.price, p.category, 
                   p.image_path, p.status, u.full_name
            FROM products p
            JOIN users u ON p.seller_id = u.user_id
            WHERE p.name LIKE '%College Bag%'
        """)
        result = conn.execute(query).fetchone()
        
        if result:
            print("\nCollege Bag Product Found!")
            print(f"Product ID: {result[0]}")
            print(f"Name: {result[1]}")
            print(f"Description: {result[2][:50]}...")
            print(f"Price: Rs. {result[3]}")
            print(f"Category: {result[4]}")
            print(f"Image Path: {result[5]}")
            print(f"Status: {result[6]}")
            print(f"Seller: {result[7]}")
            
            # Verify image file exists
            import os as filesystem
            image_path = f"static/{result[5]}"
            if filesystem.path.exists(image_path):
                size = filesystem.path.getsize(image_path)
                print(f"\nImage file exists: {image_path} ({size} bytes)")
                print("NOTE: This is a placeholder image. Replace with actual college bag image.")
            else:
                print(f"\nImage file NOT found: {image_path}")
                
        else:
            print("\nCollege Bag Product NOT Found!")
        
        print("\n=== ALL Accessories Products ===")
        cat_query = text("SELECT name, price FROM products WHERE category = 'Accessories'")
        products = conn.execute(cat_query).fetchall()
        if products:
            for p in products:
                print(f"- {p[0]} (Rs. {p[1]})")
        else:
            print("No products in this category")

if __name__ == "__main__":
    verify_college_bag()
