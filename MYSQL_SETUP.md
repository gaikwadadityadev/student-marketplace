# MySQL Setup Guide - Fixing Access Denied Error

## Problem
You're getting: `Access denied for user 'root'@'localhost' (using password: NO)`

This means MySQL is expecting a password, but the application is trying to connect without one.

## Solution Options

### Option 1: Create .env File (Recommended)

1. **Create a `.env` file** in the `backend` folder:
   ```
   backend/.env
   ```

2. **Add your MySQL credentials** to the file:
   ```env
   MYSQL_USER=root
   MYSQL_PASSWORD=your_actual_mysql_password
   MYSQL_HOST=127.0.0.1
   MYSQL_PORT=3306
   MYSQL_DB=student_marketplace
   SECRET_KEY=your-secret-key-here
   ```

3. **Replace `your_actual_mysql_password`** with your actual MySQL root password.

### Option 2: Update config.py Directly

Edit `backend/config.py` and change line 17:
```python
password = os.getenv('MYSQL_PASSWORD', 'your_mysql_password_here')
```

### Option 3: Find Your MySQL Password

If you don't remember your MySQL password:

**Windows:**
1. Open MySQL Command Line Client
2. Try logging in - it might prompt for password
3. Or check if password is stored in MySQL configuration

**Reset MySQL Password (if needed):**
1. Stop MySQL service
2. Start MySQL in safe mode
3. Reset the password
4. Restart MySQL service

### Option 4: Test MySQL Connection

Test if MySQL is running and accessible:

```bash
mysql -u root -p
```

Enter your password when prompted. If this works, use the same password in the `.env` file.

## Step-by-Step Fix

### Step 1: Find Your MySQL Password

Try logging into MySQL:
```bash
mysql -u root -p
```

If you don't know the password, you may need to:
- Check if you set one during MySQL installation
- Check MySQL configuration files
- Reset the password

### Step 2: Create .env File

1. Go to the `backend` folder
2. Create a new file named `.env` (no extension)
3. Add the following content (replace with your actual password):

```env
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_PASSWORD_HERE
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=student_marketplace
SECRET_KEY=dev-secret-key-12345
```

### Step 3: Verify Database Exists

Make sure the database exists:
```bash
mysql -u root -p
```

Then in MySQL:
```sql
CREATE DATABASE IF NOT EXISTS student_marketplace;
USE student_marketplace;
SHOW TABLES;
```

If tables don't exist, run:
```bash
mysql -u root -p < backend/sql/schema.sql
```

### Step 4: Test the Connection

Try running the admin creation script again:
```bash
python backend/create_admin.py
```

## Common MySQL Password Scenarios

### Scenario 1: No Password Set
If MySQL was installed without a password, you might need to set one:
```sql
ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
```

### Scenario 2: XAMPP/WAMP
If using XAMPP or WAMP, the default might be:
- **XAMPP**: Usually empty password (but might need to be set)
- **WAMP**: Usually empty password

Try with empty password first in `.env`:
```env
MYSQL_PASSWORD=
```

### Scenario 3: MySQL Installer
If installed via MySQL Installer, you set a password during installation. Use that password.

## Quick Fix Script

Create a file `backend/test_mysql.py`:

```python
import pymysql

try:
    # Try with no password
    connection = pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='student_marketplace'
    )
    print("✅ Connected with empty password")
    connection.close()
except:
    print("❌ Empty password failed. You need to set your MySQL password in .env file")
    print("Password prompt: Enter your MySQL root password:")
    password = input()
    try:
        connection = pymysql.connect(
            host='127.0.0.1',
            user='root',
            password=password,
            database='student_marketplace'
        )
        print("✅ Connection successful!")
        print(f"Add this to backend/.env: MYSQL_PASSWORD={password}")
        connection.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")
```

## After Fixing

Once you've set up the `.env` file:

1. **Create the database** (if not exists):
   ```bash
   mysql -u root -p < backend/sql/schema.sql
   ```

2. **Create admin account**:
   ```bash
   python backend/create_admin.py
   ```

3. **Run the Flask app**:
   ```bash
   python backend/app.py
   ```

## Still Having Issues?

1. **Check MySQL is running:**
   - Windows: Services → MySQL
   - Or: `net start MySQL` (if installed as service)

2. **Check MySQL version:**
   ```bash
   mysql --version
   ```

3. **Check if database exists:**
   ```sql
   SHOW DATABASES;
   ```

4. **Try different user:**
   If root doesn't work, create a new MySQL user:
   ```sql
   CREATE USER 'marketplace_user'@'localhost' IDENTIFIED BY 'password123';
   GRANT ALL PRIVILEGES ON student_marketplace.* TO 'marketplace_user'@'localhost';
   FLUSH PRIVILEGES;
   ```
   
   Then use in `.env`:
   ```env
   MYSQL_USER=marketplace_user
   MYSQL_PASSWORD=password123
   ```

