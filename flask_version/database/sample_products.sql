-- =====================================================
-- Sample Student Products Data
-- Realistic products for students
-- =====================================================
USE student_marketplace_flask;

-- Clear existing dummy products (optional)
-- DELETE FROM product_images WHERE product_id IN (SELECT product_id FROM products WHERE seller_id = 1);
-- DELETE FROM product_reviews WHERE product_id IN (SELECT product_id FROM products WHERE seller_id = 1);
-- DELETE FROM products WHERE seller_id = 1;

-- =====================================================
-- BOOKS CATEGORY
-- =====================================================

-- Product 1: Engineering Mathematics
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 1, 'Engineering Mathematics Volume 1 - Grewal', 'engineering-mathematics-volume-1-grewal', 
'Complete guide to Engineering Mathematics for first year students. Covers calculus, algebra, and differential equations. Used but in excellent condition with minimal highlighting. Perfect for exam preparation and assignments.', 
450.00, 10.00, 405.00, 3, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/eng-math-cover.jpg', 1, 1),
(@product_id, 'uploads/products/eng-math-pages.jpg', 2, 0);

-- Product 2: Data Structures Book
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 1, 'Data Structures and Algorithms in C++ - Goodrich', 'data-structures-algorithms-cpp-goodrich', 
'Comprehensive textbook on data structures and algorithms. Includes arrays, linked lists, trees, graphs, and sorting algorithms. Previous edition but content is still relevant. No torn pages, all chapters intact.', 
650.00, 15.00, 552.50, 2, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/dsa-book-cover.jpg', 1, 1),
(@product_id, 'uploads/products/dsa-book-content.jpg', 2, 0);

-- Product 3: Database Systems Book
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 1, 'Database System Concepts - Silberschatz', 'database-system-concepts-silberschatz', 
'Standard textbook for database courses. Covers SQL, normalization, transactions, and database design. Used for one semester, excellent condition. Perfect for DBMS course.', 
750.00, 12.00, 660.00, 1, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/db-book-cover.jpg', 1, 1);

-- =====================================================
-- ELECTRONICS CATEGORY
-- =====================================================

-- Product 4: Wireless Mouse
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 2, 'Logitech M170 Wireless Mouse', 'logitech-m170-wireless-mouse', 
'Compact wireless mouse perfect for laptops and coding. 2.4GHz wireless connection, 12-month battery life. Used for 6 months, working perfectly. Original packaging and USB receiver included.', 
599.00, 20.00, 479.20, 1, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/mouse-front.jpg', 1, 1),
(@product_id, 'uploads/products/mouse-back.jpg', 2, 0);

-- Product 5: USB Flash Drive
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 2, 'SanDisk 32GB USB 3.0 Flash Drive', 'sandisk-32gb-usb-3-flash-drive', 
'High-speed USB 3.0 flash drive with 32GB storage capacity. Perfect for storing assignments, projects, presentations, and study materials. Brand new, sealed pack with warranty.', 
450.00, 5.00, 427.50, 5, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/usb-drive.jpg', 1, 1);

-- Product 6: Laptop Stand
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 2, 'Adjustable Aluminum Laptop Stand', 'adjustable-aluminum-laptop-stand', 
'Ergonomic laptop stand with adjustable height (5 levels). Fits laptops up to 17 inches. Improves posture during long coding and study sessions. Lightweight aluminum, portable design.', 
899.00, 25.00, 674.25, 2, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/laptop-stand-front.jpg', 1, 1),
(@product_id, 'uploads/products/laptop-stand-side.jpg', 2, 0);

-- Product 7: Keyboard
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 2, 'HP USB Keyboard (Wired)', 'hp-usb-keyboard-wired', 
'Standard USB keyboard perfect for desktop setup. Spill-resistant design, comfortable typing. Used for 1 year, all keys working perfectly. Great for programming and assignments.', 
699.00, 30.00, 489.30, 1, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/keyboard-top.jpg', 1, 1);

-- =====================================================
-- STATIONERY CATEGORY
-- =====================================================

-- Product 8: Notebook Set
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 3, 'Classmate Notebook Set (5 Pack - 200 Pages Each)', 'classmate-notebook-set-5-pack', 
'Set of 5 Classmate notebooks, 200 pages each. Ruled pages, perfect for taking class notes and assignments. Unused, brand new. Great value for money. Durable covers.', 
250.00, 0.00, 250.00, 8, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/notebooks-pack.jpg', 1, 1);

-- Product 9: Pen Set
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 3, 'Reynolds Gel Pen Set (10 Pens - Assorted Colors)', 'reynolds-gel-pen-set-10-pens', 
'Pack of 10 Reynolds gel pens in assorted colors (blue, black, red, green). Smooth writing, no smudging. Perfect for exams, assignments, and note-taking. Brand new, sealed pack.', 
120.00, 0.00, 120.00, 12, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/pens-pack.jpg', 1, 1);

-- Product 10: Scientific Calculator
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 3, 'Casio FX-991EX Scientific Calculator', 'casio-fx-991ex-scientific-calculator', 
'Advanced scientific calculator with 552 functions. Solar powered with battery backup. Allowed in engineering exams (GATE, IES, etc.). Used but in excellent condition with original manual and case.', 
1299.00, 30.00, 909.30, 1, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/calculator-front.jpg', 1, 1),
(@product_id, 'uploads/products/calculator-back.jpg', 2, 0);

-- Product 11: Geometry Box
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 3, 'Camel Geometry Box Set', 'camel-geometry-box-set', 
'Complete geometry box with compass, protractor, ruler, and other tools. Durable plastic case. Perfect for engineering drawing and mathematics. Brand new, unused.', 
150.00, 0.00, 150.00, 6, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/geometry-box.jpg', 1, 1);

