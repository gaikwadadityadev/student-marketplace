"""
Test MySQL Connection Script
Run this to test your MySQL connection and find the correct password
"""
import pymysql
import sys

def test_connection(password=''):
    """Test MySQL connection with given password"""
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password=password,
            database='student_marketplace',
            connect_timeout=5
        )
        print("✅ Connection successful!")
        connection.close()
        return True
    except pymysql.err.OperationalError as e:
        if e.args[0] == 1045:
            return False  # Wrong password
        else:
            print(f"❌ Connection error: {e}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("=" * 50)
    print("MySQL Connection Tester")
    print("=" * 50)
    print()
    
    # Try empty password first
    print("Testing with empty password...")
    if test_connection(''):
        print("✅ MySQL accepts empty password!")
        print("\nCreate backend/.env file with:")
        print("MYSQL_PASSWORD=")
        return
    
    # Ask user for password
    print("❌ Empty password failed.")
    print("\nMySQL requires a password. Please enter your MySQL root password:")
    print("(Press Enter to skip and manually create .env file)")
    
    password = input("Password: ").strip()
    
    if not password:
        print("\n No password provided.")
        print("\nTo fix manually:")
        print("1. Create backend/.env file")
        print("2. Add: MYSQL_PASSWORD=your_password_here")
        print("3. Or run: mysql -u root -p to find your password")
        return
    
    # Test with provided password
    print("\nTesting connection...")
    if test_connection(password):
        print("\n Connection successful with provided password!")
        print("\nCreate backend/.env file with the following content:")
        print("-" * 50)
        print(f"MYSQL_USER=root")
        print(f"MYSQL_PASSWORD={password}")
        print(f"MYSQL_HOST=127.0.0.1")
        print(f"MYSQL_PORT=3306")
        print(f"MYSQL_DB=student_marketplace")
        print(f"SECRET_KEY=dev-secret-key-change-in-production")
        print("-" * 50)
    else:
        print("\n❌ Connection failed with provided password.")
        print("\nPossible issues:")
        print("1. Wrong password")
        print("2. MySQL server not running")
        print("3. Database 'student_marketplace' doesn't exist")
        print("\nTry:")
        print("- Check if MySQL is running")
        print("- Create database: mysql -u root -p -e 'CREATE DATABASE student_marketplace;'")
        print("- Reset MySQL root password if needed")

if __name__ == '__main__':
    main()

