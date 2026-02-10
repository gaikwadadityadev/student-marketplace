# Quick Setup Guide
## Student Marketplace - Step by Step Installation

### Prerequisites Check
- [ ] Python 3.8+ installed
- [ ] MySQL 5.7+ installed and running
- [ ] pip installed

### Step 1: Database Setup (5 minutes)

1. **Start MySQL Server**
   ```bash
   # Windows: Start MySQL service from Services
   # Linux: sudo systemctl start mysql
   # Mac: brew services start mysql
   ```

2. **Create Database**
   ```bash
   mysql -u root -p < backend/sql/schema.sql
   ```
   
   Or manually:
   ```sql
   mysql -u root -p
   source backend/sql/schema.sql;
   ```

3. **Verify Database**
   ```sql
   USE student_marketplace;
   SHOW TABLES;
   ```
   You should see: users, products, cart, orders, order_items

### Step 2: Python Environment Setup (3 minutes)

1. **Navigate to project directory**
   ```bash
   cd "Student Marketplace"
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

### Step 3: Configuration (2 minutes)

1. **Update database credentials** (if needed)
   
   Edit `backend/config.py` or create `.env` file:
   ```env
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_HOST=127.0.0.1
   MYSQL_PORT=3306
   MYSQL_DB=student_marketplace
   ```

2. **Create uploads directory** (usually auto-created)
   ```bash
   mkdir -p static/uploads
   ```

### Step 4: Create Admin Account (2 minutes)

```bash
cd backend
python create_admin.py
```

Follow prompts:
- Username: admin (or press Enter for default)
- Email: admin@marketplace.com (or press Enter)
- Password: admin123 (or press Enter)
- Full Name: Admin User (or press Enter)

### Step 5: Run Application (1 minute)

```bash
# From backend directory
python app.py
```

Or from project root:
```bash
python backend/app.py
```

### Step 6: Access Application

Open browser and go to:
- **Home:** http://localhost:5000
- **Admin Login:** http://localhost:5000/admin/login
- **Student Registration:** http://localhost:5000/register

### Step 7: Test the Application

1. **Register a student account**
   - Go to http://localhost:5000/register
   - Fill in the form and register

2. **Login as student**
   - Go to http://localhost:5000/login
   - Login with your credentials

3. **Upload a product**
   - Go to Dashboard → Sell Product
   - Fill in product details and upload

4. **Login as admin**
   - Go to http://localhost:5000/admin/login
   - Login with admin credentials
   - Approve the product you just uploaded

5. **Browse and buy**
   - Login as student
   - Browse products
   - Add to cart and checkout

### Troubleshooting

#### Database Connection Error
```
Error: Can't connect to MySQL server
```
**Solution:**
- Check MySQL is running
- Verify credentials in config.py
- Test connection: `mysql -u root -p`

#### Module Not Found Error
```
ModuleNotFoundError: No module named 'flask'
```
**Solution:**
- Activate virtual environment
- Run: `pip install -r requirements.txt`

#### Port Already in Use
```
Error: Address already in use
```
**Solution:**
- Change port in app.py: `app.run(port=5001)`
- Or kill process using port 5000

#### Permission Denied (File Upload)
```
PermissionError: [Errno 13] Permission denied
```
**Solution:**
- Check static/uploads directory exists
- Verify write permissions
- Create directory manually if needed

### Verification Checklist

- [ ] Database created successfully
- [ ] All tables exist (users, products, cart, orders, order_items)
- [ ] Python dependencies installed
- [ ] Admin account created
- [ ] Application runs without errors
- [ ] Can access home page
- [ ] Can register new user
- [ ] Can login
- [ ] Can upload product
- [ ] Can approve product (admin)
- [ ] Can browse products
- [ ] Can add to cart
- [ ] Can place order

### Next Steps

1. **Add Sample Products**
   - Register multiple student accounts
   - Upload various products
   - Test search and filtering

2. **Test Admin Features**
   - Approve/reject products
   - Block/unblock users
   - View statistics

3. **Customize**
   - Update branding/colors
   - Add more categories
   - Customize email templates (if added)

### Support

For detailed documentation, see:
- `README.md` - Full documentation
- `SRS.md` - Software Requirements
- `ER_DIAGRAM.md` - Database Design
- `DFD.md` - Data Flow Diagram
- `PROJECT_ANALYSIS.md` - Project Analysis

---

**Setup Time:** ~15 minutes  
**Difficulty:** Beginner  
**Status:** Ready for Development

