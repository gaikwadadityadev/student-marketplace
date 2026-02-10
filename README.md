# Student Marketplace

A complete e-commerce platform for students to buy and sell products like books, accessories, gadgets, etc.

## Project Overview

**Project Type:** Final Year Project  
**Frontend:** HTML, CSS, JavaScript, Bootstrap 5  
**Backend:** Python Flask  
**Database:** MySQL  

## Features

- ✅ Student Registration & Login
- ✅ Product Upload with Image Support
- ✅ Product Management (CRUD Operations)
- ✅ Product Search & Filtering
- ✅ Shopping Cart System
- ✅ Order Placement & History
- ✅ Admin Dashboard
- ✅ Product Approval System
- ✅ User Management (Block/Unblock)
- ✅ Responsive UI with Bootstrap
- ✅ Secure Authentication with Password Hashing
- ✅ Prepared Statements for SQL Security

## Project Structure

```
Student Marketplace/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── requirements.txt       # Python dependencies
│   └── sql/
│       ├── schema.sql         # Database schema
│       └── sample_data.sql    # Sample data for testing
├── templates/
│   ├── base.html              # Base template
│   ├── index.html             # Landing page
│   ├── login.html             # Student login
│   ├── register.html          # Student registration
│   ├── dashboard.html         # Student dashboard
│   ├── product_upload.html    # Upload product
│   ├── product_edit.html      # Edit product
│   ├── products.html          # Product listing
│   ├── product_view.html      # Product details
│   ├── cart.html              # Shopping cart
│   ├── checkout.html          # Checkout page
│   ├── order_history.html     # Order history
│   ├── admin_login.html       # Admin login
│   ├── admin_dashboard.html   # Admin dashboard
│   ├── 404.html               # Error page
│   └── 500.html               # Error page
├── static/
│   ├── css/
│   │   └── style.css          # Custom styles
│   ├── js/
│   │   └── main.js            # Custom JavaScript
│   └── uploads/               # Product images storage
├── README.md                  # This file
├── SRS.md                     # Software Requirements Specification
├── ER_DIAGRAM.md              # Entity Relationship Diagram
├── DFD.md                     # Data Flow Diagram
└── PROJECT_ANALYSIS.md        # Advantages, Disadvantages, Future Scope
```

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- MySQL 5.7 or higher
- pip (Python package manager)
- Git (optional)

## Installation & Setup

### Step 1: Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd "Student Marketplace"
```

### Step 2: Set Up Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Set Up MySQL Database

1. Open MySQL command line or MySQL Workbench
2. Run the schema file to create the database:

```bash
mysql -u root -p < backend/sql/schema.sql
```

Or manually:
```sql
-- Open MySQL and run:
source backend/sql/schema.sql;
```

3. (Optional) Load sample data:

```bash
mysql -u root -p < backend/sql/sample_data.sql
```

### Step 5: Configure Database Connection

Create a `.env` file in the `backend` directory (optional, or modify `config.py`):

```env
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=student_marketplace
SECRET_KEY=your-secret-key-here
```

Or modify `backend/config.py` directly with your MySQL credentials.

### Step 6: Create Upload Directory

The upload directory should be created automatically, but if not:

```bash
# Windows PowerShell
mkdir static\uploads

# Linux/Mac
mkdir -p static/uploads
```

### Step 7: Run the Application

```bash
# From the backend directory
cd backend
python app.py
```

Or from project root:

```bash
python backend/app.py
```

The application will run on `http://localhost:5000`

## Creating Admin Account

To create an admin account, use the provided Python script:

```bash
cd backend
python create_admin.py
```

Follow the prompts to create an admin user. The script will:
- Hash the password using bcrypt
- Create the admin account in the database
- Set the role to 'admin'

**Default values:**
- Username: admin
- Email: admin@marketplace.com
- Password: admin123
- Full Name: Admin User

You can also create student accounts through the registration page at `/register`.

**Alternative method (MySQL):**
1. Register a user through the web interface
2. Update the role in MySQL:
```sql
USE student_marketplace;
UPDATE users SET role='admin' WHERE username='your_username';
```

## Usage Guide

### For Students:

1. **Register/Login:** Create an account or login
2. **Browse Products:** View all approved products
3. **Search/Filter:** Use search bar and category filter
4. **Add to Cart:** Click "Add to Cart" on any product
5. **Checkout:** Review cart and place order
6. **Sell Products:** Upload products (requires admin approval)
7. **Manage Products:** Edit or delete your products from dashboard
8. **View Orders:** Check order history

### For Admin:

1. **Login:** Use admin credentials
2. **Approve Products:** Review and approve/reject pending products
3. **Manage Users:** Block or unblock student accounts
4. **View Statistics:** See dashboard statistics

## Database Schema

The database includes the following tables:

- **users** - Student and admin accounts
- **products** - Product listings
- **cart** - Shopping cart items
- **orders** - Order records
- **order_items** - Order line items

See `backend/sql/schema.sql` for complete schema.

## Security Features

- ✅ Password hashing using bcrypt
- ✅ Prepared statements for SQL queries (prevents SQL injection)
- ✅ Session management
- ✅ File upload validation
- ✅ Role-based access control
- ✅ Input validation

## Troubleshooting

### Database Connection Error

- Check MySQL is running
- Verify credentials in `config.py` or `.env`
- Ensure database `student_marketplace` exists

### Import Errors

- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version (3.8+)

### File Upload Issues

- Check `static/uploads` directory exists
- Verify file permissions
- Check file size (max 16MB)

### Port Already in Use

- Change port in `app.py`: `app.run(port=5001)`
- Or kill the process using port 5000

## Development Notes

- The application uses Flask's development server (not for production)
- For production, use Gunicorn or uWSGI
- Enable HTTPS in production
- Use environment variables for sensitive data
- Implement proper error logging

## Technologies Used

- **Backend:** Flask, SQLAlchemy, PyMySQL, bcrypt
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
- **Database:** MySQL
- **Icons:** Bootstrap Icons

## License

This project is created for educational purposes as a Final Year Project.

## Author

Created for Final Year Project - Student Marketplace

## Support

For issues or questions, please refer to the documentation files:
- `SRS.md` - Software Requirements Specification
- `ER_DIAGRAM.md` - Database Design
- `DFD.md` - Data Flow Diagram
- `PROJECT_ANALYSIS.md` - Project Analysis

---

**Note:** This is a development version. For production deployment, additional security measures and optimizations are required.

