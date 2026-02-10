# Student Marketplace - Project Explanation
## For Final Year Project Viva

## 📋 Project Overview

**Project Name:** Student Marketplace  
**Technology:** Python Flask, MySQL, HTML, CSS, JavaScript, Bootstrap 5  
**Type:** E-commerce Web Application

## 🎯 Problem Statement

Students need a platform to buy and sell products like books, electronics, stationery, and hostel items within their campus community. This project provides a Flipkart-like e-commerce solution specifically designed for students.

## 🏗️ System Architecture

### Frontend (Client-Side)
- **HTML5** - Structure and content
- **CSS3** - Styling and layout (Flipkart-inspired design)
- **JavaScript** - Interactive features and AJAX
- **Bootstrap 5** - Responsive framework

### Backend (Server-Side)
- **Python Flask** - Web framework
- **MySQL** - Database management
- **SQLAlchemy** - Database ORM/connection

### Database
- **MySQL** - Relational database
- **5 Main Tables:** users, categories, products, product_images, product_reviews

## 📊 Database Design

### 1. Users Table
**Purpose:** Store student and admin accounts

**Key Fields:**
- `user_id` - Primary key
- `username` - Unique identifier
- `email` - Unique email
- `password` - Hashed password (bcrypt)
- `role` - student or admin
- `status` - active or blocked

**Why this design?**
- Separate roles for students and admin
- Status field for account management
- Unique constraints prevent duplicate accounts

### 2. Categories Table
**Purpose:** Organize products into categories

**Key Fields:**
- `category_id` - Primary key
- `category_name` - Display name
- `category_slug` - URL-friendly identifier

**Why this design?**
- Normalized design (prevents data duplication)
- Easy to add new categories
- Slug used in URLs for SEO

### 3. Products Table
**Purpose:** Store product information

**Key Fields:**
- `product_id` - Primary key
- `product_name` - Product title
- `product_slug` - URL-friendly identifier
- `price` - Original price
- `discount_percent` - Discount percentage
- `discounted_price` - Final price (calculated)
- `stock_quantity` - Available stock
- `status` - pending/approved/rejected

**Why this design?**
- Separate price fields for discount calculation
- Stock tracking prevents overselling
- Status for admin approval workflow

### 4. Product Images Table
**Purpose:** Store multiple images per product

**Key Fields:**
- `image_id` - Primary key
- `product_id` - Foreign key to products
- `image_path` - File path
- `is_primary` - Flag for main image
- `image_order` - Display order

**Why this design?**
- Separate table allows multiple images (Flipkart-style)
- Primary flag identifies main image
- Order field controls image sequence

### 5. Product Reviews Table
**Purpose:** Store user reviews and ratings

**Key Fields:**
- `review_id` - Primary key
- `product_id` - Foreign key
- `user_id` - Foreign key
- `rating` - 1 to 5 stars
- `review_text` - Review content
- `UNIQUE(user_id, product_id)` - One review per user per product

**Why this design?**
- UNIQUE constraint enforces one review per user
- Rating stored as integer (1-5)
- Status field for moderation

## 🔐 Security Features

### 1. Password Security
```python
# Password hashing using bcrypt
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
```
**Why:** Prevents plain text password storage. Even if database is compromised, passwords are safe.

### 2. SQL Injection Prevention
```python
# Using prepared statements
query = text("SELECT * FROM users WHERE username = :username")
result = conn.execute(query, {'username': username})
```
**Why:** Parameters are escaped automatically. Prevents SQL injection attacks.

### 3. Input Validation
- All user inputs are sanitized
- File uploads validated (type, size)
- Email format validation
- Rating range validation (1-5)

### 4. Session Management
- Session-based authentication
- Session timeout
- Secure session storage

## 🎨 Key Features Implementation

### 1. Multiple Product Images

**How it works:**
1. Product can have multiple images (up to 5)
2. One image marked as primary (displayed first)
3. Thumbnails shown below main image
4. Click thumbnail to change main image

**Code Location:**
- Database: `product_images` table
- Frontend: `product_detail.html` (image gallery)
- JavaScript: `changeMainImage()` function

**Why this approach:**
- Separate table allows flexibility
- Primary flag identifies main image
- JavaScript handles image switching

### 2. Reviews & Ratings System

**How it works:**
1. Users can rate products 1-5 stars
2. Users can write text review
3. One review per user per product (enforced)
4. Average rating calculated automatically
5. Rating distribution shown

**Average Rating Calculation:**
```python
SELECT AVG(rating) as avg_rating, COUNT(*) as review_count
FROM product_reviews
WHERE product_id = ? AND status = 'approved'
```

**One Review Per User:**
- Database UNIQUE constraint: `UNIQUE(user_id, product_id)`
- Application check before insert
- Prevents duplicate reviews

**Code Location:**
- Database: `product_reviews` table with UNIQUE constraint
- Backend: `calculate_average_rating()` function
- Frontend: Rating display and submission form

### 3. Search Functionality

**How it works:**
1. User enters search term
2. Search in product name and description
3. SQL LIKE query with wildcards
4. Results displayed in product grid

**SQL Query:**
```sql
WHERE (product_name LIKE '%search%' OR description LIKE '%search%')
```

