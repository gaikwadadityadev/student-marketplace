# Data Flow Diagram (DFD)
## Student Marketplace System

### Level 0 - Context Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    STUDENT MARKETPLACE                       │
│                                                              │
│  ┌──────────┐         ┌──────────┐         ┌──────────┐   │
│  │ Student  │         │  Admin   │         │  System  │   │
│  └────┬─────┘         └────┬─────┘         └────┬─────┘   │
│       │                    │                    │          │
│       │ Login/Register     │ Admin Login        │          │
│       │ Browse Products    │ Approve Products   │          │
│       │ Add to Cart        │ Manage Users       │          │
│       │ Place Orders       │ View Statistics    │          │
│       │ Manage Products    │                    │          │
│       │                    │                    │          │
│       └────────────────────┴────────────────────┘          │
│                            │                               │
│                            ▼                               │
│                    ┌───────────────┐                       │
│                    │   Database    │                       │
│                    │    (MySQL)    │                       │
│                    └───────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### Level 1 - System Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                      STUDENT MARKETPLACE SYSTEM                   │
└──────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   Student    │
└──────┬───────┘
       │
       ├─────────────────────────────────────────────────┐
       │                                                 │
       ▼                                                 ▼
┌──────────────┐                                ┌──────────────┐
│  Authentication│                               │  Product     │
│   Process     │                               │  Management  │
│               │                               │              │
│ - Register    │                               │ - Upload     │
│ - Login       │                               │ - Edit       │
│ - Logout      │                               │ - Delete     │
│ - Session     │                               │ - View       │
└──────┬───────┘                               └──────┬───────┘
       │                                                │
       │                                                │
       ▼                                                ▼
┌──────────────┐                                ┌──────────────┐
│   Shopping   │                                │   Database   │
│   Process    │                                │   (MySQL)    │
│              │                                │              │
│ - Browse     │                                │ - Users      │
│ - Search     │                                │ - Products   │
│ - Cart       │                                │ - Cart       │
│ - Checkout   │                                │ - Orders     │
│ - Orders     │                                │              │
└──────┬───────┘                                └──────────────┘
       │
       │
       ▼
┌──────────────┐
│   Admin      │
│   Process    │
│              │
│ - Approve    │
│ - Reject     │
│ - Manage     │
│   Users      │
└──────────────┘
```

### Level 2 - Detailed Data Flow

#### Process 1: User Authentication

```
┌──────────────┐
│   Student    │
└──────┬───────┘
       │
       │ Registration Data
       │ (username, email, password, etc.)
       ▼
┌─────────────────────┐
│  1.0 Authentication │
│                     │
│  - Validate Input   │
│  - Hash Password    │
│  - Check Duplicates │
│  - Create Session   │
└──────┬──────────────┘
       │
       │ User Data
       │ Session Data
       ▼
┌──────────────┐
│   Database   │
│   (Users)    │
└──────────────┘
```

#### Process 2: Product Management

```
┌──────────────┐
│   Student    │
└──────┬───────┘
       │
       │ Product Data
       │ (name, price, image, etc.)
       ▼
┌─────────────────────┐
│  2.0 Product        │
│     Management      │
│                     │
│  - Validate Data    │
│  - Upload Image     │
│  - Set Status       │
│  - CRUD Operations  │
└──────┬──────────────┘
       │
       │ Product Info
       │ (status: pending)
       ▼
┌──────────────┐
│   Database   │
│  (Products)  │
└──────────────┘
```

#### Process 3: Shopping Process

```
┌──────────────┐
│   Student    │
└──────┬───────┘
       │
       │ Search/Filter
       │ Cart Actions
       │ Order Request
       ▼
┌─────────────────────┐
│  3.0 Shopping       │
│     Process         │
│                     │
│  - Search Products  │
│  - Add to Cart      │
│  - Update Cart      │
│  - Place Order      │
│  - View History     │
└──────┬──────────────┘
       │
       │ Product List
       │ Cart Data
       │ Order Data
       ▼
