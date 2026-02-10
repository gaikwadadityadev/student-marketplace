"""
Script to check book product image paths
"""
from sqlalchemy import create_engine, text

# Database connection
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Aditya%4008@127.0.0.1:3306/student_marketplace'
engine = create_engine(SQLALCHEMY_DATABASE_URI)

with engine.connect() as conn:
    # Get book products
    query = text("""
        SELECT product_id, name, category, image_path, status
        FROM products 
        WHERE category = 'Books & Notes' 
        OR name LIKE '%Data Structure%'
        OR name LIKE '%Algorithm%'
        LIMIT 10
    """)
    
    results = conn.execute(query).mappings().all()
    
    print(f"\nFound {len(results)} book products:\n")
    print("-" * 100)
    
    for r in results:
        print(f"ID: {r['product_id']}")
        print(f"Name: {r['name']}")
        print(f"Category: {r['category']}")
        print(f"Image Path: {r['image_path']}")
        print(f"Status: {r['status']}")
        print("-" * 100)