-- =====================================================
-- HOSTEL ITEMS CATEGORY
-- =====================================================

-- Product 12: Study Table Lamp
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 4, 'LED Study Table Lamp with USB Port', 'led-study-table-lamp-usb', 
'Adjustable LED desk lamp with 3 brightness levels and 3 color modes (warm, cool, natural). USB charging port for phone. Perfect for late-night study sessions. Energy efficient, eye-friendly lighting.', 
799.00, 15.00, 679.15, 3, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/lamp-front.jpg', 1, 1),
(@product_id, 'uploads/products/lamp-on.jpg', 2, 0);

-- Product 13: Storage Box
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 4, 'Plastic Storage Box with Lid (40L)', 'plastic-storage-box-40l', 
'Large storage box for organizing hostel room. Durable plastic, stackable design. Perfect for storing books, clothes, and other items. Transparent lid for easy identification. Brand new.', 
450.00, 10.00, 405.00, 4, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/storage-box.jpg', 1, 1);

-- Product 14: Bed Sheet Set
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 4, 'Cotton Bed Sheet Set (Single Bed)', 'cotton-bed-sheet-set-single', 
'Comfortable cotton bed sheet set for single bed. Includes 1 bed sheet and 1 pillow cover. Soft fabric, easy to wash. Used but clean and in good condition. No stains or tears.', 
599.00, 20.00, 479.20, 2, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/bedsheet-set.jpg', 1, 1);

-- Product 15: Hanger Set
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 4, 'Plastic Hanger Set (10 Pieces)', 'plastic-hanger-set-10-pieces', 
'Set of 10 durable plastic hangers for clothes. Space-saving design, perfect for hostel wardrobe. Strong construction, won\'t break easily. Brand new, unused.', 
200.00, 0.00, 200.00, 10, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/hangers-pack.jpg', 1, 1);

-- =====================================================
-- ACCESSORIES CATEGORY
-- =====================================================

-- Product 16: Backpack
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 5, 'Skybags Backpack (30L) - Laptop Compartment', 'skybags-backpack-30l-laptop', 
'Durable laptop backpack with padded compartment for laptop up to 15.6 inches. Multiple pockets for organization. Water-resistant material. Used for 1 year, still in great condition. No tears or broken zippers.', 
1299.00, 35.00, 844.35, 1, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/backpack-front.jpg', 1, 1),
(@product_id, 'uploads/products/backpack-side.jpg', 2, 0),
(@product_id, 'uploads/products/backpack-interior.jpg', 3, 0);

-- Product 17: Power Bank
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 5, 'Mi Power Bank 20000mAh - Fast Charging', 'mi-power-bank-20000mah-fast-charging', 
'High capacity power bank with fast charging support. Can charge phone 4-5 times. Dual USB ports (2.4A output). Original Mi product with warranty card. Used for 8 months, working perfectly.', 
1499.00, 25.00, 1124.25, 1, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/powerbank-front.jpg', 1, 1),
(@product_id, 'uploads/products/powerbank-back.jpg', 2, 0);

-- Product 18: Phone Stand
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 5, 'Adjustable Phone Stand Holder - Universal', 'adjustable-phone-stand-holder-universal', 
'Universal phone stand for all smartphones (4-7 inches). Adjustable viewing angle (0-90 degrees). Perfect for video calls, online classes, and watching lectures. Foldable design, easy to carry.', 
299.00, 0.00, 299.00, 6, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/phone-stand.jpg', 1, 1);

-- Product 19: USB Hub
INSERT INTO products (seller_id, category_id, product_name, product_slug, description, price, discount_percent, discounted_price, stock_quantity, status) VALUES
(1, 5, 'USB 3.0 Hub (4 Ports)', 'usb-3-0-hub-4-ports', 
'4-port USB 3.0 hub for connecting multiple devices. High-speed data transfer. Perfect for laptops with limited USB ports. Plug and play, no drivers needed. Brand new, sealed.', 
499.00, 10.00, 449.10, 3, 'approved');

SET @product_id = LAST_INSERT_ID();
INSERT INTO product_images (product_id, image_path, image_order, is_primary) VALUES
(@product_id, 'uploads/products/usb-hub.jpg', 1, 1);

-- =====================================================
-- Sample Reviews (for demonstration)
-- =====================================================

-- Reviews for Product 1 (Engineering Mathematics)
INSERT INTO product_reviews (product_id, user_id, rating, review_title, review_text, is_verified_purchase, status) VALUES
(1, 1, 5, 'Excellent Book!', 'This book helped me a lot in my first year. Clear explanations and good examples. Highly recommended for engineering students!', 1, 'approved'),
(1, 1, 4, 'Good Condition', 'Book is in good condition as described. Fast delivery. Worth the price. Some pages have highlighting but that\'s fine.', 1, 'approved');

-- Reviews for Product 4 (Wireless Mouse)
INSERT INTO product_reviews (product_id, user_id, rating, review_title, review_text, is_verified_purchase, status) VALUES
(4, 1, 5, 'Great Mouse!', 'Works perfectly, no lag. Battery life is amazing. Great value for money. Perfect for coding and general use.', 1, 'approved');

-- Reviews for Product 10 (Calculator)
INSERT INTO product_reviews (product_id, user_id, rating, review_title, review_text, is_verified_purchase, status) VALUES
(10, 1, 5, 'Perfect for Exams', 'This calculator is allowed in GATE and other engineering exams. All functions working perfectly. Good condition.', 1, 'approved');
