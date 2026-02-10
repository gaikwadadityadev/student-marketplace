
import sys
import os
sys.path.append(os.getcwd())
from config import Config
from sqlalchemy import create_engine, text

def diagnose_images():
    print("=== IMAGE DIAGNOSTIC REPORT ===\n")
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
    with engine.connect() as conn:
        query = text("""
            SELECT product_id, name, category, image_path, status
            FROM products
            WHERE name IN ('Scientific Calculator', 'College Bag')
            ORDER BY name
        """)
        results = conn.execute(query).fetchall()
        
        if results:
            for row in results:
                print(f"Product: {row[1]}")
                print(f"  ID: {row[0]}")
                print(f"  Category: {row[2]}")
                print(f"  DB Image Path: '{row[3]}'")
                print(f"  Status: {row[4]}")
                
                # Check if file exists
                if row[3]:
                    # Try multiple possible paths
                    paths_to_check = [
                        f"static/{row[3]}",
                        f"static/uploads/{os.path.basename(row[3])}",
                        f"{row[3]}"
                    ]
                    
                    file_found = False
                    for path in paths_to_check:
                        if os.path.exists(path):
                            size = os.path.getsize(path)
                            print(f"  File Found: YES at {path} ({size} bytes)")
                            file_found = True
                            break
                    
                    if not file_found:
                        print(f"  File Found: NO")
                        print(f"  Searched: {paths_to_check}")
                else:
                    print("  Error: No image_path in database!")
                print()
        else:
            print("ERROR: No products found!\n")
        
        # Show actual files in uploads directory
        print("=== FILES IN static/uploads ===")
        upload_dir = "static/uploads"
        if os.path.exists(upload_dir):
            all_files = os.listdir(upload_dir)
            relevant_files = [f for f in all_files if 'calc' in f.lower() or 'bag' in f.lower() or 'college' in f.lower()]
            for f in relevant_files:
                full_path = os.path.join(upload_dir, f)
                size = os.path.getsize(full_path)
                print(f"  {f} ({size} bytes)")
        else:
            print("  ERROR: uploads directory not found!")
        
        print("\n=== RECOMMENDATION ===")
        print("If images exist but aren't showing:")
        print("1. Check Flask app is serving /static/ URL correctly")
        print("2. Verify browser console for 404 errors")
        print("3. Restart Flask server")

if __name__ == "__main__":
    diagnose_images()
