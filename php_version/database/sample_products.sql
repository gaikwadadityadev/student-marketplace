-- =====================================================
-- Sample Realistic Student Products
-- =====================================================
USE student_marketplace_php;

-- Clear existing products (optional - uncomment if needed)
-- DELETE FROM product_images;
-- DELETE FROM product_reviews;
-- DELETE FROM products;

-- =====================================================
-- Books Category Products
-- =====================================================

-- Product 1: Engineering Mathematics Book
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 1, 'Engineering Mathematics - Volume 1', 'engineering-mathematics-volume-1', 
'Complete guide to Engineering Mathematics for first year students. Covers calculus, algebra, and differential equations. Used but in excellent condition with minimal highlighting. Perfect for exam preparation.', 
450.00, 10.00, 405.00, 3, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/eng-math-1.jpg', 1, 1),
(@product_id, 'uploads/products/eng-math-2.jpg', 2, 0);

-- Product 2: Data Structures Book
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 1, 'Data Structures and Algorithms in C++', 'data-structures-algorithms-cpp', 
'Comprehensive textbook on data structures. Includes arrays, linked lists, trees, graphs, and sorting algorithms. Previous edition but content is still relevant. No torn pages.', 
650.00, 15.00, 552.50, 2, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/dsa-book-1.jpg', 1, 1),
(@product_id, 'uploads/products/dsa-book-2.jpg', 2, 0);

-- =====================================================
-- Electronics Category Products
-- =====================================================

-- Product 3: Wireless Mouse
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 2, 'Logitech M170 Wireless Mouse', 'logitech-m170-wireless-mouse', 
'Compact wireless mouse perfect for laptops. 2.4GHz wireless connection, 12-month battery life. Used for 6 months, working perfectly. Original packaging included.', 
599.00, 20.00, 479.20, 1, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/mouse-1.jpg', 1, 1),
(@product_id, 'uploads/products/mouse-2.jpg', 2, 0);

-- Product 4: USB Flash Drive
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 2, 'SanDisk 32GB USB 3.0 Flash Drive', 'sandisk-32gb-usb-flash-drive', 
'High-speed USB 3.0 flash drive. 32GB storage capacity. Perfect for storing assignments, projects, and study materials. Brand new, sealed pack.', 
450.00, 5.00, 427.50, 5, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/usb-1.jpg', 1, 1);

-- Product 5: Laptop Stand
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 2, 'Adjustable Aluminum Laptop Stand', 'adjustable-aluminum-laptop-stand', 
'Ergonomic laptop stand with adjustable height. Fits laptops up to 17 inches. Improves posture during long study sessions. Lightweight and portable.', 
899.00, 25.00, 674.25, 2, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/laptop-stand-1.jpg', 1, 1),
(@product_id, 'uploads/products/laptop-stand-2.jpg', 2, 0);

-- =====================================================
-- Stationery Category Products
-- =====================================================

-- Product 6: Notebook Set
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 3, 'Classmate Notebook Set (5 Pack)', 'classmate-notebook-set-5-pack', 
'Set of 5 Classmate notebooks, 200 pages each. Ruled pages, perfect for taking notes. Unused, brand new. Great value for money.', 
250.00, 0.00, 250.00, 8, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/notebooks-1.jpg', 1, 1);

-- Product 7: Pen Set
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 3, 'Reynolds Gel Pen Set (10 Pens)', 'reynolds-gel-pen-set-10-pens', 
'Pack of 10 Reynolds gel pens in assorted colors. Smooth writing, no smudging. Perfect for exams and assignments. Brand new.', 
120.00, 0.00, 120.00, 12, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/pens-1.jpg', 1, 1);

-- Product 8: Scientific Calculator
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 3, 'Casio FX-991EX Scientific Calculator', 'casio-fx-991ex-scientific-calculator', 
'Advanced scientific calculator with 552 functions. Solar powered with battery backup. Allowed in engineering exams. Used but in excellent condition with manual.', 
1299.00, 30.00, 909.30, 1, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/calculator-1.jpg', 1, 1),
(@product_id, 'uploads/products/calculator-2.jpg', 2, 0);

-- =====================================================
-- Hostel Items Category Products
-- =====================================================

-- Product 9: Study Table Lamp
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 4, 'LED Study Table Lamp with USB Port', 'led-study-table-lamp-usb', 
'Adjustable LED desk lamp with 3 brightness levels. USB charging port for phone. Perfect for late-night study sessions. Energy efficient.', 
799.00, 15.00, 679.15, 3, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/lamp-1.jpg', 1, 1),
(@product_id, 'uploads/products/lamp-2.jpg', 2, 0);

-- Product 10: Storage Box
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 4, 'Plastic Storage Box with Lid (40L)', 'plastic-storage-box-40l', 
'Large storage box for organizing hostel room. Durable plastic, stackable design. Perfect for storing books, clothes, and other items. Brand new.', 
450.00, 10.00, 405.00, 4, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/storage-box-1.jpg', 1, 1);

-- Product 11: Bed Sheet Set
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 4, 'Cotton Bed Sheet Set (Single Bed)', 'cotton-bed-sheet-set-single', 
'Comfortable cotton bed sheet set for single bed. Includes 1 bed sheet and 1 pillow cover. Soft fabric, easy to wash. Used but clean and in good condition.', 
599.00, 20.00, 479.20, 2, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/bedsheet-1.jpg', 1, 1);

-- =====================================================
-- Accessories Category Products
-- =====================================================

-- Product 12: Backpack
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 5, 'Skybags Backpack (30L)', 'skybags-backpack-30l', 
'Durable laptop backpack with padded compartment. Multiple pockets for organization. Water-resistant material. Used for 1 year, still in great condition.', 
1299.00, 35.00, 844.35, 1, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/backpack-1.jpg', 1, 1),
(@product_id, 'uploads/products/backpack-2.jpg', 2, 0),
(@product_id, 'uploads/products/backpack-3.jpg', 3, 0);

-- Product 13: Power Bank
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 5, 'Mi Power Bank 20000mAh', 'mi-power-bank-20000mah', 
'High capacity power bank with fast charging. Can charge phone 4-5 times. Dual USB ports. Original Mi product with warranty card. Used for 8 months.', 
1499.00, 25.00, 1124.25, 1, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/powerbank-1.jpg', 1, 1),
(@product_id, 'uploads/products/powerbank-2.jpg', 2, 0);

-- Product 14: Phone Stand
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(2, 5, 'Adjustable Phone Stand Holder', 'adjustable-phone-stand-holder', 
'Universal phone stand for all smartphones. Adjustable viewing angle. Perfect for video calls and watching lectures. Foldable design, easy to carry.', 
299.00, 0.00, 299.00, 6, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/phone-stand-1.jpg', 1, 1);

-- =====================================================
-- Sample Reviews (for demonstration)
-- =====================================================

-- Reviews for Product 1 (Engineering Mathematics)
INSERT INTO product_reviews (product_id, user_id, rating, review_title, review_text, is_verified_purchase, status) VALUES
(1, 2, 5, 'Excellent Book!', 'This book helped me a lot in my first year. Clear explanations and good examples. Highly recommended!', 1, 'approved'),
(1, 2, 4, 'Good Condition', 'Book is in good condition as described. Fast delivery. Worth the price.', 1, 'approved');

-- Reviews for Product 3 (Wireless Mouse)
INSERT INTO product_reviews (product_id, user_id, rating, review_title, review_text, is_verified_purchase, status) VALUES
(3, 2, 5, 'Great Mouse!', 'Works perfectly, no lag. Battery life is amazing. Great value for money.', 1, 'approved');
