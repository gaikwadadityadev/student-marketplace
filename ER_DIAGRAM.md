# Entity Relationship Diagram (ERD)
## Student Marketplace Database Design

### Entity Relationship Diagram Description

```
┌─────────────────────────────────────────────────────────────────┐
│                         ER DIAGRAM                              │
└─────────────────────────────────────────────────────────────────┘

┌──────────────┐
│    USERS     │
├──────────────┤
│ user_id (PK) │
│ username     │
│ email        │
│ password     │
│ full_name    │
│ phone        │
│ role         │
│ status       │
│ created_at   │
└──────┬───────┘
       │
       │ 1
       │
       │ N
       │
┌──────▼──────────────┐         ┌──────────────┐
│     PRODUCTS        │         │     CART     │
├─────────────────────┤         ├──────────────┤
│ product_id (PK)     │         │ cart_id (PK) │
│ seller_id (FK) ─────┼─────────┤ user_id (FK) │
│ name                │   1     │ product_id   │
│ description         │    │    │ (FK)         │
│ price               │    │    │ quantity     │
│ category            │    │    │ created_at   │
│ image_path          │    │    └──────────────┘
│ status              │    │
│ created_at          │    │
│ updated_at          │    │
└─────────────────────┘    │
                           │
                           │ N
                           │
                    ┌──────▼──────────┐
                    │   ORDER_ITEMS   │
                    ├─────────────────┤
                    │ order_item_id   │
                    │   (PK)          │
                    │ order_id (FK)   │
                    │ product_id (FK) │
                    │ quantity        │
                    │ price           │
                    └──────┬──────────┘
                           │
                           │ N
                           │
                    ┌──────▼──────┐
                    │   ORDERS    │
                    ├─────────────┤
                    │ order_id    │
                    │   (PK)      │
                    │ buyer_id    │
                    │   (FK)      │
                    │ total_amount│
                    │ status      │
                    │ created_at  │
                    └─────────────┘
```

### Entity Descriptions

#### 1. USERS Entity
**Purpose:** Stores information about students and administrators

**Attributes:**
- `user_id` (Primary Key, INT, AUTO_INCREMENT): Unique identifier
- `username` (VARCHAR(50), UNIQUE, NOT NULL): Login username
- `email` (VARCHAR(100), UNIQUE, NOT NULL): Email address
- `password` (VARCHAR(255), NOT NULL): Hashed password
- `full_name` (VARCHAR(100), NOT NULL): Full name
- `phone` (VARCHAR(20)): Phone number (optional)
- `role` (ENUM('student', 'admin'), DEFAULT 'student'): User role
- `status` (ENUM('active', 'blocked'), DEFAULT 'active'): Account status
- `created_at` (TIMESTAMP): Registration timestamp

**Relationships:**
- One-to-Many with PRODUCTS (one user can have many products)
- One-to-Many with ORDERS (one user can have many orders)
- One-to-Many with CART (one user can have many cart items)

#### 2. PRODUCTS Entity
**Purpose:** Stores product listings

**Attributes:**
- `product_id` (Primary Key, INT, AUTO_INCREMENT): Unique identifier
- `seller_id` (Foreign Key → USERS.user_id, NOT NULL): Product seller
- `name` (VARCHAR(255), NOT NULL): Product name
- `description` (TEXT): Product description
- `price` (DECIMAL(10,2), NOT NULL): Product price
- `category` (VARCHAR(50)): Product category
- `image_path` (VARCHAR(255)): Path to product image
- `status` (ENUM('pending', 'approved', 'rejected'), DEFAULT 'pending'): Approval status
- `created_at` (TIMESTAMP): Creation timestamp
- `updated_at` (TIMESTAMP): Last update timestamp

**Relationships:**
- Many-to-One with USERS (many products belong to one user)
- One-to-Many with CART (one product can be in many carts)
- One-to-Many with ORDER_ITEMS (one product can be in many orders)

