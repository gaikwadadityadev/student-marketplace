# Quick Start Guide - Student Marketplace

## ✅ Step 1: Application is Running!

Your Flask application is now running at:
- **Local URL:** http://127.0.0.1:5000
- **Network URL:** http://172.22.239.129:5000

## 📝 Step 2: Open in Browser

1. Open your web browser (Chrome, Firefox, Edge, etc.)
2. Go to: **http://127.0.0.1:5000** or **http://localhost:5000**
3. You should see the **Student Marketplace** home page

## 👤 Step 3: Create Admin Account

Before you can manage the system, you need to create an admin account:

### Option A: Using Python Script (Recommended)
1. Open a **NEW terminal/command prompt** (keep the Flask server running)
2. Navigate to the project directory
3. Run:
   ```bash
   cd backend
   python create_admin.py
   ```
4. Follow the prompts:
   - Username: `admin` (or press Enter for default)
   - Email: `admin@marketplace.com` (or press Enter)
   - Password: `admin123` (or press Enter)
   - Full Name: `Admin User` (or press Enter)

### Option B: Through Web Interface
1. Go to: http://127.0.0.1:5000/register
2. Register a new account
3. Then update the role in MySQL:
   ```sql
   mysql -u root -p
   USE student_marketplace;
   UPDATE users SET role='admin' WHERE username='your_username';
   ```

## 🎯 Step 4: Test the Application

### A. Test as Admin
1. Go to: **http://127.0.0.1:5000/admin/login**
2. Login with admin credentials
3. You'll see the Admin Dashboard with:
   - Statistics
   - Pending products (if any)
   - User management

### B. Test as Student
1. Go to: **http://127.0.0.1:5000/register**
2. Register a new student account
3. Login at: **http://127.0.0.1:5000/login**
4. Try these features:
   - Upload a product (Dashboard → Sell Product)
   - Browse products (Products menu)
   - Add products to cart
   - Place an order

### C. Complete the Flow
1. **Student 1:**
   - Register and login
   - Upload a product (it will be "pending")
   
2. **Admin:**
   - Login to admin panel
   - Go to Admin Dashboard
   - Approve the product
   
3. **Student 2:**
   - Register a different account
   - Browse products (should see approved product)
   - Add to cart and checkout

## 🔍 Step 5: Verify Database

If you want to check the database:

```bash
mysql -u root -p
USE student_marketplace;
SHOW TABLES;
SELECT * FROM users;
SELECT * FROM products;
```

## 📱 Step 6: Access from Other Devices

If you want to access from another device on the same network:
- Use: **http://172.22.239.129:5000**
- Make sure firewall allows port 5000

## ⚠️ Important Notes

1. **Keep the terminal running** - Don't close the terminal where Flask is running
2. **Database must be running** - MySQL server should be active
3. **First time setup** - Make sure you've run the database schema:
   ```bash
   mysql -u root -p < backend/sql/schema.sql
   ```

## 🐛 Troubleshooting

### Can't access the website?
- Check if Flask is still running in terminal
- Try: http://localhost:5000 instead
- Check firewall settings

### Database connection error?
- Make sure MySQL is running
- Check credentials in `backend/config.py`
- Verify database exists: `SHOW DATABASES;`

### Admin login not working?
- Make sure you created admin account using `create_admin.py`
- Check if account exists: `SELECT * FROM users WHERE role='admin';`

## 📚 Next Steps

1. **Add Sample Products:**
   - Register multiple student accounts
   - Upload various products
   - Test search and filtering

2. **Customize:**
   - Update colors/branding in `static/css/style.css`
   - Modify templates in `templates/` folder
   - Add more product categories

3. **Explore Features:**
   - Product management (CRUD)
   - Shopping cart
   - Order placement
   - Admin approvals

## 🎉 You're All Set!

Your Student Marketplace is now running and ready to use!

For detailed documentation, see:
- `README.md` - Full documentation
- `SETUP_GUIDE.md` - Detailed setup instructions
- `SRS.md` - Requirements specification

