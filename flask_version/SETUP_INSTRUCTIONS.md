# Complete Setup Instructions - Student Marketplace Flask

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ MySQL 5.7 or higher installed and running
- ✅ pip (Python package manager)
- ✅ Text editor or IDE

## 🚀 Step-by-Step Setup

### Step 1: Navigate to Project Directory

```bash
cd flask_version
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Expected output:** All packages installed successfully

### Step 4: Configure Database Connection

Edit `config.py` and update MySQL credentials:

```python
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_mysql_password'  # Change this
MYSQL_HOST = '127.0.0.1'
MYSQL_DB = 'student_marketplace_flask'
```

### Step 5: Setup Database

**Option A: Using Python Script (Easiest)**

```bash
python setup_database.py
```

**Option B: Manual MySQL Commands**

```bash
# Connect to MySQL
mysql -u root -p

# Run schema
source database/schema.sql;

# Load sample data
source database/sample_products.sql;

# Exit MySQL
exit;
```

### Step 6: Create Upload Directory

```bash
# Windows
mkdir static\uploads\products

# Linux/Mac
mkdir -p static/uploads/products
```

### Step 7: Run the Application

```bash
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 8: Access the Application

Open your browser and go to: **http://localhost:5000**

## ✅ Verification Checklist

After setup, verify:

- [ ] Application runs without errors
- [ ] Home page loads correctly
- [ ] Products page shows sample products
- [ ] Can view product details
- [ ] Can login with admin credentials
- [ ] Can register new user
- [ ] Can submit a review (after login)
- [ ] Search functionality works
- [ ] Filters work correctly

## 🧪 Testing Features

### Test 1: Browse Products
1. Go to: http://localhost:5000/products
2. Should see 19 sample products
3. Products should have images, prices, ratings

### Test 2: Search
1. Enter "book" in search box
2. Should filter to show only books
3. Try searching "mouse" or "calculator"

### Test 3: Filters
1. Select "Electronics" category
2. Set price range: 500 to 1500
3. Set minimum rating: 4 stars
4. Click "Apply Filters"
5. Should show filtered results

### Test 4: Product Details
1. Click on any product
2. Should see:
   - Product images (if available)
   - Price with discount
   - Description
   - Reviews section

### Test 5: Submit Review
1. Login as student (or register new account)
2. Go to any product detail page
3. Scroll to reviews section
4. Select rating (1-5 stars)
5. Write review text
6. Click "Submit Review"
7. Review should appear immediately

### Test 6: One Review Per User
1. Try to submit another review for the same product
2. Should show error: "You have already reviewed this product"

## 🐛 Common Issues & Solutions

### Issue 1: ModuleNotFoundError
**Error:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue 2: Database Connection Error
**Error:** `Can't connect to MySQL server`

**Solutions:**
1. Check MySQL is running:
   ```bash
   # Windows
   net start MySQL
   
   # Linux/Mac
   sudo systemctl start mysql
   ```

2. Verify credentials in `config.py`
3. Check MySQL port (default: 3306)

### Issue 3: Database Doesn't Exist
**Error:** `Unknown database 'student_marketplace_flask'`

**Solution:**
```bash
python setup_database.py
# OR
mysql -u root -p < database/schema.sql
```

### Issue 4: Images Not Displaying
**Error:** Images show broken/placeholder

**Solutions:**
1. Check `static/uploads/products/` directory exists
2. Verify image paths in database
3. Check file permissions

### Issue 5: Port Already in Use
**Error:** `Address already in use`

**Solution:**
```bash
# Find and kill process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill
```

## 📊 Sample Data Included

The database includes:
- **5 Categories:** Books, Electronics, Stationery, Hostel Items, Accessories
- **19 Products:** Realistic student products with descriptions
- **1 Admin User:** admin / admin123
- **1 Student User:** student1 / student123
- **Sample Reviews:** For demonstration

## 🎯 Next Steps

After successful setup:

1. **Explore the Application**
   - Browse products
   - Test all features
   - Submit reviews

2. **Customize**
   - Add your own products
   - Modify UI colors/styles
   - Add more features

3. **Prepare for Viva**
   - Read `PROJECT_EXPLANATION.md`
   - Understand database design
   - Review code comments

## 📞 Support

If you encounter issues:
1. Check error messages in terminal
2. Review `PROJECT_EXPLANATION.md`
3. Verify all setup steps completed
4. Check MySQL is running
5. Verify file permissions

---

**Setup Complete!** 🎉

Your Student Marketplace is ready to use!
