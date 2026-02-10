# Commands to Run Student Marketplace

## 🚀 Quick Start Commands

### Option 1: Run from Project Root (Recommended)
```bash
python backend/app.py
```

### Option 2: Run from Backend Directory
```bash
cd backend
python app.py
```

## 📋 Complete Setup Commands

### 1. Navigate to Project Directory
```bash
cd "C:\Users\adity\OneDrive\Documents\Project\Student Marketplace"
```

### 2. (Optional) Activate Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies (if not already installed)
```bash
pip install -r backend/requirements.txt
```

### 4. Fix Database Schema (First Time Only)
```bash
python backend/fix_order_status.py
```

### 5. Run the Application
```bash
python backend/app.py
```

## 🌐 Access URLs

After running the application, open in browser:

- **Home Page:** http://localhost:5000
- **Admin Login:** http://localhost:5000/admin/login
- **Student Login:** http://localhost:5000/login
- **Student Register:** http://localhost:5000/register
- **Admin Dashboard:** http://localhost:5000/admin/dashboard

## 🛑 Stop the Server

Press `CTRL + C` in the terminal where Flask is running

## 🔐 Default Admin Credentials

If you haven't created admin yet:
```bash
cd backend
python create_admin.py
```

Default values (press Enter for each):
- Username: `admin`
- Email: `admin@marketplace.com`
- Password: `admin123`
- Full Name: `Admin User`

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows - Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### Database Connection Error
- Make sure MySQL is running
- Check credentials in `backend/config.py`

### Module Not Found
```bash
pip install -r backend/requirements.txt
```

## ✅ Quick Test Checklist

1. ✅ Run: `python backend/app.py`
2. ✅ Open: http://localhost:5000
3. ✅ Login as admin
4. ✅ Test order status update
5. ✅ Verify status changes work

---

**Ready to run!** 🎉


