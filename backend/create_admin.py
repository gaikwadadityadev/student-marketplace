"""
Helper script to create admin user with proper password hashing
Run this script to create an admin account
"""
import bcrypt
from sqlalchemy import create_engine, text
from config import Config

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_admin():
    """Create admin user"""
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
    
    username = input("Enter admin username (default: admin): ").strip() or "admin"
    email = input("Enter admin email (default: admin@marketplace.com): ").strip() or "admin@marketplace.com"
    password = input("Enter admin password (default: admin123): ").strip() or "admin123"
    full_name = input("Enter admin full name (default: Admin User): ").strip() or "Admin User"
    
    hashed_password = hash_password(password)
    
    try:
        with engine.connect() as conn:
            # Check if admin already exists
            check_query = text("SELECT user_id FROM users WHERE username = :username OR email = :email")
            existing = conn.execute(check_query, {'username': username, 'email': email}).mappings().first()
            
            if existing:
                print(f"User with username '{username}' or email '{email}' already exists!")
                update = input("Do you want to update the password? (y/n): ").strip().lower()
                if update == 'y':
                    update_query = text("""
                        UPDATE users 
                        SET password = :password, role = 'admin', status = 'active'
                        WHERE username = :username
                    """)
                    conn.execute(update_query, {'username': username, 'password': hashed_password})
                    conn.commit()
                    print(f"Admin user '{username}' password updated successfully!")
                return
            
            # Insert new admin
            insert_query = text("""
                INSERT INTO users (username, email, password, full_name, role, status)
                VALUES (:username, :email, :password, :full_name, 'admin', 'active')
            """)
            conn.execute(insert_query, {
                'username': username,
                'email': email,
                'password': hashed_password,
                'full_name': full_name
            })
            conn.commit()
            print(f"Admin user '{username}' created successfully!")
            print(f"Username: {username}")
            print(f"Password: {password}")
    except Exception as e:
        print(f"Error creating admin: {e}")

if __name__ == '__main__':
    print("=" * 50)
    print("Student Marketplace - Admin User Creator")
    print("=" * 50)
    create_admin()

