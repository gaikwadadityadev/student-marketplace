"""
Database Setup Script
Run this script to set up the database and load sample data
"""

import mysql.connector
from config import Config
import os

def setup_database():
    """Set up database and load sample data"""
    print("=" * 60)
    print("Student Marketplace - Database Setup")
    print("=" * 60)
    
    try:
        # Connect to MySQL (without database)
        conn = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            port=int(Config.MYSQL_PORT)
        )
        cursor = conn.cursor()
        
        # Read and execute schema.sql
        print("\n[1/2] Creating database and tables...")
        schema_path = os.path.join(os.path.dirname(__file__), 'database', 'schema.sql')
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            # Split by semicolon and execute each statement
            for statement in schema_sql.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            conn.commit()
        
        print("✅ Database schema created successfully!")
        
        # Read and execute sample_products.sql
        print("\n[2/2] Loading sample products...")
        sample_path = os.path.join(os.path.dirname(__file__), 'database', 'sample_products.sql')
        
        with open(sample_path, 'r', encoding='utf-8') as f:
            sample_sql = f.read()
            for statement in sample_sql.split(';'):
                if statement.strip():
                    cursor.execute(statement)
            conn.commit()
        
        print("✅ Sample products loaded successfully!")
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("✅ Database setup complete!")
        print("=" * 60)
        print("\nYou can now run the Flask application:")
        print("  python app.py")
        print("\nDefault credentials:")
        print("  Admin: admin / admin123")
        print("  Student: student1 / student123")
        
    except mysql.connector.Error as e:
        print(f"\n❌ Database error: {e}")
        print("\nPlease check:")
        print("  1. MySQL is running")
        print("  2. Credentials in config.py are correct")
        print("  3. You have permission to create databases")
    except FileNotFoundError as e:
        print(f"\n❌ File not found: {e}")
        print("Make sure schema.sql and sample_products.sql exist in database/ folder")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    setup_database()
