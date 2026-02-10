# Student Marketplace - Flask Version

A complete e-commerce platform for students built with Python Flask, featuring Flipkart-like functionalities.

## 🎯 Project Overview

**Final Year Project** - Student Marketplace  
**Tech Stack:** Python Flask, MySQL, HTML, CSS, JavaScript, Bootstrap 5

## ✨ Features Implemented

### 1. Product Management
- ✅ Multiple images per product (Flipkart-style gallery)
- ✅ Price with discount calculation
- ✅ Category-based organization
- ✅ Stock quantity tracking
- ✅ Detailed product descriptions

### 2. Flipkart-like Functionalities
- ✅ Product listing page with grid layout
- ✅ Product detail page with image gallery
- ✅ Image slider/thumbnail navigation
- ✅ Product reviews & ratings (1-5 stars)
- ✅ Average rating calculation
- ✅ One review per user per product (enforced)
- ✅ Search products by name
- ✅ Filter by category, price range, rating
- ✅ Sort by price, rating, newest

### 3. User System
- ✅ User registration & login
- ✅ Session-based authentication
- ✅ Only logged-in users can add reviews
- ✅ Secure password hashing (bcrypt)

### 4. Backend Security
- ✅ Prepared statements (SQL injection prevention)
- ✅ Secure image upload handling
- ✅ Input validation and sanitization
- ✅ Password hashing

### 5. UI/UX
- ✅ Clean & modern design (Flipkart-inspired)
- ✅ Fully responsive layout
- ✅ Student-friendly interface
- ✅ Smooth animations and transitions

## 📁 Project Structure

```
flask_version/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── requirements.txt        # Python dependencies
├── database/
│   ├── schema.sql         # Database schema
│   └── sample_products.sql # Sample products data
├── templates/
│   ├── base.html          # Base template
│   ├── index.html         # Home page
│   ├── products.html       # Product listing
│   ├── product_detail.html # Product detail page
│   ├── login.html         # Login page
│   └── register.html      # Registration page
└── static/
    ├── css/
    │   └── style.css      # Custom styles
    ├── js/
    │   └── main.js        # JavaScript functions
    └── uploads/
        └── products/       # Product images
```

## 🚀 Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Database Setup

1. **Create Database:**
```bash
mysql -u root -p < database/schema.sql
```

2. **Load Sample Products:**
```bash
mysql -u root -p < database/sample_products.sql
```

### Step 3: Configure Database

Edit `config.py` and update MySQL credentials:
```python
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_HOST = '127.0.0.1'
MYSQL_DB = 'student_marketplace_flask'
```

### Step 4: Create Upload Directory

```bash
mkdir -p static/uploads/products
```

### Step 5: Run Application

```bash
python app.py
```

The application will run on: **http://localhost:5000**

## 🔐 Default Credentials

**Admin:**
- Username: `admin`
- Password: `admin123`

**Student:**
- Username: `student1`
- Password: `student123`

## 📊 Database Schema

### Tables Created:
1. **users** - User accounts (students & admin)
2. **categories** - Product categories
3. **products** - Product information
4. **product_images** - Multiple images per product
5. **product_reviews** - Reviews and ratings (one per user per product)

### Key Features:
- Foreign key constraints for data integrity
- Unique constraints (username, email, product_slug)
- Indexes for performance
- ENUM types for status fields

## 🎨 Key Features Explained

### 1. Multiple Product Images
- Each product can have up to 5 images
- One primary image (displayed first)
- Thumbnail navigation on detail page
- Image gallery with click-to-view

### 2. Reviews & Ratings System
- Users can rate products 1-5 stars
- One review per user per product (enforced by UNIQUE constraint)
- Average rating calculated automatically
- Rating distribution shown on detail page
- Only logged-in users can review

### 3. Search & Filters
- Search by product name or description
- Filter by category
- Filter by price range (min-max)
- Filter by minimum rating
- Sort by: newest, price (low-high), price (high-low), rating

### 4. Security Features
- Password hashing with bcrypt
- Prepared statements (SQL injection prevention)
- Input validation and sanitization
- File upload validation
- Session-based authentication

## 🧪 Testing the Application

1. **View Products:**
   - Go to: http://localhost:5000/products
   - Test search and filters

2. **View Product Details:**
   - Click on any product
   - View image gallery
   - See reviews and ratings

3. **Submit Review:**
   - Login as student
   - Go to product detail page
   - Write a review (one per product)

4. **Test Filters:**
   - Filter by category
   - Set price range
   - Filter by rating
   - Sort products

## 📝 Code Quality

- ✅ Well-commented code (suitable for viva)
- ✅ Clean code structure
- ✅ Error handling
- ✅ Security best practices
- ✅ Responsive design
- ✅ Beginner-friendly

## 🎓 Viva Preparation

### Key Points to Explain:

1. **Database Design:**
   - Why separate tables for images and reviews
   - UNIQUE constraint for one review per user
   - Foreign key relationships

2. **Security:**
   - Password hashing (bcrypt)
   - Prepared statements (SQL injection prevention)
   - Input validation

3. **Features:**
   - How average rating is calculated
   - How filters work (SQL queries)
   - Image upload handling

4. **Flask Concepts:**
   - Routes and decorators
   - Session management
   - Template inheritance
   - Static files

## 🐛 Troubleshooting

### Database Connection Error
- Check MySQL is running
- Verify credentials in `config.py`
- Ensure database exists

### Images Not Displaying
- Check `static/uploads/products/` directory exists
- Verify file permissions
- Check image paths in database

### Module Not Found
```bash
pip install -r requirements.txt
```

## 📚 Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Bootstrap 5: https://getbootstrap.com/
- SQLAlchemy: https://www.sqlalchemy.org/

## 👨‍💻 Author

Final Year Project - Student Marketplace

---

**Note:** This is a development version. For production, add:
- Error logging
- Email notifications
- Payment gateway integration
- Admin panel enhancements
- Cart and checkout functionality