**Code Location:**
- Backend: `products()` route in `app.py`
- Frontend: Search input in `products.html`

### 4. Filter System

**Filters Available:**
- Category (dropdown)
- Price range (min-max)
- Minimum rating (dropdown)
- Sort by (newest, price, rating)

**How it works:**
1. User selects filter options
2. Form submits with filter parameters
3. Backend builds dynamic WHERE clause
4. Results filtered and displayed

**Code Location:**
- Backend: `products()` route (dynamic query building)
- Frontend: Filter form in `products.html`

### 5. Image Upload

**How it works:**
1. Validate file type (jpg, png, etc.)
2. Validate file size (max 5MB)
3. Generate unique filename
4. Save to `static/uploads/products/`
5. Store path in database

**Security:**
- File type validation
- File size limit
- Secure filename generation
- Path stored, not full file

## 📱 Responsive Design

**Approach:**
- Bootstrap 5 grid system
- Mobile-first design
- Breakpoints: xs, sm, md, lg, xl
- Flexible images and layouts

**Key Responsive Features:**
- Navigation collapses on mobile
- Product grid: 4 columns (desktop) → 2 columns (tablet) → 1 column (mobile)
- Filter sidebar stacks on mobile
- Touch-friendly buttons

## 🧪 Testing Checklist

### Functional Testing
- [ ] User registration works
- [ ] User login works
- [ ] Product listing displays correctly
- [ ] Search finds products
- [ ] Filters work correctly
- [ ] Product detail page loads
- [ ] Image gallery works
- [ ] Review submission works
- [ ] One review per user enforced
- [ ] Average rating calculates correctly

### Security Testing
- [ ] SQL injection prevented
- [ ] Passwords are hashed
- [ ] Session management works
- [ ] Unauthorized access blocked
- [ ] File upload validation works

### UI/UX Testing
- [ ] Responsive on mobile
- [ ] Images load correctly
- [ ] Forms validate input
- [ ] Error messages display
- [ ] Success messages display

## 🎓 Viva Questions & Answers

### Q1: Why did you choose Flask over Django?
**Answer:** Flask is lightweight and flexible. For this project, we don't need Django's admin panel and built-in features. Flask gives us more control and is easier to understand for beginners.

### Q2: How do you prevent SQL injection?
**Answer:** We use prepared statements with SQLAlchemy. Parameters are passed separately and escaped automatically. Example: `text("SELECT * FROM users WHERE username = :username")` with `{'username': username}`.

### Q3: How is password security handled?
**Answer:** Passwords are hashed using bcrypt before storing. The `hash_password()` function uses bcrypt's `gensalt()` to create a unique salt for each password. We never store plain text passwords.

### Q4: Explain the one-review-per-user feature.
**Answer:** We use a UNIQUE constraint in the database: `UNIQUE(user_id, product_id)`. This ensures at the database level that a user can only have one review per product. We also check in the application before inserting.

### Q5: How is average rating calculated?
**Answer:** We use SQL's AVG() function: `SELECT AVG(rating) FROM product_reviews WHERE product_id = ?`. This calculates the average of all approved reviews for a product. We round it to 1 decimal place for display.

### Q6: Why separate table for product images?
**Answer:** This allows multiple images per product (Flipkart-style). A single product can have 1-5 images. The `is_primary` flag identifies the main image, and `image_order` controls display sequence.

### Q7: How does the filter system work?
**Answer:** Filters are passed as query parameters. The backend builds a dynamic WHERE clause based on selected filters. For example, if category is selected, we add `category_slug = ?` to the WHERE clause.

### Q8: What is session-based authentication?
**Answer:** When user logs in, we store their user_id in Flask's session. Session data is stored server-side and secured. On each request, we check if user_id exists in session to verify authentication.

## 📚 Technologies Used

1. **Python Flask** - Web framework
2. **MySQL** - Database
3. **SQLAlchemy** - Database toolkit
4. **Bootstrap 5** - CSS framework
5. **Bootstrap Icons** - Icon library
6. **bcrypt** - Password hashing
7. **Werkzeug** - WSGI utilities

## 🔄 Future Enhancements

1. **Cart & Checkout** - Shopping cart functionality
2. **Payment Gateway** - Online payment integration
3. **Email Notifications** - Order confirmations
4. **Admin Panel** - Product management interface
5. **Wishlist** - Save favorite products
6. **Order Tracking** - Track order status
7. **Chat System** - Buyer-seller communication

## 📝 Code Structure Explanation

### app.py Structure:
1. **Configuration** - Database and app settings
2. **Helper Functions** - Reusable functions (hashing, validation)
3. **Routes** - URL endpoints and handlers
4. **Error Handlers** - 404, 500 error pages

### Template Structure:
- **base.html** - Base template with navigation
- **index.html** - Home page with featured products
- **products.html** - Product listing with filters
- **product_detail.html** - Product detail with gallery and reviews

### Database Queries:
- All queries use prepared statements
- Parameters passed separately
- Results fetched as dictionaries for easy access

---

**This project demonstrates:**
- Full-stack web development
- Database design and normalization
- Security best practices
- Responsive UI design
- RESTful API concepts
- Session management

**Suitable for:** Final Year Project, Portfolio, Learning Flask
