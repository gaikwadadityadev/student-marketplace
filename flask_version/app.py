"""
Student Marketplace - Flask Application
Main application file with all routes and business logic
Final Year Project - Well-commented for viva
"""

import os
import bcrypt
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_cors import CORS
from sqlalchemy import create_engine, text
from werkzeug.utils import secure_filename
from config import Config

# =====================================================
# Initialize Flask Application
# =====================================================
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.config.from_object(Config)
app.secret_key = app.config.get('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', '*')}})

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database engine (using SQLAlchemy for connection management)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_pre_ping=True)

# =====================================================
# Helper Functions
# =====================================================

def allowed_file(filename):
    """Check if file extension is allowed for upload"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def hash_password(password):
    """Hash password using bcrypt for security"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def login_required(f):
    """Decorator to check if user is logged in"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def calculate_average_rating(product_id):
    """Calculate average rating for a product"""
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT 
                    AVG(rating) as avg_rating,
                    COUNT(*) as review_count
                FROM product_reviews 
                WHERE product_id = :product_id AND status = 'approved'
            """)
            result = conn.execute(query, {'product_id': product_id}).mappings().first()
            if result and result['avg_rating']:
                return {
                    'average': round(float(result['avg_rating']), 1),
                    'count': int(result['review_count'])
                }
    except Exception as e:
        print(f"Error calculating rating: {e}")
    return {'average': 0.0, 'count': 0}

