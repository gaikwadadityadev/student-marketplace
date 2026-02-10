<?php
/**
 * Application Configuration
 * Student Marketplace - PHP Version
 */

// Start session if not already started
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

// Base URL configuration
define('BASE_URL', 'http://localhost/student-marketplace-php/');
define('BASE_PATH', __DIR__ . '/../');

// Upload configuration
define('UPLOAD_DIR', BASE_PATH . 'uploads/products/');
define('UPLOAD_URL', BASE_URL . 'uploads/products/');
define('MAX_FILE_SIZE', 5 * 1024 * 1024); // 5MB
define('ALLOWED_EXTENSIONS', ['jpg', 'jpeg', 'png', 'webp']);

// Pagination
define('PRODUCTS_PER_PAGE', 12);

// Image settings
define('MAX_IMAGES_PER_PRODUCT', 5);
define('THUMBNAIL_WIDTH', 300);
define('THUMBNAIL_HEIGHT', 300);

// Timezone
date_default_timezone_set('Asia/Kolkata');

// Error reporting (disable in production)
error_reporting(E_ALL);
ini_set('display_errors', 1);

// Include database connection
require_once __DIR__ . '/database.php';
