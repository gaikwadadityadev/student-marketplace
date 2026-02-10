<?php
/**
 * Common Functions
 * Student Marketplace - PHP Version
 */

/**
 * Sanitize input data
 * @param string $data
 * @return string
 */
function sanitize($data) {
    $data = trim($data);
    $data = stripslashes($data);
    $data = htmlspecialchars($data, ENT_QUOTES, 'UTF-8');
    return $data;
}

/**
 * Check if user is logged in
 * @return bool
 */
function isLoggedIn() {
    return isset($_SESSION['user_id']);
}

/**
 * Check if user is admin
 * @return bool
 */
function isAdmin() {
    return isset($_SESSION['role']) && $_SESSION['role'] === 'admin';
}

/**
 * Redirect to a page
 * @param string $url
 */
function redirect($url) {
    header("Location: " . $url);
    exit();
}

/**
 * Format price with currency
 * @param float $price
 * @return string
 */
function formatPrice($price) {
    return '₹' . number_format($price, 2);
}

/**
 * Calculate discount percentage
 * @param float $original
 * @param float $discounted
 * @return float
 */
function calculateDiscount($original, $discounted) {
    if ($original <= 0) return 0;
    return round((($original - $discounted) / $original) * 100, 2);
}

/**
 * Generate product slug from name
 * @param string $name
 * @return string
 */
function generateSlug($name) {
    $slug = strtolower($name);
    $slug = preg_replace('/[^a-z0-9]+/', '-', $slug);
    $slug = trim($slug, '-');
    return $slug;
}

/**
 * Validate image file
 * @param array $file
 * @return array ['valid' => bool, 'error' => string]
 */
function validateImage($file) {
    $result = ['valid' => false, 'error' => ''];
    
    if (!isset($file['tmp_name']) || !is_uploaded_file($file['tmp_name'])) {
        $result['error'] = 'No file uploaded';
        return $result;
    }
    
    // Check file size
    if ($file['size'] > MAX_FILE_SIZE) {
        $result['error'] = 'File size exceeds 5MB limit';
        return $result;
    }
    
    // Check file extension
    $ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    if (!in_array($ext, ALLOWED_EXTENSIONS)) {
        $result['error'] = 'Invalid file type. Allowed: ' . implode(', ', ALLOWED_EXTENSIONS);
        return $result;
    }
    
    // Check if it's actually an image
    $imageInfo = @getimagesize($file['tmp_name']);
    if ($imageInfo === false) {
        $result['error'] = 'File is not a valid image';
        return $result;
    }
    
    $result['valid'] = true;
    return $result;
}

/**
 * Upload product image
 * @param array $file
 * @param int $productId
 * @return array ['success' => bool, 'path' => string, 'error' => string]
 */
function uploadProductImage($file, $productId) {
    $result = ['success' => false, 'path' => '', 'error' => ''];
    
    // Validate image
    $validation = validateImage($file);
    if (!$validation['valid']) {
        $result['error'] = $validation['error'];
        return $result;
    }
    
    // Create upload directory if it doesn't exist
    if (!file_exists(UPLOAD_DIR)) {
        mkdir(UPLOAD_DIR, 0777, true);
    }
    
    // Generate unique filename
    $ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
    $filename = 'product_' . $productId . '_' . time() . '_' . rand(1000, 9999) . '.' . $ext;
    $filepath = UPLOAD_DIR . $filename;
    
    // Move uploaded file
    if (move_uploaded_file($file['tmp_name'], $filepath)) {
        $result['success'] = true;
        $result['path'] = 'uploads/products/' . $filename;
    } else {
        $result['error'] = 'Failed to upload file';
    }
    
    return $result;
}

/**
 * Calculate average rating for a product
 * @param int $productId
 * @param PDO $db
 * @return array ['average' => float, 'count' => int]
 */
function calculateAverageRating($productId, $db) {
    $stmt = $db->prepare("
        SELECT 
            AVG(rating) as average_rating,
            COUNT(*) as review_count
        FROM product_reviews 
        WHERE product_id = ? AND status = 'approved'
    ");
    $stmt->execute([$productId]);
    $result = $stmt->fetch();
    
    return [
        'average' => round($result['average_rating'] ?? 0, 1),
        'count' => $result['review_count'] ?? 0
    ];
}

/**
 * Check if user has already reviewed a product
 * @param int $productId
 * @param int $userId
 * @param PDO $db
 * @return bool
 */
function hasUserReviewed($productId, $userId, $db) {
    $stmt = $db->prepare("
        SELECT COUNT(*) as count 
        FROM product_reviews 
        WHERE product_id = ? AND user_id = ?
    ");
    $stmt->execute([$productId, $userId]);
    $result = $stmt->fetch();
    return $result['count'] > 0;
}

/**
 * Generate star rating HTML
 * @param float $rating
 * @return string
 */
function generateStarRating($rating) {
    $fullStars = floor($rating);
    $halfStar = ($rating - $fullStars) >= 0.5;
    $emptyStars = 5 - $fullStars - ($halfStar ? 1 : 0);
    
    $html = '<div class="star-rating">';
    
    // Full stars
    for ($i = 0; $i < $fullStars; $i++) {
        $html .= '<i class="bi bi-star-fill text-warning"></i>';
    }
    
    // Half star
    if ($halfStar) {
        $html .= '<i class="bi bi-star-half text-warning"></i>';
    }
    
    // Empty stars
    for ($i = 0; $i < $emptyStars; $i++) {
        $html .= '<i class="bi bi-star text-warning"></i>';
    }
    
    $html .= '</div>';
    return $html;
}
