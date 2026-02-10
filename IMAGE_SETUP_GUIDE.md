# Product Image Setup Guide

## Overview

This guide explains how product images are handled in the Student Marketplace application and how to fix any image path issues.

## Image Storage Structure

- **Upload Directory:** `static/uploads/`
- **Database Path Format:** `uploads/filename.jpg` (relative to static folder)
- **URL Format:** `/static/uploads/filename.jpg`

## How Images Work

1. **When Uploading:** Images are saved to `static/uploads/` with a filename like: `{user_id}_{timestamp}_{original_filename}`
2. **In Database:** The `image_path` field stores: `uploads/filename.jpg`
3. **In Templates:** Images are displayed using the `product_image` filter which normalizes paths automatically

## Fixing Image Paths

### Step 1: Run the Image Path Fixer Script

```bash
cd backend
python fix_image_paths.py
```

This script will:
- Check all products in the database
- Normalize image paths to the correct format (`uploads/filename.jpg`)
- Verify that image files actually exist
- Update incorrect paths in the database
- Report any missing images

### Step 2: List Available Images

To see all images in the uploads folder:

```bash
cd backend
python fix_image_paths.py --list
```

### Step 3: Verify Images Display Correctly

1. Start the Flask application:
   ```bash
   python backend/app.py
   ```

2. Open your browser and go to: http://localhost:5000/products

3. Check if all product images are displaying correctly

## Common Issues and Solutions

### Issue 1: Images Not Displaying

**Symptoms:** Product cards show placeholder icons instead of images

**Solution:**
1. Run the fix script: `python backend/fix_image_paths.py`
2. Check if image files exist in `static/uploads/`
3. Verify database paths are in format `uploads/filename.jpg`

### Issue 2: Broken Image Paths

**Symptoms:** 404 errors when loading images

**Possible Causes:**
- Image file was deleted but database still has the path
- Path format is incorrect (e.g., `static/uploads/` instead of `uploads/`)
- File was moved but database wasn't updated

**Solution:**
1. Run the fix script to normalize paths
2. If images are missing, either:
   - Re-upload the images through the product edit page
   - Delete products with missing images
   - Update products to remove image paths

### Issue 3: Images Uploaded But Not Showing

**Symptoms:** Image uploads successfully but doesn't display

**Solution:**
1. Check the uploads folder: `static/uploads/`
2. Verify the file was created
3. Check database: `SELECT product_id, name, image_path FROM products WHERE product_id = ?;`
4. Ensure path is `uploads/filename.jpg` (not `static/uploads/...`)

## Manual Database Fix

If you need to manually fix image paths in the database:

```sql
-- Connect to MySQL
mysql -u root -p
USE student_marketplace;

-- View current image paths
SELECT product_id, name, image_path FROM products;

-- Fix a specific product's image path
UPDATE products 
SET image_path = 'uploads/filename.jpg' 
WHERE product_id = 1;

-- Fix all paths that start with 'static/'
UPDATE products 
SET image_path = REPLACE(image_path, 'static/uploads/', 'uploads/') 
WHERE image_path LIKE 'static/uploads/%';

-- Fix paths that don't start with 'uploads/'
UPDATE products 
SET image_path = CONCAT('uploads/', SUBSTRING_INDEX(image_path, '/', -1)) 
WHERE image_path NOT LIKE 'uploads/%' AND image_path IS NOT NULL;
```

## Adding Images to Existing Products

### Method 1: Through Web Interface (Recommended)

1. Login as the product owner
2. Go to Dashboard
3. Click "Edit" on the product
4. Upload a new image
5. Save changes

### Method 2: Direct File Upload + Database Update

1. Copy image file to `static/uploads/` folder
2. Rename it to: `{user_id}_{timestamp}_{original_name}.jpg`
3. Update database:
   ```sql
   UPDATE products 
   SET image_path = 'uploads/your_filename.jpg' 
   WHERE product_id = ?;
   ```

## Image Path Normalization

The application uses a custom Jinja2 filter `product_image` that automatically:
- Converts backslashes to forward slashes
- Removes leading slashes
- Ensures path starts with `uploads/`
- Generates correct URL using Flask's `url_for('static', filename=...)`

**Example:**
- Database: `uploads/product.jpg` → URL: `/static/uploads/product.jpg`
- Database: `static/uploads/product.jpg` → URL: `/static/uploads/product.jpg` (normalized)
- Database: `product.jpg` → URL: `/static/uploads/product.jpg` (normalized)

## Best Practices

1. **Always use the web interface** to upload images (ensures correct paths)
2. **Run the fix script periodically** to check for issues
3. **Keep image filenames unique** (the system adds user_id and timestamp)
4. **Use supported formats:** PNG, JPG, JPEG, GIF, WEBP
5. **Max file size:** 16MB (configured in `config.py`)

## Testing Image Display

1. **Upload a test product** with an image
2. **Check the database:**
   ```sql
   SELECT product_id, name, image_path FROM products ORDER BY product_id DESC LIMIT 1;
   ```
3. **Verify file exists:**
   ```bash
   ls -la static/uploads/ | grep filename
   ```
4. **Check URL in browser:**
   - Go to: http://localhost:5000/products
   - Right-click on image → Inspect
   - Verify the image URL is correct

## Troubleshooting Commands

```bash
# List all images in uploads folder
python backend/fix_image_paths.py --list

# Fix all image paths
python backend/fix_image_paths.py

# Check Flask app is running
python backend/app.py

# Check database connection
python backend/test_mysql_connection.py
```

## Support

If you encounter issues:
1. Check the Flask console for error messages
2. Verify MySQL is running
3. Check file permissions on `static/uploads/` folder
4. Ensure image files are not corrupted
5. Review the fix script output for specific errors

---

**Note:** The image path fixer script is safe to run multiple times. It only updates paths that need fixing and doesn't modify correct paths.

