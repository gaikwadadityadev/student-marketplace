-- Script to create sample users with proper password hashing
-- Note: Run create_admin.py Python script instead for proper bcrypt hashing
-- This SQL file is for reference only

-- To create users with proper password hashing, use the Python script:
-- python backend/create_admin.py

-- Or use this SQL after generating bcrypt hashes in Python:
-- Example: password 'student123' hashed with bcrypt

USE student_marketplace;

-- Admin user (password: admin123)
-- Generate hash using: python -c "import bcrypt; print(bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))"
INSERT INTO users (username, email, password, full_name, role, status) 
VALUES ('admin', 'admin@marketplace.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'Admin User', 'admin', 'active')
ON DUPLICATE KEY UPDATE password = VALUES(password);

-- Sample student users (password: student123)
-- Note: Replace the password hash with actual bcrypt hash generated in Python
INSERT INTO users (username, email, password, full_name, phone, role, status) VALUES
('john_doe', 'john@student.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'John Doe', '9876543210', 'student', 'active'),
('jane_smith', 'jane@student.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'Jane Smith', '9876543211', 'student', 'active'),
('mike_wilson', 'mike@student.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyY5Y5Y5Y5Y5', 'Mike Wilson', '9876543212', 'student', 'active')
ON DUPLICATE KEY UPDATE password = VALUES(password);

-- Note: The password hashes above are placeholders.
-- For actual use, generate proper bcrypt hashes using the create_admin.py script
-- or use: python -c "import bcrypt; print(bcrypt.hashpw('your_password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))"