┌──────────────┐
│   Database   │
│ (Products,   │
│  Cart,       │
│  Orders)     │
└──────────────┘
```

#### Process 4: Admin Process

```
┌──────────────┐
│    Admin     │
└──────┬───────┘
       │
       │ Approval Decision
       │ User Management
       ▼
┌─────────────────────┐
│  4.0 Admin          │
│     Process         │
│                     │
│  - View Pending     │
│  - Approve/Reject   │
│  - Block/Unblock    │
│  - View Statistics  │
└──────┬──────────────┘
       │
       │ Updated Status
       │ User Status
       ▼
┌──────────────┐
│   Database   │
│ (Products,   │
│  Users)      │
└──────────────┘
```

### Data Flow Details

#### Data Stores

1. **D1: Users**
   - Stores: User accounts, authentication data
   - Input: Registration data, login data
   - Output: User information, session data

2. **D2: Products**
   - Stores: Product listings, images, status
   - Input: Product uploads, edits
   - Output: Product listings, search results

3. **D3: Cart**
   - Stores: Cart items, quantities
   - Input: Add to cart, update quantity
   - Output: Cart contents

4. **D4: Orders**
   - Stores: Order records, order items
   - Input: Order placement
   - Output: Order history

#### External Entities

1. **Student**
   - Inputs: Registration, login, product upload, search, cart actions, orders
   - Outputs: Product listings, cart contents, order confirmations

2. **Admin**
   - Inputs: Admin login, approval decisions, user management
   - Outputs: Pending products, user lists, statistics

#### Data Flows

1. **Registration Flow:**
   Student → Authentication → Database (Users)
   - Data: username, email, password, full_name, phone

2. **Login Flow:**
   Student → Authentication → Database (Users) → Session
   - Data: username, password → session_id, user_data

3. **Product Upload Flow:**
   Student → Product Management → Database (Products)
   - Data: name, description, price, category, image → product_id, status

4. **Product Approval Flow:**
   Database (Products) → Admin → Admin Process → Database (Products)
   - Data: pending products → approval decision → status update

5. **Shopping Flow:**
   Student → Shopping Process → Database (Products, Cart, Orders)
   - Data: search query → product list
   - Data: product_id → cart item
   - Data: cart → order

6. **Order Flow:**
   Shopping Process → Database (Orders, Order_Items) → Database (Cart cleared)
   - Data: cart items → order → order_items

### Process Specifications

#### P1: Authentication Process
- **Input:** Registration/Login data
- **Process:** Validate, hash password, check duplicates, create session
- **Output:** Session data, user information
- **Error Handling:** Invalid credentials, duplicate username/email

#### P2: Product Management Process
- **Input:** Product data, image file
- **Process:** Validate, upload image, set status to pending
- **Output:** Product record with pending status
- **Error Handling:** Invalid data, file upload errors

#### P3: Shopping Process
- **Input:** Search query, product selection, cart actions
- **Process:** Search products, manage cart, process orders
- **Output:** Product listings, cart contents, order confirmation
- **Error Handling:** Product not found, cart errors

#### P4: Admin Process
- **Input:** Approval decisions, user management actions
- **Process:** Update product status, update user status, calculate statistics
- **Output:** Updated records, statistics
- **Error Handling:** Invalid operations

### Data Dictionary

#### Data Elements

1. **user_id:** Integer, Primary Key, Unique identifier for users
2. **username:** String(50), Unique, User login name
3. **email:** String(100), Unique, User email address
4. **password:** String(255), Hashed, User password
5. **product_id:** Integer, Primary Key, Unique identifier for products
6. **product_name:** String(255), Product name
7. **price:** Decimal(10,2), Product price in currency
8. **status:** Enum, Product/Order status (pending, approved, etc.)
9. **order_id:** Integer, Primary Key, Unique identifier for orders
10. **total_amount:** Decimal(10,2), Total order amount

---

**Diagram Created:** 2025  
**Version:** 1.0  
**Notation:** Yourdon/DeMarco DFD Notation

