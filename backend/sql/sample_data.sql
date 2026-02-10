-- Sample Data for Student Marketplace
-- Use this to populate the database with test data

USE student_marketplace;

-- NOTE: For creating users with proper password hashing, use the Python script:
-- python backend/create_admin.py
-- 
-- Or register users through the web interface at /register
-- 
-- The password hashes below are placeholders and will NOT work.
-- To create test users, either:
-- 1. Use the registration page in the web interface
-- 2. Use the create_admin.py script for admin users
-- 3. Generate proper bcrypt hashes and update this file

-- Insert Admin User (PLACEHOLDER - Use create_admin.py instead)
-- Password: admin123
-- INSERT INTO users (username, email, password, full_name, phone, role, status) VALUES
-- ('admin', 'admin@marketplace.com', 'PLACEHOLDER_HASH', 'Admin User', '1234567890', 'admin', 'active');

-- Insert Sample Students (PLACEHOLDER - Register through web interface)
-- Password: student123
-- INSERT INTO users (username, email, password, full_name, phone, role, status) VALUES
-- ('john_doe', 'john@student.com', 'PLACEHOLDER_HASH', 'John Doe', '9876543210', 'student', 'active'),
-- ('jane_smith', 'jane@student.com', 'PLACEHOLDER_HASH', 'Jane Smith', '9876543211', 'student', 'active'),
-- ('mike_wilson', 'mike@student.com', 'PLACEHOLDER_HASH', 'Mike Wilson', '9876543212', 'student', 'active');

-- Insert Sample Products (Note: Update image_path after uploading images)
INSERT INTO products (seller_id, name, description, price, category, image_path, status) VALUES
(2, 'Calculus Textbook', 'Calculus textbook for engineering students. Good condition, barely used.', 500.00, 'Books', 'uploads/product_1.jpg', 'approved'),
(2, 'Laptop Stand', 'Adjustable laptop stand for better ergonomics. Metal construction.', 800.00, 'Accessories', 'uploads/product_2.jpg', 'approved'),
(3, 'Wireless Mouse', 'Logitech wireless mouse. Works perfectly, includes USB receiver.', 600.00, 'Gadgets', 'uploads/product_3.jpg', 'approved'),
(3, 'Python Programming Book', 'Learn Python programming. Comprehensive guide with examples.', 450.00, 'Books', 'uploads/product_4.jpg', 'approved'),
(4, 'USB-C Hub', 'Multi-port USB-C hub with HDMI, USB 3.0 ports. Perfect for laptops.', 1200.00, 'Gadgets', 'uploads/product_5.jpg', 'approved'),
(2, 'Backpack', 'College backpack with laptop compartment. Waterproof material.', 900.00, 'Accessories', 'uploads/product_6.jpg', 'pending'),
(4, 'Mechanical Keyboard', 'RGB mechanical keyboard. Blue switches, excellent condition.', 2500.00, 'Gadgets', 'uploads/product_7.jpg', 'pending'),
(3, 'Data Structures Book', 'Data structures and algorithms textbook. Latest edition.', 550.00, 'Books', 'uploads/product_8.jpg', 'approved');

-- Note: For actual password hashing, use bcrypt in Python:
-- import bcrypt
-- password = 'student123'
-- hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
-- The sample passwords above are placeholders. The actual app will hash them properly.
