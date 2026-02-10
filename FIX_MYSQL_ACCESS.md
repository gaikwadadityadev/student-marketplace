# How to Fix MySQL Access Denied Error

## Quick Fix Steps

### Step 1: Find Your MySQL Password

**Option A: Try logging into MySQL manually**
```bash
mysql -u root -p
```
Enter your password when prompted. If you don't know it, see Step 2.

**Option B: Check if you have no password (XAMPP/WAMP)**
- XAMPP MySQL usually has **empty password**
- Try: `mysql -u root` (without -p)

### Step 2: Create .env File

1. **Go to the `backend` folder**
2. **Create a new file named `.env`** (exactly this name, no extension)
3. **Add your MySQL credentials:**

If you have a password, use:
```env
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_PASSWORD_HERE
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=student_marketplace
SECRET_KEY=dev-secret-key-12345
```

If you have NO password (XAMPP), use:
```env
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=student_marketplace
SECRET_KEY=dev-secret-key-12345
```

### Step 3: Verify Database Exists

Open MySQL and check:
```bash
mysql -u root -p
```

Then run:
```sql
CREATE DATABASE IF NOT EXISTS student_marketplace;
USE student_marketplace;
SHOW TABLES;
```

If no tables exist, create them:
```bash
mysql -u root -p < backend/sql/schema.sql
```

### Step 4: Test Again

Try creating admin account again:
```bash
cd backend
python create_admin.py
```

## Alternative: Update config.py Directly

If .env doesn't work, edit `backend/config.py`:

Find line 17 and change:
```python
password = os.getenv('MYSQL_PASSWORD', '')  # Empty password
```

To:
```python
password = os.getenv('MYSQL_PASSWORD', 'your_password_here')  # Your password
```

## Common Scenarios

### Scenario 1: XAMPP (Usually empty password)
Use in .env:
```env
MYSQL_PASSWORD=
```

### Scenario 2: MySQL Installer (Password set during install)
Use the password you set during installation.

### Scenario 3: Forgot Password
You may need to reset MySQL root password. Search online for "reset MySQL root password Windows"

## Test MySQL Connection

Test manually:
```bash
mysql -u root -p
```

If this works, use the same password in .env file.

## Still Not Working?

1. Make sure MySQL service is running
2. Check MySQL is on port 3306
3. Try creating a new MySQL user for the app
4. Check firewall isn't blocking MySQL

