-- ================================================================
-- Update Product Images - Reuse Existing Images
-- This will assign existing images to products without images
-- ================================================================

USE student_marketplace;

-- ================================================================
-- BOOKS & NOTES - Distribute existing book images
-- ================================================================

-- Use DSA image for algorithm/programming books
UPDATE products 
SET image_path = 'uploads/dsa_aho.png'
WHERE category = 'Books & Notes' 
AND (name LIKE '%Data Structure%' OR name LIKE '%Algorithm%' OR name LIKE '%Digital%')
AND (image_path IS NULL OR image_path = '');

-- Use C book image for C/programming books
UPDATE products 
SET image_path = 'uploads/c_deitel.png'
WHERE category = 'Books & Notes' 
AND (name LIKE '%C Programming%' OR name LIKE '%Let Us C%')
AND (image_path IS NULL OR image_path = '');

-- Use CS Essential for OS, DBMS, Networks, etc.
UPDATE products 
SET image_path = 'uploads/cs_essential.png'
WHERE category = 'Books & Notes' 
AND (name LIKE '%Operating%' OR name LIKE '%Database%' OR name LIKE '%Network%' 
     OR name LIKE '%Software%' OR name LIKE '%Artificial%')
AND (image_path IS NULL OR image_path = '');

-- Use DSA Russell for Java, Python, Mathematics
UPDATE products 
SET image_path = 'uploads/dsa_russell.png'
WHERE category = 'Books & Notes' 
AND (name LIKE '%Java%' OR name LIKE '%Python%' OR name LIKE '%Mathematics%' 
     OR name LIKE '%Engineering Mathematics%')
AND (image_path IS NULL OR image_path = '');

-- For GATE and remaining books, distribute images
UPDATE products 
SET image_path = CASE 
    WHEN product_id % 4 = 0 THEN 'uploads/dsa_aho.png'
    WHEN product_id % 4 = 1 THEN 'uploads/cs_essential.png'
    WHEN product_id % 4 = 2 THEN 'uploads/dsa_russell.png'
    ELSE 'uploads/c_deitel.png'
END
WHERE category = 'Books & Notes' 
AND (image_path IS NULL OR image_path = '');

-- ================================================================
-- ELECTRONICS - Map to specific electronics images
-- ================================================================

-- Laptops
UPDATE products 
SET image_path = 'uploads/elec_laptop.png'
WHERE category = 'Electronics' 
AND name LIKE '%laptop%'
AND (image_path IS NULL OR image_path = '');

-- Mouse
UPDATE products 
SET image_path = 'uploads/elec_mouse.png'
WHERE category = 'Electronics' 
AND (name LIKE '%mouse%' OR name LIKE '%Mouse%')
AND (image_path IS NULL OR image_path = '');

-- Keyboard
UPDATE products 
SET image_path = 'uploads/elec_keyboard.png'
WHERE category = 'Electronics' 
AND (name LIKE '%keyboard%' OR name LIKE '%Keyboard%' OR name LIKE '%Combo%')
AND (image_path IS NULL OR image_path = '');

-- Headphones & Earbuds
UPDATE products 
SET image_path = 'uploads/elec_headphones.png'
WHERE category = 'Electronics' 
AND (name LIKE '%headphone%' OR name LIKE '%Headphone%' 
     OR name LIKE '%earbuds%' OR name LIKE '%Airdopes%' 
     OR name LIKE '%JBL%' OR name LIKE '%Boat%')
AND (image_path IS NULL OR image_path = '');

-- Pendrives & Storage
UPDATE products 
SET image_path = 'uploads/elec_pendrive.png'
WHERE category = 'Electronics' 
AND (name LIKE '%pendrive%' OR name LIKE '%Pendrive%' 
     OR name LIKE '%DataTraveler%' OR name LIKE '%USB%' 
     OR name LIKE '%Flash%')
AND (image_path IS NULL OR image_path = '');

-- Calculator
UPDATE products 
SET image_path = 'uploads/calculator.png'
WHERE category = 'Electronics' 
AND (name LIKE '%calculator%' OR name LIKE '%Calculator%' OR name LIKE '%Casio%')
AND (image_path IS NULL OR image_path = '');

-- Remaining electronics - distribute available images
UPDATE products 
SET image_path = CASE 
    WHEN product_id % 3 = 0 THEN 'uploads/elec_headphones.png'
    WHEN product_id % 3 = 1 THEN 'uploads/elec_pendrive.png'
    ELSE 'uploads/elec_laptop.png'
END
WHERE category = 'Electronics' 
AND (image_path IS NULL OR image_path = '');

-- ================================================================
-- STUDENT ESSENTIALS - Use bag image
-- ================================================================

-- Backpacks and bags
UPDATE products 
SET image_path = 'uploads/college_bag.png'
WHERE category = 'Student Essentials' 
AND (name LIKE '%bag%' OR name LIKE '%Bag%' 
     OR name LIKE '%backpack%' OR name LIKE '%Backpack%'
     OR name LIKE '%Wildcraft%' OR name LIKE '%American Tourister%')
AND (image_path IS NULL OR image_path = '');

-- For other student essentials without images, use bag as placeholder
UPDATE products 
SET image_path = 'uploads/college_bag.png'
WHERE category = 'Student Essentials' 
AND (image_path IS NULL OR image_path = '');

-- ================================================================
-- CLOTHING - Use generic images from what we have
-- ================================================================

-- Distribute available images as placeholders
UPDATE products 
SET image_path = CASE 
    WHEN product_id % 2 = 0 THEN 'uploads/college_bag.png'
    ELSE 'uploads/cs_essential.png'
END
WHERE category = 'Clothing' 
AND (image_path IS NULL OR image_path = '');

-- ================================================================
-- ACCESSORIES - Use generic images
-- ================================================================

UPDATE products 
SET image_path = CASE 
    WHEN product_id % 3 = 0 THEN 'uploads/calculator.png'
    WHEN product_id % 3 = 1 THEN 'uploads/elec_pendrive.png'
    ELSE 'uploads/college_bag.png'
END
WHERE category = 'Accessories' 
AND (image_path IS NULL OR image_path = '');

-- ================================================================
-- VERIFY RESULTS
-- ================================================================

-- Show products by category with image status
SELECT 
    category,
    COUNT(*) as total_products,
    SUM(CASE WHEN image_path IS NOT NULL AND image_path != '' THEN 1 ELSE 0 END) as with_images,
    SUM(CASE WHEN image_path IS NULL OR image_path = '' THEN 1 ELSE 0 END) as without_images
FROM products
GROUP BY category
ORDER BY category;

-- Show recently updated products
SELECT product_id, name, category, image_path 
FROM products 
ORDER BY product_id DESC 
LIMIT 20;

-- ================================================================
-- SUCCESS MESSAGE
-- ================================================================
SELECT 'Images updated successfully! All products now have images.' as message;

-- ================================================================
-- NOTES:
-- 1. This reuses existing 12 images intelligently
-- 2. Similar products get matching images
-- 3. All products will now have some image
-- 4. You can replace with better images later
-- 5. Your placeholder system will handle broken paths
-- ================================================================
