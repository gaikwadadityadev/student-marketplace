# Student Marketplace - Quick Command Reference

## 🚀 Commands to Run the Website

### ✅ MAIN COMMAND (Run This Now!)
```bash
python backend/app.py
```

### Alternative: Run from Backend Directory
```bash
cd backend
python app.py
```

**The website will be available at:** http://localhost:5000

**To stop the server:** Press `CTRL + C` in the terminal

### First Time Setup (If Needed)

1. **Fix Database Schema (Order Status):**
   ```bash
   python backend/fix_order_status.py
   ```

2. **Create Admin Account:**
   ```bash
   cd backend
   python create_admin.py
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r backend/requirements.txt
   ```

---

## 🔐 Commands to Reset Admin Details

### Method 1: Using Python Script (Recommended)
```bash
cd backend
python create_admin.py
```

**Follow the prompts:**
- Username: `admin` (or press Enter for default)
- Email: `admin@marketplace.com` (or press Enter for default)
- Password: Enter your new password (or press Enter for default `admin123`)
- Full Name: `Admin User` (or press Enter for default)

**If admin already exists:**
- The script will ask: "Do you want to update the password? (y/n)"
- Type `y` and press Enter to reset the password

### Method 2: Reset Admin via MySQL (Alternative)

1. **Connect to MySQL:**
```bash
mysql -u root -p
```

2. **Select database and update admin:**
```sql
USE student_marketplace;
UPDATE users SET password = 'new_hashed_password', role = 'admin', status = 'active' WHERE username = 'admin';
```

**Note:** For Method 2, you need to hash the password first using bcrypt. Method 1 is easier as it handles hashing automatically.

---

## 📋 Complete Setup Commands (First Time)

### 1. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 2. Set Up Database (if not done)
```bash
mysql -u root -p student_marketplace < backend/sql/schema.sql
```

### 3. Create Admin Account
```bash
cd backend
python create_admin.py
```

### 4. Run the Website
```bash
python backend/app.py
```

---

## 🌐 Access URLs

- **Home Page:** http://localhost:5000
- **Admin Login:** http://localhost:5000/admin/login
- **Student Login:** http://localhost:5000/login
- **Student Register:** http://localhost:5000/register
- **Admin Dashboard:** http://localhost:5000/admin/dashboard

---

## 🔄 Quick Reset Admin Command (One-Liner)

```bash
cd backend && python create_admin.py
```

Just press Enter for all prompts to use defaults:
- Username: `admin`
- Email: `admin@marketplace.com`
- Password: `admin123`
- Full Name: `Admin User`

Or enter custom values when prompted.

---

## ⚠️ Important Notes

1. **MySQL must be running** before starting the Flask app
2. **Keep the terminal open** while the website is running
3. **Default admin credentials** (if using defaults):
   - Username: `admin`
   - Password: `admin123`
4. **Database connection** is configured in `backend/config.py`
5. **Virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

---

## 🖼️ Fix Product Image Paths

### Fix Image Paths in Database
```bash
cd backend
python fix_image_paths.py
```

### List All Available Images
```bash
cd backend
python fix_image_paths.py --list
```

This will:
- Check all product image paths
- Fix incorrect paths automatically
- Report missing images
- Normalize path formats

See `IMAGE_SETUP_GUIDE.md` for detailed information.

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill process on port 5000 (Windows)
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Database Connection Error
- Check MySQL is running
- Verify credentials in `backend/config.py`
- Ensure database exists: `mysql -u root -p -e "SHOW DATABASES;"`

### Module Not Found
```bash
pip install -r backend/requirements.txt
```

### Images Not Displaying
```bash
# Fix image paths
cd backend
python fix_image_paths.py

# Check if images exist
ls static/uploads/
```

