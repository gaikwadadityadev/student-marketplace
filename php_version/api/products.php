<?php
/**
 * Products API Endpoint
 * Handles product listing, search, and filtering
 */

require_once '../config/config.php';
require_once '../includes/functions.php';

header('Content-Type: application/json');

// Get database connection
global $db;

// Get request parameters
$action = $_GET['action'] ?? 'list';
$page = isset($_GET['page']) ? (int)$_GET['page'] : 1;
$limit = PRODUCTS_PER_PAGE;
$offset = ($page - 1) * $limit;

try {
    switch ($action) {
        case 'list':
            // Get filter parameters
            $category = $_GET['category'] ?? '';
            $minPrice = isset($_GET['min_price']) ? (float)$_GET['min_price'] : 0;
            $maxPrice = isset($_GET['max_price']) ? (float)$_GET['max_price'] : 0;
            $minRating = isset($_GET['min_rating']) ? (float)$_GET['min_rating'] : 0;
            $search = $_GET['search'] ?? '';
            $sort = $_GET['sort'] ?? 'newest'; // newest, price_low, price_high, rating
            
            // Build query
            $where = ["p.status = 'approved'"];
            $params = [];
            
            // Category filter
            if (!empty($category)) {
                $where[] = "c.category_slug = ?";
                $params[] = $category;
            }
            
            // Price filter
            if ($minPrice > 0) {
                $where[] = "p.discounted_price >= ?";
                $params[] = $minPrice;
            }
            if ($maxPrice > 0) {
                $where[] = "p.discounted_price <= ?";
                $params[] = $maxPrice;
            }
            
            // Search filter
            if (!empty($search)) {
                $where[] = "(p.product_name LIKE ? OR p.description LIKE ?)";
                $searchTerm = "%$search%";
                $params[] = $searchTerm;
                $params[] = $searchTerm;
            }
            
            $whereClause = implode(' AND ', $where);
            
            // Rating filter (using subquery)
            $ratingFilter = '';
            if ($minRating > 0) {
                $ratingFilter = "HAVING avg_rating >= ?";
                $params[] = $minRating;
            }
            
            // Sort order
            $orderBy = "ORDER BY p.created_at DESC";
            switch ($sort) {
                case 'price_low':
                    $orderBy = "ORDER BY p.discounted_price ASC";
                    break;
                case 'price_high':
                    $orderBy = "ORDER BY p.discounted_price DESC";
                    break;
                case 'rating':
                    $orderBy = "ORDER BY avg_rating DESC";
                    break;
            }
            
            // Get products with ratings
            $sql = "
                SELECT 
                    p.*,
                    c.category_name,
                    c.category_slug,
                    u.username as seller_name,
                    COALESCE(AVG(pr.rating), 0) as avg_rating,
                    COUNT(DISTINCT pr.review_id) as review_count,
                    (SELECT image_path FROM product_images WHERE product_id = p.product_id AND is_primary = 1 LIMIT 1) as primary_image
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN users u ON p.seller_id = u.user_id
                LEFT JOIN product_reviews pr ON p.product_id = pr.product_id AND pr.status = 'approved'
                WHERE $whereClause
                GROUP BY p.product_id
                $ratingFilter
                $orderBy
                LIMIT ? OFFSET ?
            ";
            
            $params[] = $limit;
            $params[] = $offset;
            
            $stmt = $db->prepare($sql);
            $stmt->execute($params);
            $products = $stmt->fetchAll();
            
            // Get total count for pagination
            $countSql = "
                SELECT COUNT(DISTINCT p.product_id) as total
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN product_reviews pr ON p.product_id = pr.product_id AND pr.status = 'approved'
                WHERE $whereClause
            ";
            
            $countParams = array_slice($params, 0, -2); // Remove limit and offset
            $countStmt = $db->prepare($countSql);
            $countStmt->execute($countParams);
            $total = $countStmt->fetch()['total'];
            
            // Format products
            foreach ($products as &$product) {
                $product['avg_rating'] = round((float)$product['avg_rating'], 1);
                $product['price'] = (float)$product['price'];
                $product['discounted_price'] = (float)$product['discounted_price'];
                $product['discount_percent'] = (float)$product['discount_percent'];
                $product['stock_quantity'] = (int)$product['stock_quantity'];
            }
            
            echo json_encode([
                'success' => true,
                'products' => $products,
                'pagination' => [
                    'current_page' => $page,
                    'per_page' => $limit,
                    'total' => $total,
                    'total_pages' => ceil($total / $limit)
                ]
            ]);
            break;
            
        case 'detail':
            $productId = (int)($_GET['id'] ?? 0);
            $slug = $_GET['slug'] ?? '';
            
            if ($productId <= 0 && empty($slug)) {
                throw new Exception('Product ID or slug required');
            }
            
            // Get product details
            if ($productId > 0) {
                $stmt = $db->prepare("
                    SELECT 
                        p.*,
                        c.category_name,
                        c.category_slug,
                        u.username as seller_name,
                        u.full_name as seller_full_name
                    FROM products p
                    LEFT JOIN categories c ON p.category_id = c.category_id
                    LEFT JOIN users u ON p.seller_id = u.user_id
                    WHERE p.product_id = ? AND p.status = 'approved'
                ");
                $stmt->execute([$productId]);
            } else {
                $stmt = $db->prepare("
                    SELECT 
                        p.*,
                        c.category_name,
                        c.category_slug,
                        u.username as seller_name,
                        u.full_name as seller_full_name
                    FROM products p
                    LEFT JOIN categories c ON p.category_id = c.category_id
                    LEFT JOIN users u ON p.seller_id = u.user_id
                    WHERE p.product_slug = ? AND p.status = 'approved'
                ");
                $stmt->execute([$slug]);
            }
            
            $product = $stmt->fetch();
            
            if (!$product) {
                throw new Exception('Product not found');
            }
            
            // Get product images
            $stmt = $db->prepare("
                SELECT image_id, image_path, image_order, is_primary
                FROM product_images
                WHERE product_id = ?
                ORDER BY image_order ASC, is_primary DESC
            ");
            $stmt->execute([$product['product_id']]);
            $product['images'] = $stmt->fetchAll();
            
            // Get average rating
            $rating = calculateAverageRating($product['product_id'], $db);
            $product['avg_rating'] = $rating['average'];
            $product['review_count'] = $rating['count'];
            
            // Update view count
            $stmt = $db->prepare("UPDATE products SET views_count = views_count + 1 WHERE product_id = ?");
            $stmt->execute([$product['product_id']]);
            
            // Format prices
            $product['price'] = (float)$product['price'];
            $product['discounted_price'] = (float)$product['discounted_price'];
            $product['discount_percent'] = (float)$product['discount_percent'];
            $product['stock_quantity'] = (int)$product['stock_quantity'];
            
            echo json_encode([
                'success' => true,
                'product' => $product
            ]);
            break;
            
        case 'categories':
            // Get all categories
            $stmt = $db->prepare("
                SELECT 
                    c.*,
                    COUNT(p.product_id) as product_count
                FROM categories c
                LEFT JOIN products p ON c.category_id = p.category_id AND p.status = 'approved'
                GROUP BY c.category_id
                ORDER BY c.category_name ASC
            ");
            $stmt->execute();
            $categories = $stmt->fetchAll();
            
            echo json_encode([
                'success' => true,
                'categories' => $categories
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