def has_user_reviewed(product_id, user_id):
    """Check if user has already reviewed a product (one review per user)"""
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT COUNT(*) as count 
                FROM product_reviews 
                WHERE product_id = :product_id AND user_id = :user_id
            """)
            result = conn.execute(query, {'product_id': product_id, 'user_id': user_id}).mappings().first()
            return result['count'] > 0
    except Exception as e:
        print(f"Error checking review: {e}")
    return False

# =====================================================
# Routes - Home & Product Listing
# =====================================================

@app.route('/')
def index():
    """Home page - Shows featured products"""
    try:
        with engine.connect() as conn:
            # Get featured products (approved, ordered by views)
            query = text("""
                SELECT 
                    p.*,
                    c.category_name,
                    c.category_slug,
                    (SELECT image_path FROM product_images 
                     WHERE product_id = p.product_id AND is_primary = 1 LIMIT 1) as primary_image
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                WHERE p.status = 'approved'
                ORDER BY p.views_count DESC, p.created_at DESC
                LIMIT 8
            """)
            products = conn.execute(query).mappings().all()
            
            # Calculate ratings for each product
            for product in products:
                rating = calculate_average_rating(product['product_id'])
                product['avg_rating'] = rating['average']
                product['review_count'] = rating['count']
            
            return render_template('index.html', products=products)
    except Exception as e:
        print(f"Error in index: {e}")
        return render_template('index.html', products=[])

@app.route('/products')
def products():
    """Product listing page with search and filters (Flipkart-style)"""
    try:
        # Get filter parameters from query string
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        min_price = request.args.get('min_price', '0')
        max_price = request.args.get('max_price', '0')
        min_rating = request.args.get('min_rating', '0')
        sort_by = request.args.get('sort', 'newest')  # newest, price_low, price_high, rating
        page = request.args.get('page', 1, type=int)
        
        # Convert to appropriate types
        try:
            min_price = float(min_price) if min_price else 0
            max_price = float(max_price) if max_price else 0
            min_rating = float(min_rating) if min_rating else 0
        except ValueError:
            min_price = max_price = min_rating = 0
        
        with engine.connect() as conn:
            # Build WHERE clause dynamically
            where_conditions = ["p.status = 'approved'"]
            params = {}
            
            # Search filter
            if search:
                where_conditions.append("(p.product_name LIKE :search OR p.description LIKE :search)")
                params['search'] = f"%{search}%"
            
            # Category filter
            if category:
                where_conditions.append("c.category_slug = :category")
                params['category'] = category
            
            # Price filters
            if min_price > 0:
                where_conditions.append("p.discounted_price >= :min_price")
                params['min_price'] = min_price
            if max_price > 0:
                where_conditions.append("p.discounted_price <= :max_price")
                params['max_price'] = max_price
            
            where_clause = " AND ".join(where_conditions)
            
            # Sort order
            order_by = "ORDER BY p.created_at DESC"
            if sort_by == 'price_low':
                order_by = "ORDER BY p.discounted_price ASC"
            elif sort_by == 'price_high':
                order_by = "ORDER BY p.discounted_price DESC"
            elif sort_by == 'rating':
                order_by = "ORDER BY avg_rating DESC"
            
            # Get products with ratings
            query = text(f"""
                SELECT 
                    p.*,
                    c.category_name,
                    c.category_slug,
                    COALESCE(AVG(pr.rating), 0) as avg_rating,
                    COUNT(DISTINCT pr.review_id) as review_count,
                    (SELECT image_path FROM product_images 
                     WHERE product_id = p.product_id AND is_primary = 1 LIMIT 1) as primary_image
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN product_reviews pr ON p.product_id = pr.product_id AND pr.status = 'approved'
                WHERE {where_clause}
                GROUP BY p.product_id
                HAVING avg_rating >= :min_rating
                {order_by}
                LIMIT :limit OFFSET :offset
            """)
            
            params['min_rating'] = min_rating
            params['limit'] = app.config['PRODUCTS_PER_PAGE']
            params['offset'] = (page - 1) * app.config['PRODUCTS_PER_PAGE']
            
            products = conn.execute(query, params).mappings().all()
            
            # Get total count for pagination
            count_query = text(f"""
                SELECT COUNT(DISTINCT p.product_id) as total
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN product_reviews pr ON p.product_id = pr.product_id AND pr.status = 'approved'
                WHERE {where_clause}
                GROUP BY p.product_id
                HAVING COALESCE(AVG(pr.rating), 0) >= :min_rating
            """)
            count_params = {k: v for k, v in params.items() if k not in ['limit', 'offset']}
            total_result = conn.execute(count_query, count_params).fetchall()
            total = len(total_result)
            
            # Get all categories for filter
            categories_query = text("SELECT * FROM categories ORDER BY category_name")
            categories = conn.execute(categories_query).mappings().all()
            
            # Format products
            for product in products:
                product['avg_rating'] = round(float(product['avg_rating']), 1)
            
            return render_template('products.html', 
                                 products=products,
                                 categories=categories,
                                 search=search,
                                 category=category,
                                 min_price=min_price,
                                 max_price=max_price,
                                 min_rating=min_rating,
                                 sort_by=sort_by,
                                 page=page,
                                 total_pages=(total + app.config['PRODUCTS_PER_PAGE'] - 1) // app.config['PRODUCTS_PER_PAGE'])
    except Exception as e:
        print(f"Error in products: {e}")
        return render_template('products.html', products=[], categories=[])

@app.route('/product/<slug>')
def product_detail(slug):
    """Product detail page with image gallery and reviews"""
    try:
        with engine.connect() as conn:
            # Get product details
            query = text("""
                SELECT 
                    p.*,
                    c.category_name,
                    c.category_slug,
                    u.username as seller_name,
                    u.full_name as seller_full_name
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN users u ON p.seller_id = u.user_id
                WHERE p.product_slug = :slug AND p.status = 'approved'
            """)
            product = conn.execute(query, {'slug': slug}).mappings().first()
            
            if not product:
                flash('Product not found', 'danger')
                return redirect(url_for('products'))
            
            # Get all product images
            images_query = text("""
                SELECT image_id, image_path, image_order, is_primary
                FROM product_images
                WHERE product_id = :product_id
                ORDER BY image_order ASC, is_primary DESC
            """)
            images = conn.execute(images_query, {'product_id': product['product_id']}).mappings().all()
            
            if not images:
                # If no images, add placeholder
                images = [{'image_path': 'placeholder.jpg', 'is_primary': 1}]
            
            # Get average rating
            rating = calculate_average_rating(product['product_id'])
            product['avg_rating'] = rating['average']
            product['review_count'] = rating['count']
            
            # Get reviews
            reviews_query = text("""
                SELECT 
                    pr.*,
                    u.username,
                    u.full_name,
                    DATE_FORMAT(pr.created_at, '%d %M %Y') as review_date
                FROM product_reviews pr
                LEFT JOIN users u ON pr.user_id = u.user_id
                WHERE pr.product_id = :product_id AND pr.status = 'approved'
                ORDER BY pr.created_at DESC
                LIMIT 10
            """)
            reviews = conn.execute(reviews_query, {'product_id': product['product_id']}).mappings().all()
            
            # Get rating distribution
            dist_query = text("""
                SELECT rating, COUNT(*) as count
                FROM product_reviews
                WHERE product_id = :product_id AND status = 'approved'
                GROUP BY rating
                ORDER BY rating DESC
            """)
            distribution = conn.execute(dist_query, {'product_id': product['product_id']}).mappings().all()
            rating_dist = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
            for dist in distribution:
                rating_dist[dist['rating']] = dist['count']
            
            # Check if user has reviewed
            user_reviewed = False
            if 'user_id' in session:
                user_reviewed = has_user_reviewed(product['product_id'], session['user_id'])
            
            # Update view count
            update_views = text("UPDATE products SET views_count = views_count + 1 WHERE product_id = :product_id")
            conn.execute(update_views, {'product_id': product['product_id']})
            conn.commit()
            
            return render_template('product_detail.html',
                                 product=product,
                                 images=images,
                                 reviews=reviews,
                                 rating_dist=rating_dist,
                                 user_reviewed=user_reviewed)
    except Exception as e:
        print(f"Error in product_detail: {e}")
        flash('Error loading product', 'danger')
        return redirect(url_for('products'))

# =====================================================
# Routes - User Authentication
# =====================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # Validation
        if not all([username, email, password, full_name]):
            flash('All required fields must be filled', 'danger')
            return render_template('register.html')
        
        try:
            with engine.connect() as conn:
                # Check if username or email already exists
                check_query = text("SELECT user_id FROM users WHERE username = :username OR email = :email")
                existing = conn.execute(check_query, {'username': username, 'email': email}).mappings().first()
                
                if existing:
                    flash('Username or email already exists', 'danger')
                    return render_template('register.html')
                
                # Insert new user
                insert_query = text("""
                    INSERT INTO users (username, email, password, full_name, phone, role, status)
                    VALUES (:username, :email, :password, :full_name, :phone, 'student', 'active')
                """)
                hashed_password = hash_password(password)
                conn.execute(insert_query, {
                    'username': username,
                    'email': email,
                    'password': hashed_password,
                    'full_name': full_name,
                    'phone': phone
                })
                conn.commit()
                
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
        except Exception as e:
            print(f"Registration error: {e}")
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required', 'danger')
            return render_template('login.html')
        
        try:
            with engine.connect() as conn:
                query = text("SELECT user_id, username, email, password, role, status FROM users WHERE username = :username")
                user = conn.execute(query, {'username': username}).mappings().first()
                
                if user and check_password(password, user['password']):
                    if user['status'] == 'blocked':
                        flash('Your account has been blocked. Contact admin.', 'danger')
                        return render_template('login.html')
                    
                    # Set session
                    session['user_id'] = user['user_id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    session['email'] = user['email']
                    
                    flash('Login successful!', 'success')
                    return redirect(url_for('index'))
                else:
                    flash('Invalid username or password', 'danger')
        except Exception as e:
            print(f"Login error: {e}")
            flash('Login failed. Please try again.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))

# =====================================================
# Routes - Reviews & Ratings
# =====================================================

@app.route('/product/<slug>/review', methods=['POST'])
@login_required
def submit_review(slug):
    """Submit a product review (one review per user)"""
    try:
        rating = int(request.form.get('rating', 0))
        review_title = request.form.get('review_title', '').strip()
        review_text = request.form.get('review_text', '').strip()
        
        # Validation
        if rating < 1 or rating > 5:
            flash('Rating must be between 1 and 5', 'danger')
            return redirect(url_for('product_detail', slug=slug))
        
        if not review_text:
            flash('Review text is required', 'danger')
            return redirect(url_for('product_detail', slug=slug))
        
        with engine.connect() as conn:
            # Get product ID
            product_query = text("SELECT product_id FROM products WHERE product_slug = :slug")
            product = conn.execute(product_query, {'slug': slug}).mappings().first()
            
            if not product:
                flash('Product not found', 'danger')
                return redirect(url_for('products'))
            
            product_id = product['product_id']
            
            # Check if user has already reviewed
            if has_user_reviewed(product_id, session['user_id']):
                flash('You have already reviewed this product', 'warning')
                return redirect(url_for('product_detail', slug=slug))
            
            # Insert review
            insert_query = text("""
                INSERT INTO product_reviews 
                (product_id, user_id, rating, review_title, review_text, status)
                VALUES (:product_id, :user_id, :rating, :review_title, :review_text, 'approved')
            """)
            conn.execute(insert_query, {
                'product_id': product_id,
                'user_id': session['user_id'],
                'rating': rating,
                'review_title': review_title,
                'review_text': review_text
            })
            conn.commit()
            
            flash('Review submitted successfully!', 'success')
            return redirect(url_for('product_detail', slug=slug))
    except Exception as e:
        print(f"Review submission error: {e}")
        flash('Failed to submit review. Please try again.', 'danger')
        return redirect(url_for('product_detail', slug=slug))

# =====================================================
# API Routes (for AJAX)
# =====================================================

@app.route('/api/products')
def api_products():
    """API endpoint for products (for AJAX requests)"""
    try:
        search = request.args.get('search', '').strip()
        category = request.args.get('category', '').strip()
        
        with engine.connect() as conn:
            where_conditions = ["p.status = 'approved'"]
            params = {}
            
            if search:
                where_conditions.append("(p.product_name LIKE :search OR p.description LIKE :search)")
                params['search'] = f"%{search}%"
            
            if category:
                where_conditions.append("c.category_slug = :category")
                params['category'] = category
            
            where_clause = " AND ".join(where_conditions)
            
            query = text(f"""
                SELECT 
                    p.*,
                    c.category_name,
                    c.category_slug,
                    COALESCE(AVG(pr.rating), 0) as avg_rating,
                    (SELECT image_path FROM product_images 
                     WHERE product_id = p.product_id AND is_primary = 1 LIMIT 1) as primary_image
                FROM products p
                LEFT JOIN categories c ON p.category_id = c.category_id
                LEFT JOIN product_reviews pr ON p.product_id = pr.product_id AND pr.status = 'approved'
                WHERE {where_clause}
                GROUP BY p.product_id
                ORDER BY p.created_at DESC
                LIMIT 20
            """)
            
            products = conn.execute(query, params).mappings().all()
            
            # Format for JSON
            for product in products:
                product['avg_rating'] = round(float(product['avg_rating']), 1)
                product['price'] = float(product['price'])
                product['discounted_price'] = float(product['discounted_price'])
            
            return jsonify({'success': True, 'products': list(products)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# =====================================================
# Error Handlers
# =====================================================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

# =====================================================
# Run Application
# =====================================================

if __name__ == '__main__':
    # Run in debug mode for development
    # Change to False in production
    app.run(host='0.0.0.0', port=5000, debug=True)
