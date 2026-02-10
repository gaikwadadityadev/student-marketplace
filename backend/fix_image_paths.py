"""
Utility script to fix product image paths in the database
This script ensures all product image paths are correct and images exist
"""
import os
import sys
from sqlalchemy import create_engine, text
from config import Config

def fix_image_paths():
    """Fix image paths for all products"""
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
    upload_folder = Config.UPLOAD_FOLDER
    
    print("=" * 60)
    print("Product Image Path Fixer")
    print("=" * 60)
    print(f"Upload folder: {upload_folder}")
    print()
    
    try:
        with engine.connect() as conn:
            # Get all products
            query = text("SELECT product_id, name, image_path FROM products")
            products = conn.execute(query).mappings().all()
            
            if not products:
                print("No products found in database.")
                return
            
            print(f"Found {len(products)} products")
            print()
            
            fixed_count = 0
            missing_count = 0
            already_correct = 0
            
            for product in products:
                product_id = product['product_id']
                name = product['name']
                image_path = product['image_path']
                
                if not image_path:
                    print(f"⚠️  Product #{product_id} ({name}): No image path")
                    missing_count += 1
                    continue
                
                # Normalize the path - should be 'uploads/filename.jpg'
                normalized_path = image_path.replace('\\', '/')
                
                # Remove leading slash if present
                if normalized_path.startswith('/'):
                    normalized_path = normalized_path[1:]
                
                # Ensure it starts with 'uploads/'
                if not normalized_path.startswith('uploads/'):
                    if normalized_path.startswith('static/uploads/'):
                        normalized_path = normalized_path.replace('static/uploads/', 'uploads/', 1)
                    else:
                        normalized_path = f"uploads/{normalized_path}"
                
                # Extract filename
                filename = os.path.basename(normalized_path)
                full_path = os.path.join(upload_folder, filename)
                
                # Check if file exists
                if os.path.exists(full_path):
                    # Update database if path changed
                    if normalized_path != image_path:
                        update_query = text("""
                            UPDATE products 
                            SET image_path = :image_path 
                            WHERE product_id = :product_id
                        """)
                        conn.execute(update_query, {
                            'product_id': product_id,
                            'image_path': normalized_path
                        })
                        print(f"✅ Fixed: Product #{product_id} ({name})")
                        print(f"   Old: {image_path}")
                        print(f"   New: {normalized_path}")
                        fixed_count += 1
                    else:
                        already_correct += 1
                        print(f"✓ Product #{product_id} ({name}): Path is correct")
                else:
                    print(f"❌ Missing: Product #{product_id} ({name})")
                    print(f"   Expected: {full_path}")
                    print(f"   Database path: {image_path}")
                    missing_count += 1
            
            conn.commit()
            
            print()
            print("=" * 60)
            print("Summary:")
            print(f"  Fixed: {fixed_count}")
            print(f"  Already correct: {already_correct}")
            print(f"  Missing images: {missing_count}")
            print("=" * 60)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

def list_all_images():
    """List all images in uploads folder"""
    upload_folder = Config.UPLOAD_FOLDER
    print("=" * 60)
    print("Available Images in Uploads Folder")
    print("=" * 60)
    print(f"Folder: {upload_folder}")
    print()
    
    if not os.path.exists(upload_folder):
        print("Uploads folder does not exist!")
        return
    
    images = [f for f in os.listdir(upload_folder) 
              if os.path.isfile(os.path.join(upload_folder, f))]
    
    if not images:
        print("No images found in uploads folder.")
        return
    
    print(f"Found {len(images)} images:")
    for i, img in enumerate(images, 1):
        full_path = os.path.join(upload_folder, img)
        size = os.path.getsize(full_path)
        size_kb = size / 1024
        print(f"  {i}. {img} ({size_kb:.2f} KB)")
        print(f"     Path: uploads/{img}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--list':
        list_all_images()
    else:
        fix_image_paths()
        print()
        print("Run with --list to see all available images:")
        print("  python fix_image_paths.py --list")