#### 3. CART Entity
**Purpose:** Stores shopping cart items

**Attributes:**
- `cart_id` (Primary Key, INT, AUTO_INCREMENT): Unique identifier
- `user_id` (Foreign Key → USERS.user_id, NOT NULL): Cart owner
- `product_id` (Foreign Key → PRODUCTS.product_id, NOT NULL): Product in cart
- `quantity` (INT, DEFAULT 1): Quantity of product
- `created_at` (TIMESTAMP): Addition timestamp

**Relationships:**
- Many-to-One with USERS (many cart items belong to one user)
- Many-to-One with PRODUCTS (many cart items reference one product)
- Unique constraint on (user_id, product_id) - one product per user in cart

#### 4. ORDERS Entity
**Purpose:** Stores order records

**Attributes:**
- `order_id` (Primary Key, INT, AUTO_INCREMENT): Unique identifier
- `buyer_id` (Foreign Key → USERS.user_id, NOT NULL): Order buyer
- `total_amount` (DECIMAL(10,2), NOT NULL): Total order amount
- `status` (ENUM('pending', 'completed', 'cancelled'), DEFAULT 'pending'): Order status
- `created_at` (TIMESTAMP): Order timestamp

**Relationships:**
- Many-to-One with USERS (many orders belong to one user)
- One-to-Many with ORDER_ITEMS (one order has many items)

#### 5. ORDER_ITEMS Entity
**Purpose:** Stores individual items in an order

**Attributes:**
- `order_item_id` (Primary Key, INT, AUTO_INCREMENT): Unique identifier
- `order_id` (Foreign Key → ORDERS.order_id, NOT NULL): Parent order
- `product_id` (Foreign Key → PRODUCTS.product_id, NOT NULL): Product ordered
- `quantity` (INT, NOT NULL): Quantity ordered
- `price` (DECIMAL(10,2), NOT NULL): Price at time of order

**Relationships:**
- Many-to-One with ORDERS (many items belong to one order)
- Many-to-One with PRODUCTS (many order items reference one product)

### Relationship Summary

1. **USERS → PRODUCTS** (1:N)
   - One user can list many products
   - Each product belongs to one user (seller)

2. **USERS → ORDERS** (1:N)
   - One user can place many orders
   - Each order belongs to one user (buyer)

3. **USERS → CART** (1:N)
   - One user can have many cart items
   - Each cart item belongs to one user

4. **PRODUCTS → CART** (1:N)
   - One product can be in many users' carts
   - Each cart item references one product

5. **PRODUCTS → ORDER_ITEMS** (1:N)
   - One product can be in many order items
   - Each order item references one product

6. **ORDERS → ORDER_ITEMS** (1:N)
   - One order can have many items
   - Each order item belongs to one order

### Key Constraints

1. **Primary Keys:** Each entity has a unique primary key
2. **Foreign Keys:** All foreign keys reference valid primary keys
3. **Unique Constraints:**
   - USERS.username (unique)
   - USERS.email (unique)
   - CART(user_id, product_id) (unique - one product per user in cart)
4. **Cascade Deletes:**
   - Deleting a user deletes their products, orders, and cart items
   - Deleting a product deletes related cart items and order items
   - Deleting an order deletes its order items

### Indexes

For performance optimization, indexes are created on:
- `users.email`
- `users.username`
- `users.role`
- `products.seller_id`
- `products.status`
- `products.category`
- `cart.user_id`
- `orders.buyer_id`
- `orders.status`
- `order_items.order_id`

### Data Types and Constraints

- **INT:** For IDs and quantities
- **VARCHAR:** For text fields with length limits
- **TEXT:** For longer text (descriptions)
- **DECIMAL(10,2):** For monetary values (price, total_amount)
- **ENUM:** For fixed value sets (role, status, category)
- **TIMESTAMP:** For date/time tracking

---

**Diagram Created:** 2025  
**Database:** MySQL  
**Version:** 1.0

