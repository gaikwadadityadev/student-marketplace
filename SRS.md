# Software Requirements Specification (SRS)
## Student Marketplace

### 1. Introduction

#### 1.1 Purpose
This document specifies the requirements for the Student Marketplace system, an e-commerce platform designed for students to buy and sell products within their academic community.

#### 1.2 Scope
The Student Marketplace allows students to:
- Register and manage accounts
- List products for sale (books, accessories, gadgets, etc.)
- Browse and search for products
- Add products to cart and place orders
- View order history

Administrators can:
- Approve or reject product listings
- Manage user accounts (block/unblock)
- View system statistics

#### 1.3 Definitions and Acronyms
- **SRS:** Software Requirements Specification
- **CRUD:** Create, Read, Update, Delete
- **UI:** User Interface
- **API:** Application Programming Interface
- **SQL:** Structured Query Language

### 2. Overall Description

#### 2.1 Product Perspective
The Student Marketplace is a web-based application built using:
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Backend:** Python Flask
- **Database:** MySQL

#### 2.2 Product Functions
1. User Authentication (Registration, Login, Logout)
2. Product Management (Upload, Edit, Delete, View)
3. Product Search and Filtering
4. Shopping Cart Management
5. Order Processing
6. Admin Product Approval
7. Admin User Management

#### 2.3 User Classes and Characteristics

**Students:**
- Can register and create accounts
- Can list products for sale
- Can browse and purchase products
- Can manage their own products and orders

**Administrators:**
- Can approve/reject product listings
- Can block/unblock user accounts
- Can view system statistics

#### 2.4 Operating Environment
- **Server:** Windows/Linux/Mac with Python 3.8+
- **Database:** MySQL 5.7+
- **Browser:** Modern browsers (Chrome, Firefox, Edge, Safari)
- **Network:** Internet connection required

### 3. System Features

#### 3.1 User Registration and Authentication

**3.1.1 Description**
Students can register with username, email, password, full name, and phone number. Passwords are securely hashed using bcrypt.

**3.1.2 Functional Requirements**
- FR-1.1: System shall allow new users to register
- FR-1.2: System shall validate all required fields
- FR-1.3: System shall check for duplicate usernames/emails
- FR-1.4: System shall hash passwords before storage
- FR-1.5: System shall allow users to login with username and password
- FR-1.6: System shall maintain user sessions
- FR-1.7: System shall allow users to logout

#### 3.2 Product Management

**3.2.1 Description**
Students can upload products with name, description, price, category, and image. Products require admin approval before being visible.

**3.2.2 Functional Requirements**
- FR-2.1: System shall allow students to upload products
- FR-2.2: System shall validate product information
- FR-2.3: System shall support image uploads (JPG, PNG, GIF, WEBP)
- FR-2.4: System shall set product status to "pending" on upload
- FR-2.5: System shall allow students to edit their products
- FR-2.6: System shall allow students to delete their products
- FR-2.7: System shall display only approved products to students

#### 3.3 Product Search and Browsing

**3.3.1 Description**
Students can search products by name/description and filter by category.

**3.3.2 Functional Requirements**
- FR-3.1: System shall display all approved products
- FR-3.2: System shall allow search by product name/description
- FR-3.3: System shall allow filtering by category
- FR-3.4: System shall display product details on click

#### 3.4 Shopping Cart

**3.4.1 Description**
Students can add products to cart, update quantities, and remove items.

**3.4.2 Functional Requirements**
- FR-4.1: System shall allow adding products to cart
- FR-4.2: System shall allow updating item quantities
- FR-4.3: System shall allow removing items from cart
- FR-4.4: System shall calculate cart total
- FR-4.5: System shall persist cart data in database

#### 3.5 Order Management

**3.5.1 Description**
Students can place orders from cart and view order history.

**3.5.2 Functional Requirements**
- FR-5.1: System shall allow placing orders from cart
- FR-5.2: System shall create order records
- FR-5.3: System shall clear cart after order placement
- FR-5.4: System shall display order history
- FR-5.5: System shall show order status

#### 3.6 Admin Dashboard

**3.6.1 Description**
Administrators can approve/reject products and manage users.

**3.6.2 Functional Requirements**
- FR-6.1: System shall require admin login
- FR-6.2: System shall display pending products
- FR-6.3: System shall allow approving products
- FR-6.4: System shall allow rejecting products
- FR-6.5: System shall display all users
- FR-6.6: System shall allow blocking users
- FR-6.7: System shall allow unblocking users
- FR-6.8: System shall display statistics

### 4. Non-Functional Requirements

#### 4.1 Performance
- Page load time should be under 3 seconds
- Database queries should use indexes
- Image uploads limited to 16MB

#### 4.2 Security
- Passwords must be hashed (bcrypt)
- SQL queries must use prepared statements
- File uploads must be validated
- Session management for authentication
- Role-based access control

#### 4.3 Usability
- Responsive design for mobile/tablet/desktop
- Intuitive navigation
- Clear error messages
- Bootstrap-based modern UI

#### 4.4 Reliability
- Error handling for all operations
- Database transaction support
- Input validation

#### 4.5 Maintainability
- Clean, commented code
- Modular structure
- Consistent coding style

### 5. System Models

#### 5.1 Use Case Diagram
```
[Student] --> (Register)
[Student] --> (Login)
[Student] --> (Upload Product)
[Student] --> (Browse Products)
[Student] --> (Add to Cart)
[Student] --> (Place Order)
[Admin] --> (Approve Product)
[Admin] --> (Manage Users)
```

#### 5.2 Data Flow
1. User Registration → Database
2. Product Upload → Database (pending) → Admin Approval → Database (approved)
3. Cart Addition → Database
4. Order Placement → Database

### 6. Constraints

#### 6.1 Technical Constraints
- Must use MySQL database
- Must use Flask framework
- Must support file uploads
- Must be web-based

#### 6.2 Business Constraints
- Products require admin approval
- Only approved products visible to students
- Students can only edit/delete their own products

### 7. Assumptions and Dependencies

#### 7.1 Assumptions
- Users have internet connection
- MySQL server is available
- Users have modern web browsers
- Admin will review products regularly

#### 7.2 Dependencies
- Python 3.8+
- MySQL 5.7+
- Flask framework
- Bootstrap 5
- bcrypt library

### 8. Glossary

- **Product:** Item listed for sale by a student
- **Cart:** Temporary storage for products before purchase
- **Order:** Completed purchase transaction
- **Admin:** System administrator with approval privileges
- **Student:** Regular user who can buy and sell products

---

**Document Version:** 1.0  
**Date:** 2025  
**Status:** Final

