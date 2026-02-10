# Quick Start Guide - Student Marketplace Flask

## 🚀 Quick Setup (5 Steps)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Database
```bash
# Option A: Using Python script (Recommended)
python setup_database.py

# Option B: Manual MySQL
mysql -u root -p < database/schema.sql
mysql -u root -p < database/sample_products.sql
```

### 3. Configure Database
Edit `config.py` and update your MySQL password:
```python
MYSQL_PASSWORD = 'your_password'
```

### 4. Create Upload Directory
```bash
mkdir -p static/uploads/products
```

### 5. Run Application
```bash
python app.py
```

## 🌐 Access URLs

- **Home:** http://localhost:5000
- **Products:** http://localhost:5000/products
- **Login:** http://localhost:5000/login
- **Register:** http://localhost:5000/register

## 🔐 Login Credentials

**Admin:**
- Username: `admin`
- Password: `admin123`

**Student:**
- Username: `student1`
- Password: `student123`

## ✅ Test Features

1. **Browse Products** - View all products with filters
2. **Search** - Search by product name
3. **View Details** - Click any product to see details
4. **Image Gallery** - Click thumbnails to change main image
5. **Submit Review** - Login and write a review (one per product)
6. **Filters** - Filter by category, price, rating

## 🎯 Key Features

✅ Multiple product images  
✅ Reviews & ratings (1-5 stars)  
✅ Average rating calculation  
✅ One review per user  
✅ Search functionality  
✅ Filter by category, price, rating  
✅ Sort by price, rating, newest  
✅ Responsive design  
✅ Secure authentication  

---

**Ready to use!** 🎉
