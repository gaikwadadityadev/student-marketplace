# Student Marketplace - Simple Step-by-Step Guide
## Complete Setup from Scratch

---

## 📋 Prerequisites Checklist

Before starting, make sure you have:
- [ ] Python 3.8 or higher installed
- [ ] MySQL installed and running
- [ ] Internet connection (for downloading packages)

---

## 🚀 Step-by-Step Instructions

### **STEP 1: Open Command Prompt/Terminal**

1. Press `Windows Key + R`
2. Type `cmd` and press Enter
3. Navigate to your project folder:
   ```bash
   cd "C:\Users\adity\OneDrive\Documents\Project\Student Marketplace"
   ```

---

### **STEP 2: Create Virtual Environment (Optional but Recommended)**

```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` at the start of your command line.

---

### **STEP 3: Install Python Packages**

```bash
pip install -r backend/requirements.txt
```

Wait for installation to complete.

---

### **STEP 4: Set Up MySQL Database**

#### 4.1. Open MySQL

```bash
mysql -u root -p
```

Enter your MySQL password when prompted.

#### 4.2. Create Database

In MySQL, run:
```sql
CREATE DATABASE IF NOT EXISTS student_marketplace;
USE student_marketplace;
```

#### 4.3. Exit MySQL

```sql
exit;
```

#### 4.4. Import Database Schema

```bash
mysql -u root -p student_marketplace < backend/sql/schema.sql
```

Enter your MySQL password when prompted.

---

### **STEP 5: Configure MySQL Connection**

#### 5.1. Create `.env` File

1. Go to the `backend` folder
2. Create a new file named `.env` (exactly this name, no extension)
3. Open it in Notepad and add:

```env
MYSQL_USER=root
MYSQL_PASSWORD=YOUR_MYSQL_PASSWORD
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_DB=student_marketplace
SECRET_KEY=my-secret-key-12345
```

**Important:** Replace `YOUR_MYSQL_PASSWORD` with your actual MySQL root password.

**If you have no password (XAMPP users), use:**
```env
MYSQL_PASSWORD=
```

---

### **STEP 6: Create Admin Account**

```bash
cd backend
python create_admin.py
```

Follow the prompts:
- Username: Press Enter for `admin` (or type your own)
- Email: Press Enter for `admin@marketplace.com` (or type your own)
- Password: Press Enter for `admin123` (or type your own)
- Full Name: Press Enter for `Admin User` (or type your own)

You should see: "Admin user 'admin' created successfully!"

---

### **STEP 7: Run the Flask Application**

```bash
python backend/app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
```

**Keep this window open!** Don't close it.

---

### **STEP 8: Open Website in Browser**

1. Open any web browser (Chrome, Firefox, Edge)
2. Go to: **http://localhost:5000**
3. You should see the Student Marketplace home page!

---

## 🎯 Testing the Application

### **Test 1: Admin Login**

1. Go to: http://localhost:5000/admin/login
2. Username: `admin`
3. Password: `admin123` (or what you set)
4. Click Login
5. You should see the Admin Dashboard

### **Test 2: Student Registration**

1. Go to: http://localhost:5000/register
2. Fill in the form:
   - Full Name: Test User
   - Username: testuser
   - Email: test@example.com
   - Phone: 1234567890
   - Password: test123
3. Click Register
4. You should see "Registration successful!"

### **Test 3: Student Login**

1. Go to: http://localhost:5000/login
2. Username: `testuser`
3. Password: `test123`
4. Click Login
5. You should see the Student Dashboard

### **Test 4: Upload a Product**

1. After logging in as student, click "Sell Product"
2. Fill in:
   - Product Name: Test Book
   - Description: This is a test product
   - Price: 100
   - Category: Books
   - (Optional) Upload an image
3. Click "Upload Product"
4. You should see "Product uploaded successfully!"

### **Test 5: Approve Product (Admin)**

1. Logout and login as admin
2. Go to Admin Dashboard
3. You should see "Test Book" in pending products
4. Click "Approve"
5. Product is now approved!

### **Test 6: Browse and Buy**

1. Logout and login as student (or register another account)
2. Go to "Products" menu
3. You should see "Test Book"
4. Click "View Details"
5. Click "Add to Cart"
6. Go to Cart
7. Click "Proceed to Checkout"
8. Click "Place Order"
9. Order placed successfully!

---

## 📝 Quick Command Reference

### Start the Application
```bash
python backend/app.py
```

### Stop the Application
Press `CTRL + C` in the terminal where Flask is running

### Create Admin Account
```bash
cd backend
python create_admin.py
```

### Access Website
- Home: http://localhost:5000
- Admin Login: http://localhost:5000/admin/login
- Student Login: http://localhost:5000/login
- Register: http://localhost:5000/register

---

## ⚠️ Common Issues & Solutions

### Issue 1: "Module not found"
**Solution:** 
```bash
pip install -r backend/requirements.txt
```

### Issue 2: "Access denied for MySQL"
**Solution:** 
- Check your MySQL password in `backend/.env` file
- Make sure MySQL is running

### Issue 3: "Database doesn't exist"
**Solution:**
```bash
mysql -u root -p < backend/sql/schema.sql
```

### Issue 4: "Port already in use"
**Solution:**
- Close other Flask applications
- Or change port in `backend/app.py` line 830: `app.run(port=5001)`

### Issue 5: "Can't access website"
**Solution:**
- Make sure Flask is running (check terminal)
- Try: http://127.0.0.1:5000
- Check firewall settings

---

## 🎉 Success Checklist

After setup, you should be able to:
- [ ] Access http://localhost:5000
- [ ] Login as admin
- [ ] Register a new student
- [ ] Upload a product
- [ ] Approve product as admin
- [ ] Browse products
- [ ] Add to cart
- [ ] Place order

---

## 📞 Need Help?

1. Check `README.md` for detailed documentation
2. Check `FIX_MYSQL_ACCESS.md` for MySQL issues
3. Check error messages in the terminal
4. Make sure all steps were followed correctly

---

## 🚀 You're All Set!

Your Student Marketplace is now running! Enjoy testing and exploring all the features.

**Remember:** Keep the Flask terminal window open while using the website!

