<?php
/**
 * Reviews API Endpoint
 * Handles product reviews and ratings
 */

require_once '../config/config.php';
require_once '../includes/functions.php';

header('Content-Type: application/json');

// Get database connection
global $db;

// Check if user is logged in
if (!isLoggedIn()) {
    http_response_code(401);
    echo json_encode(['success' => false, 'error' => 'Please login to submit a review']);
    exit();
}

$action = $_GET['action'] ?? $_POST['action'] ?? 'list';
$method = $_SERVER['REQUEST_METHOD'];

try {
    switch ($action) {
        case 'list':
            // Get reviews for a product
            $productId = (int)($_GET['product_id'] ?? 0);
            
            if ($productId <= 0) {
                throw new Exception('Product ID required');
            }
            
            $page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
            $limit = 10;
            $offset = ($page - 1) * $limit;
            
            $stmt = $db->prepare("
                SELECT 
                    pr.*,
                    u.username,
                    u.full_name,
                    DATE_FORMAT(pr.created_at, '%d %M %Y') as review_date
                FROM product_reviews pr
                LEFT JOIN users u ON pr.user_id = u.user_id
                WHERE pr.product_id = ? AND pr.status = 'approved'
                ORDER BY pr.created_at DESC
                LIMIT ? OFFSET ?
            ");
            $stmt->execute([$productId, $limit, $offset]);
            $reviews = $stmt->fetchAll();
            
            // Get total count
            $countStmt = $db->prepare("
                SELECT COUNT(*) as total
                FROM product_reviews
                WHERE product_id = ? AND status = 'approved'
            ");
            $countStmt->execute([$productId]);
            $total = $countStmt->fetch()['total'];
            
            // Get rating distribution
            $distStmt = $db->prepare("
                SELECT rating, COUNT(*) as count
                FROM product_reviews
                WHERE product_id = ? AND status = 'approved'
                GROUP BY rating
                ORDER BY rating DESC
            ");
            $distStmt->execute([$productId]);
            $distribution = $distStmt->fetchAll();
            
            // Format distribution
            $ratingDist = [5 => 0, 4 => 0, 3 => 0, 2 => 0, 1 => 0];
            foreach ($distribution as $dist) {
                $ratingDist[$dist['rating']] = (int)$dist['count'];
            }
            
            echo json_encode([
                'success' => true,
                'reviews' => $reviews,
                'pagination' => [
                    'current_page' => $page,
                    'per_page' => $limit,
                    'total' => $total,
                    'total_pages' => ceil($total / $limit)
                ],
                'rating_distribution' => $ratingDist
            ]);
            break;
            
        case 'submit':
            // Submit a new review
            if ($method !== 'POST') {
                throw new Exception('POST method required');
            }
            
            $productId = (int)($_POST['product_id'] ?? 0);
            $rating = (int)($_POST['rating'] ?? 0);
            $reviewTitle = sanitize($_POST['review_title'] ?? '');
            $reviewText = sanitize($_POST['review_text'] ?? '');
            
            // Validation
            if ($productId <= 0) {
                throw new Exception('Invalid product ID');
            }
            
            if ($rating < 1 || $rating > 5) {
                throw new Exception('Rating must be between 1 and 5');
            }
            
            if (empty($reviewText)) {
                throw new Exception('Review text is required');
            }
            
            // Check if product exists
            $stmt = $db->prepare("SELECT product_id FROM products WHERE product_id = ? AND status = 'approved'");
            $stmt->execute([$productId]);
            if (!$stmt->fetch()) {
                throw new Exception('Product not found');
            }
            
            // Check if user has already reviewed
            if (hasUserReviewed($productId, $_SESSION['user_id'], $db)) {
                throw new Exception('You have already reviewed this product');
            }
            
            // Insert review
            $stmt = $db->prepare("
                INSERT INTO product_reviews 
                (product_id, user_id, rating, review_title, review_text, is_verified_purchase, status)
                VALUES (?, ?, ?, ?, ?, 0, 'approved')
            ");
            $stmt->execute([
                $productId,
                $_SESSION['user_id'],
                $rating,
                $reviewTitle,
                $reviewText
            ]);
            
            echo json_encode([
                'success' => true,
                'message' => 'Review submitted successfully',
                'review_id' => $db->lastInsertId()
            ]);
            break;
            
        case 'helpful':
            // Mark review as helpful
            if ($method !== 'POST') {
                throw new Exception('POST method required');
            }
            
            $reviewId = (int)($_POST['review_id'] ?? 0);
            
            if ($reviewId <= 0) {
                throw new Exception('Invalid review ID');
            }
            
            $stmt = $db->prepare("
                UPDATE product_reviews 
                SET helpful_count = helpful_count + 1 
                WHERE review_id = ?
            ");
            $stmt->execute([$reviewId]);
            
            echo json_encode([
                'success' => true,
                'message' => 'Thank you for your feedback'
            ]);
            break;
            
        default:
            throw new Exception('Invalid action');
    }
    
} catch (Exception $e) {
    http_response_code(400);
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ]);
}
