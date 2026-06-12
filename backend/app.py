"""
Student Marketplace - Flask Backend Application
Main application file with all routes and business logic
"""
import os
import re
import bcrypt
from datetime import datetime
import traceback
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory
from flask_cors import CORS
from sqlalchemy import create_engine, text
from werkzeug.utils import secure_filename
from config import Config

# Initialize Flask app
app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.config.from_object(Config)
app.secret_key = app.config.get('SECRET_KEY', 'dev-secret-key-change-in-production')
CORS(app, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', '*')}})

# Add custom Jinja2 filter for product images
@app.template_filter('product_image')
def product_image_filter(image_path):
    """Jinja2 filter to get product image URL"""
    if not image_path:
        return None
    # Normalize path
    normalized_path = image_path.replace('\\', '/')
    if normalized_path.startswith('/'):
        normalized_path = normalized_path[1:]
    if not normalized_path.startswith('uploads/'):
        if 'uploads/' in normalized_path:
            normalized_path = 'uploads/' + normalized_path.split('uploads/')[-1]
        else:
            normalized_path = 'uploads/' + normalized_path
    return url_for('static', filename=normalized_path)

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
PRODUCTS_UPLOAD_DIR = os.path.join(app.config['UPLOAD_FOLDER'], 'products')
os.makedirs(PRODUCTS_UPLOAD_DIR, exist_ok=True)

# Database engine — add SSL connect_args for PostgreSQL
_db_uri = app.config['SQLALCHEMY_DATABASE_URI']
_engine_kwargs = {'pool_pre_ping': True}
if _db_uri.startswith('postgresql'):
    _engine_kwargs['connect_args'] = {'sslmode': 'require'}
engine = create_engine(_db_uri, **_engine_kwargs)
print(f'[OK] Engine created: dialect={engine.dialect.name}, db={_db_uri[:40]}...')


# ==================== AUTO TABLE CREATION + ADMIN SEED ====================
def create_all_tables():
    """Create all database tables if they don't exist. Runs on startup."""
    try:
        dialect = engine.dialect.name
        with engine.connect() as conn:
            if dialect == 'mysql':
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INT PRIMARY KEY AUTO_INCREMENT,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        full_name VARCHAR(100) NOT NULL,
                        phone VARCHAR(20),
                        college_id VARCHAR(20),
                        role ENUM('student','admin') DEFAULT 'student',
                        status ENUM('active','blocked') DEFAULT 'active',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        INDEX idx_email (email),
                        INDEX idx_username (username)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS products (
                        product_id INT PRIMARY KEY AUTO_INCREMENT,
                        seller_id INT NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        description TEXT,
                        price DECIMAL(10,2) NOT NULL,
                        category VARCHAR(50),
                        stock INT DEFAULT 0,
                        image_path VARCHAR(255),
                        status ENUM('pending','approved','rejected') DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        FOREIGN KEY (seller_id) REFERENCES users(user_id) ON DELETE CASCADE,
                        INDEX idx_status (status),
                        INDEX idx_category (category)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS cart (
                        cart_id INT PRIMARY KEY AUTO_INCREMENT,
                        user_id INT NOT NULL,
                        product_id INT NOT NULL,
                        quantity INT DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
                        UNIQUE KEY unique_cart_item (user_id, product_id)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id INT PRIMARY KEY AUTO_INCREMENT,
                        buyer_id INT NOT NULL,
                        total_amount DECIMAL(10,2) NOT NULL,
                        status ENUM('pending','approved','rejected','completed','cancelled') DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        address TEXT,
                        city VARCHAR(100),
                        zip_code VARCHAR(20),
                        FOREIGN KEY (buyer_id) REFERENCES users(user_id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS order_items (
                        order_item_id INT PRIMARY KEY AUTO_INCREMENT,
                        order_id INT NOT NULL,
                        product_id INT NOT NULL,
                        quantity INT NOT NULL,
                        price DECIMAL(10,2) NOT NULL,
                        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS product_reviews (
                        review_id INT PRIMARY KEY AUTO_INCREMENT,
                        product_id INT NOT NULL,
                        user_id INT NOT NULL,
                        rating INT NOT NULL,
                        review_title VARCHAR(255),
                        review_text TEXT,
                        status ENUM('pending','approved','rejected') DEFAULT 'approved',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
                """))
            elif dialect == 'postgresql':
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id SERIAL PRIMARY KEY,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        full_name VARCHAR(100) NOT NULL,
                        phone VARCHAR(20),
                        college_id VARCHAR(20),
                        role VARCHAR(20) DEFAULT 'student',
                        status VARCHAR(20) DEFAULT 'active',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS products (
                        product_id SERIAL PRIMARY KEY,
                        seller_id INT NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        description TEXT,
                        price DECIMAL(10,2) NOT NULL,
                        category VARCHAR(50),
                        stock INT DEFAULT 0,
                        image_path VARCHAR(255),
                        status VARCHAR(20) DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (seller_id) REFERENCES users(user_id) ON DELETE CASCADE
                    )
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS cart (
                        cart_id SERIAL PRIMARY KEY,
                        user_id INT NOT NULL,
                        product_id INT NOT NULL,
                        quantity INT DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
                        UNIQUE (user_id, product_id)
                    )
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id SERIAL PRIMARY KEY,
                        buyer_id INT NOT NULL,
                        total_amount DECIMAL(10,2) NOT NULL,
                        status VARCHAR(20) DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        address TEXT,
                        city VARCHAR(100),
                        zip_code VARCHAR(20),
                        FOREIGN KEY (buyer_id) REFERENCES users(user_id) ON DELETE CASCADE
                    )
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS order_items (
                        order_item_id SERIAL PRIMARY KEY,
                        order_id INT NOT NULL,
                        product_id INT NOT NULL,
                        quantity INT NOT NULL,
                        price DECIMAL(10,2) NOT NULL,
                        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
                    )
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS product_reviews (
                        review_id SERIAL PRIMARY KEY,
                        product_id INT NOT NULL,
                        user_id INT NOT NULL,
                        rating INT NOT NULL,
                        review_title VARCHAR(255),
                        review_text TEXT,
                        status VARCHAR(20) DEFAULT 'approved',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    )
                """))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_email ON users (email)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_username ON users (username)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_products_status ON products (status)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_products_category ON products (category)"))
            else: # sqlite
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username VARCHAR(50) UNIQUE NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        full_name VARCHAR(100) NOT NULL,
                        phone VARCHAR(20),
                        college_id VARCHAR(20),
                        role VARCHAR(20) DEFAULT 'student',
                        status VARCHAR(20) DEFAULT 'active',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS products (
                        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        seller_id INT NOT NULL,
                        name VARCHAR(255) NOT NULL,
                        description TEXT,
                        price DECIMAL(10,2) NOT NULL,
                        category VARCHAR(50),
                        stock INT DEFAULT 0,
                        image_path VARCHAR(255),
                        status VARCHAR(20) DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (seller_id) REFERENCES users(user_id) ON DELETE CASCADE
                    )
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS cart (
                        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INT NOT NULL,
                        product_id INT NOT NULL,
                        quantity INT DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
                        UNIQUE (user_id, product_id)
                    )
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS orders (
                        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        buyer_id INT NOT NULL,
                        total_amount DECIMAL(10,2) NOT NULL,
                        status VARCHAR(20) DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        address TEXT,
                        city VARCHAR(100),
                        zip_code VARCHAR(20),
                        FOREIGN KEY (buyer_id) REFERENCES users(user_id) ON DELETE CASCADE
                    )
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS order_items (
                        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        order_id INT NOT NULL,
                        product_id INT NOT NULL,
                        quantity INT NOT NULL,
                        price DECIMAL(10,2) NOT NULL,
                        FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE,
                        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE
                    )
                """))
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS product_reviews (
                        review_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        product_id INT NOT NULL,
                        user_id INT NOT NULL,
                        rating INT NOT NULL,
                        review_title VARCHAR(255),
                        review_text TEXT,
                        status VARCHAR(20) DEFAULT 'approved',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (product_id) REFERENCES products(product_id) ON DELETE CASCADE,
                        FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                    )
                """))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_email ON users (email)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_users_username ON users (username)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_products_status ON products (status)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS idx_products_category ON products (category)"))

            # Auto-migrate: Add missing columns if they don't exist (fails silently if they do)
            try:
                conn.execute(text("ALTER TABLE orders ADD COLUMN address TEXT"))
            except Exception:
                pass
            
            try:
                conn.execute(text("ALTER TABLE orders ADD COLUMN city VARCHAR(100)"))
            except Exception:
                pass
                
            try:
                conn.execute(text("ALTER TABLE orders ADD COLUMN zip_code VARCHAR(20)"))
            except Exception:
                pass

            conn.commit()
            print('[OK] Database tables created/verified successfully')

            # ── Auto-seed/sync admin user ───────────────────────────
            admin_user = os.getenv('ADMIN_USERNAME', 'Aditya')
            admin_pass = os.getenv('ADMIN_PASSWORD', 'Aditya@2103')
            admin_email = os.getenv('ADMIN_EMAIL', 'admin@marketplace.com')

            existing_admin = conn.execute(
                text("SELECT user_id FROM users WHERE username = :username"),
                {'username': admin_user}
            ).mappings().first()

            hashed = bcrypt.hashpw(
                admin_pass.encode('utf-8'), bcrypt.gensalt()
            ).decode('utf-8')

            if not existing_admin:
                conn.execute(text("""
                    INSERT INTO users (username, email, password, full_name, role, status)
                    VALUES (:username, :email, :password, :full_name, 'admin', 'active')
                """), {
                    'username':  admin_user,
                    'email':     admin_email,
                    'password':  hashed,
                    'full_name': admin_user,
                })
                conn.commit()
                print(f'[OK] Admin user "{admin_user}" created automatically')
            else:
                conn.execute(text("""
                    UPDATE users
                    SET email = :email, password = :password, role = 'admin', status = 'active'
                    WHERE username = :username
                """), {
                    'username':  admin_user,
                    'email':     admin_email,
                    'password':  hashed,
                })
                conn.commit()
                print(f'[OK] Admin user "{admin_user}" credentials synced/updated')

    except Exception as e:
        print(f'[WARN] Startup DB warning: {e}')
        import traceback as _tb
        _tb.print_exc()


# Run table creation + admin seed on every startup
create_all_tables()



def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def hash_password(password):
    """Hash password using bcrypt"""
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


def admin_required(f):
    """Decorator to check if user is admin"""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash('Admin access required', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


# ==================== HELPER FUNCTIONS FOR REVIEWS ====================
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
    """Check if user has already reviewed a product"""
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

# ==================== LANDING / HOME PAGE ====================
@app.route('/')
def index():
    """Landing/Home page"""
    try:
        with engine.connect() as conn:
            # Get approved products for display
            # Get approved products for display with ratings
            query = text("""
                SELECT 
                    p.*, 
                    u.username, 
                    u.full_name,
                    COALESCE((SELECT AVG(rating) FROM product_reviews WHERE product_id = p.product_id AND status = 'approved'), 0) as avg_rating,
                    (SELECT COUNT(*) FROM product_reviews WHERE product_id = p.product_id AND status = 'approved') as review_count
                FROM products p 
                JOIN users u ON p.seller_id = u.user_id 
                WHERE p.status = 'approved' 
                ORDER BY p.created_at DESC 
                LIMIT 8
            """)
            products = conn.execute(query).mappings().all()
            
            # Format ratings
            products_list = []
            for p in products:
                prod = dict(p)
                prod['avg_rating'] = round(float(prod['avg_rating']), 1)
                products_list.append(prod)
            
            return render_template('index.html', products=products_list)
    except Exception as e:
        print(f"Error in index: {e}")
        return render_template('index.html', products=[])


@app.route('/db-test')
def db_test():
    import urllib.parse
    info = {
        'database_uri_configured': app.config.get('SQLALCHEMY_DATABASE_URI'),
        'dialect': engine.dialect.name,
        'error': None,
        'traceback': None,
        'test_query_result': None,
        'tables': []
    }
    if info['database_uri_configured']:
        try:
            # Simple obfuscation of credentials
            parsed = urllib.parse.urlsplit(info['database_uri_configured'])
            if parsed.password:
                obfuscated_netloc = parsed.netloc.replace(parsed.password, '********')
                info['database_uri_configured'] = parsed._replace(netloc=obfuscated_netloc).geturl()
        except Exception:
            pass
    try:
        with engine.connect() as conn:
            res = conn.execute(text("SELECT 1")).scalar()
            info['test_query_result'] = res
            if engine.dialect.name == 'postgresql':
                tables_res = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")).all()
            elif engine.dialect.name == 'mysql':
                tables_res = conn.execute(text("SHOW TABLES")).all()
            else:
                tables_res = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).all()
            info['tables'] = [row[0] for row in tables_res]
    except Exception as e:
        info['error'] = str(e)
        info['traceback'] = traceback.format_exc()
    return jsonify(info)


@app.route('/version')
def version():
    import subprocess
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=os.path.dirname(__file__)).decode().strip()
    except Exception:
        commit = 'unavailable'
    return jsonify({
        'commit': commit,
        'db_dialect': engine.dialect.name,
        'db_uri_prefix': app.config['SQLALCHEMY_DATABASE_URI'][:50],
        'deploy_timestamp': '2026-06-08T17:45-commit-5'
    })


@app.route('/admin-check')
def admin_check():
    """Debug route: verify admin user exists and password is correct."""
    result = {'admin_found': False, 'password_ok': False, 'error': None, 'user': None}
    try:
        with engine.connect() as conn:
            row = conn.execute(
                text("SELECT user_id, username, role, status, password FROM users WHERE role='admin'")
            ).mappings().first()
            if row:
                u = dict(row)
                result['admin_found'] = True
                result['user'] = {
                    'user_id': u['user_id'],
                    'username': u['username'],
                    'role': u['role'],
                    'status': u['status'],
                    'hash_prefix': u['password'][:20] + '...'
                }
                admin_pass = os.getenv('ADMIN_PASSWORD', 'Aditya@2103')
                result['password_ok'] = check_password(admin_pass, u['password'])
                result['env_admin_password_used'] = admin_pass
    except Exception as e:
        result['error'] = str(e)
    return jsonify(result)


# ==================== STUDENT REGISTRATION ====================
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Student registration page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()
        college_id = request.form.get('college_id', '').strip()
        
        # Validation
        if not all([username, email, password, full_name]):
            flash('All fields are required', 'danger')
            return render_template('register.html')
        
        # College ID validation: 12 digits starting with 2023-2026 (or empty = skip)
        if college_id and not re.match(r'^(202[3-6])\d{8}$', college_id):
            flash('Invalid College ID. Must be 12 digits starting with 2023, 2024, 2025, or 2026.', 'danger')
            return render_template('register.html')
        
        try:
            with engine.connect() as conn:
                # Check if username or email already exists
                check_query = text("SELECT user_id FROM users WHERE username = :username OR email = :email")
                existing = conn.execute(check_query, {'username': username, 'email': email}).mappings().first()
                
                if existing:
                    flash('Username or email already exists', 'danger')
                    return render_template('register.html')
                
                # Insert new user with prepared statement
                insert_query = text("""
                    INSERT INTO users (username, email, password, full_name, phone, college_id, role, status)
                    VALUES (:username, :email, :password, :full_name, :phone, :college_id, 'student', 'active')
                """)
                hashed_password = hash_password(password)
                conn.execute(insert_query, {
                    'username': username,
                    'email': email,
                    'password': hashed_password,
                    'full_name': full_name,
                    'phone': phone,
                    'college_id': college_id
                })
                conn.commit()
                
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('login'))
        except Exception as e:
            print(f"Registration error: {e}")
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('register.html')


# ==================== STUDENT LOGIN ====================
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Student login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required', 'danger')
            return render_template('login.html')
        
        try:
            with engine.connect() as conn:
                # Get user with prepared statement
                query = text("SELECT user_id, username, email, password, role, status FROM users WHERE username = :username")
                user_result = conn.execute(query, {'username': username}).mappings().first()
                
                if user_result and check_password(password, user_result['password']):
                    user = dict(user_result)
                    if user['status'] == 'blocked':
                        flash('Your account has been blocked. Contact admin.', 'danger')
                        return render_template('login.html')
                    
                    # Set session
                    session.permanent = True
                    session['user_id'] = user['user_id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    session['email'] = user['email']
                    
                    if user['role'] == 'admin':
                        return redirect(url_for('admin_dashboard'))
                    else:
                        return redirect(url_for('dashboard'))
                else:
                    flash('Invalid username or password', 'danger')
        except Exception as e:
            print(f"Login error: {e}")
            flash('Login failed. Please try again.', 'danger')
    
    return render_template('login.html')


# ==================== ADMIN LOGIN ====================
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required', 'danger')
            return render_template('admin_login.html')
        
        try:
            with engine.connect() as conn:
                query = text("""
                    SELECT user_id, username, email, password, role, status 
                    FROM users 
                    WHERE username = :username AND role = 'admin'
                """)
                user_result = conn.execute(query, {'username': username}).mappings().first()
                
                if user_result and check_password(password, user_result['password']):
                    user = dict(user_result)
                    session.permanent = True
                    session['user_id'] = user['user_id']
                    session['username'] = user['username']
                    session['role'] = user['role']
                    session['email'] = user['email']
                    return redirect(url_for('admin_dashboard'))
                else:
                    flash('Invalid admin credentials', 'danger')
        except Exception as e:
            print(f"Admin login error: {e}")
            flash('Login failed. Please try again.', 'danger')
    
    return render_template('admin_login.html')


# ==================== STUDENT DASHBOARD ====================
@app.route('/dashboard')
@login_required
def dashboard():
    """Student dashboard"""
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    try:
        user_id = session.get('user_id')
        
        with engine.connect() as conn:
            # Get user's products
            products_query = text("""
                SELECT * FROM products 
                WHERE seller_id = :user_id 
                ORDER BY created_at DESC
            """)
            my_products_raw = conn.execute(products_query, {'user_id': user_id}).mappings().all()
            my_products = [dict(p) for p in my_products_raw]
            
            # Get user's orders with explicit columns
            orders_query = text("""
                SELECT o.order_id, o.buyer_id, o.total_amount, o.status, o.created_at,
                       COUNT(oi.order_item_id) as item_count
                FROM orders o
                LEFT JOIN order_items oi ON o.order_id = oi.order_id
                WHERE o.buyer_id = :user_id
                GROUP BY o.order_id, o.buyer_id, o.total_amount, o.status, o.created_at
                ORDER BY o.created_at DESC
                LIMIT 10
            """)
            orders_raw = conn.execute(orders_query, {'user_id': user_id}).mappings().all()
            orders = [dict(o) for o in orders_raw]
            
            
            return render_template('dashboard.html', products=my_products, orders=orders)
    except Exception as e:
        print(f"Dashboard error: {e}")
        traceback.print_exc()
        return render_template('dashboard.html', products=[], orders=[])


# ==================== PRODUCT UPLOAD ====================
@app.route('/product/upload', methods=['GET', 'POST'])
@login_required
def product_upload():
    """Product upload page"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        price = request.form.get('price', '0')
        category = request.form.get('category', '').strip()
        stock = request.form.get('stock', '0')
        image = request.files.get('image')
        
        # Validation
        if not all([name, description, price, category]):
            flash('All fields are required', 'danger')
            return render_template('product_upload.html')
        
        try:
            price = float(price)
            if price <= 0:
                flash('Price must be greater than 0', 'danger')
                return render_template('product_upload.html')
                
            stock = int(stock)
            if stock < 0:
                flash('Stock cannot be negative', 'danger')
                return render_template('product_upload.html')
        except ValueError:
            flash('Invalid price or stock', 'danger')
            return render_template('product_upload.html')
        
        # Handle image upload
        image_path = None
        if image and image.filename and allowed_file(image.filename):
            filename = secure_filename(f"{session['user_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.filename}")
            # Ensure products directory exists
            products_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'products')
            os.makedirs(products_dir, exist_ok=True)
            
            file_path = os.path.join(products_dir, filename)
            image.save(file_path)
            # Store relative path for database: uploads/products/filename
            image_path = f"uploads/products/{filename}"
        
        try:
            with engine.connect() as conn:
                # Insert product with prepared statement
                insert_query = text("""
                    INSERT INTO products (seller_id, name, description, price, category, stock, image_path, status)
                    VALUES (:seller_id, :name, :description, :price, :category, :stock, :image_path, 'pending')
                """)
                conn.execute(insert_query, {
                    'seller_id': session['user_id'],
                    'name': name,
                    'description': description,
                    'price': price,
                    'category': category,
                    'stock': stock,
                    'image_path': image_path
                })
                conn.commit()
                
                flash('Product uploaded successfully! Waiting for admin approval.', 'success')
                return redirect(url_for('dashboard'))
        except Exception as e:
            print(f"Product upload error: {e}")
            flash('Failed to upload product. Please try again.', 'danger')
    
    return render_template('product_upload.html')


# ==================== PRODUCT EDIT ====================
@app.route('/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def product_edit(product_id):
    """Edit product page"""
    try:
        with engine.connect() as conn:
            # Get product (only if user is the seller)
            query = text("SELECT * FROM products WHERE product_id = :product_id AND seller_id = :user_id")
            product_result = conn.execute(query, {'product_id': product_id, 'user_id': session['user_id']}).mappings().first()
            
            if not product_result:
                flash('Product not found or you do not have permission', 'danger')
                return redirect(url_for('dashboard'))
            
            product = dict(product_result)
            
            if request.method == 'POST':
                name = request.form.get('name', '').strip()
                description = request.form.get('description', '').strip()
                price = request.form.get('price', '0')
                category = request.form.get('category', '').strip()
                image = request.files.get('image')
                
                if not all([name, description, price, category]):
                    flash('All fields are required', 'danger')
                    return render_template('product_edit.html', product=product)
                
                try:
                    price = float(price)
                except ValueError:
                    flash('Invalid price', 'danger')
                    return render_template('product_edit.html', product=product)
                
                # Handle image upload
                image_path = product.get('image_path')
                if image and image.filename and allowed_file(image.filename):
                    filename = secure_filename(f"{session['user_id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{image.filename}")
                    # Ensure products directory exists
                    products_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'products')
                    os.makedirs(products_dir, exist_ok=True)
                    
                    file_path = os.path.join(products_dir, filename)
                    image.save(file_path)
                    # Store relative path for database: uploads/products/filename
                    image_path = f"uploads/products/{filename}"
                
                # Update product with prepared statement
                update_query = text("""
                    UPDATE products 
                    SET name = :name, description = :description, price = :price, 
                        category = :category, image_path = :image_path, status = 'pending'
                    WHERE product_id = :product_id AND seller_id = :user_id
                """)
                conn.execute(update_query, {
                    'product_id': product_id,
                    'user_id': session['user_id'],
                    'name': name,
                    'description': description,
                    'price': price,
                    'category': category,
                    'image_path': image_path
                })
                conn.commit()
                
                flash('Product updated successfully! Waiting for admin approval.', 'success')
                return redirect(url_for('dashboard'))
            
            return render_template('product_edit.html', product=product)
    except Exception as e:
        print(f"Product edit error: {e}")
        flash('Error loading product', 'danger')
        return redirect(url_for('dashboard'))


# ==================== PRODUCT DELETE ====================
@app.route('/product/delete/<int:product_id>', methods=['POST'])
@login_required
def product_delete(product_id):
    """Delete product"""
    try:
        with engine.connect() as conn:
            # Check if user owns the product
            check_query = text("SELECT product_id FROM products WHERE product_id = :product_id AND seller_id = :user_id")
            product = conn.execute(check_query, {'product_id': product_id, 'user_id': session['user_id']}).mappings().first()
            
            if product:
                delete_query = text("DELETE FROM products WHERE product_id = :product_id")
                conn.execute(delete_query, {'product_id': product_id})
                conn.commit()
                flash('Product deleted successfully', 'success')
            else:
                flash('Product not found or you do not have permission', 'danger')
    except Exception as e:
        print(f"Product delete error: {e}")
        flash('Failed to delete product', 'danger')
    
    return redirect(url_for('dashboard'))


# ==================== PRODUCT SEARCH & VIEW ====================
@app.route('/products')
def products():
    """Product listing page with search"""
    search = request.args.get('search', '').strip()
    category = request.args.get('category', '').strip()
    
    try:
        with engine.connect() as conn:
            # Build query with prepared statement
            query = text("""
                SELECT 
                    p.*, 
                    u.username, 
                    u.full_name,
                    COALESCE((SELECT AVG(rating) FROM product_reviews WHERE product_id = p.product_id AND status = 'approved'), 0) as avg_rating,
                    (SELECT COUNT(*) FROM product_reviews WHERE product_id = p.product_id AND status = 'approved') as review_count
                FROM products p 
                JOIN users u ON p.seller_id = u.user_id 
                WHERE p.status = 'approved'
                AND (:search = '' OR p.name LIKE :search_like OR p.description LIKE :search_like)
                AND (:category = '' OR p.category = :category)
                ORDER BY p.created_at DESC
            """)
            search_like = f"%{search}%"
            products_result = conn.execute(query, {
                'search': search,
                'search_like': search_like,
                'category': category
            }).mappings().all()
            
            # Format output
            products = []
            for p in products_result:
                prod = dict(p)
                prod['avg_rating'] = round(float(prod['avg_rating']), 1)
                products.append(prod)
            
            # Get unique categories
            categories_query = text("SELECT DISTINCT category FROM products WHERE status = 'approved'")
            categories = [row[0] for row in conn.execute(categories_query).fetchall() if row[0]]
            
            return render_template('products.html', products=products, search=search, category=category, categories=categories)
    except Exception as e:
        print(f"Products error: {e}")
        return render_template('products.html', products=[], search=search, category=category, categories=[])


@app.route('/product/<int:product_id>')
def product_view(product_id):
    """View single product"""
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT p.*, u.username, u.full_name, u.email 
                FROM products p 
                JOIN users u ON p.seller_id = u.user_id 
                WHERE p.product_id = :product_id AND p.status = 'approved'
            """)
            product_result = conn.execute(query, {'product_id': product_id}).mappings().first()
            
            if not product_result:
                flash('Product not found', 'danger')
                return redirect(url_for('products'))
            
            product = dict(product_result)
            
            # Get rating info
            rating_info = calculate_average_rating(product_id)
            product['avg_rating'] = rating_info['average']
            product['review_count'] = rating_info['count']
            
            # Get reviews
            reviews_query = text("""
                SELECT 
                    pr.*,
                    u.username,
                    u.full_name
                FROM product_reviews pr
                LEFT JOIN users u ON pr.user_id = u.user_id
                WHERE pr.product_id = :product_id AND pr.status = 'approved'
                ORDER BY pr.created_at DESC
                LIMIT 10
            """)
            reviews_raw = conn.execute(reviews_query, {'product_id': product_id}).mappings().all()
            
            reviews = []
            for r in reviews_raw:
                rev = dict(r)
                dt = rev.get('created_at')
                if dt:
                    if isinstance(dt, str):
                        try:
                            # Standard SQLite datetime string parsing
                            dt = datetime.strptime(dt.split('.')[0], '%Y-%m-%d %H:%M:%S')
                        except Exception:
                            pass
                    if isinstance(dt, datetime):
                        rev['review_date'] = dt.strftime('%d %B %Y')
                    else:
                        rev['review_date'] = str(dt)
                else:
                    rev['review_date'] = ''
                reviews.append(rev)
            
            # Get rating distribution
            dist_query = text("""
                SELECT rating, COUNT(*) as count
                FROM product_reviews
                WHERE product_id = :product_id AND status = 'approved'
                GROUP BY rating
                ORDER BY rating DESC
            """)
            distribution = conn.execute(dist_query, {'product_id': product_id}).mappings().all()
            rating_dist = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
            for dist in distribution:
                rating_dist[dist['rating']] = dist['count']
                
            # Check if user has reviewed
            user_reviewed = False
            if 'user_id' in session:
                user_reviewed = has_user_reviewed(product_id, session['user_id'])
            
            return render_template('product_view.html', 
                                 product=product,
                                 reviews=reviews,
                                 rating_dist=rating_dist,
                                 user_reviewed=user_reviewed)
    except Exception as e:
        print(f"Product view error: {e}")
        flash('Error loading product', 'danger')
        return redirect(url_for('products'))


@app.route('/product/<int:product_id>/review', methods=['POST'])
@login_required
def submit_review(product_id):
    """Submit a product review"""
    try:
        rating = int(request.form.get('rating', 0))
        review_title = request.form.get('review_title', '').strip()
        review_text = request.form.get('review_text', '').strip()
        
        # Validation
        if rating < 1 or rating > 5:
            flash('Rating must be between 1 and 5', 'danger')
            return redirect(url_for('product_view', product_id=product_id))
        
        with engine.connect() as conn:
            # Check if user has already reviewed
            if has_user_reviewed(product_id, session['user_id']):
                flash('You have already reviewed this product', 'warning')
                return redirect(url_for('product_view', product_id=product_id))
            
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
            return redirect(url_for('product_view', product_id=product_id))
            
    except Exception as e:
        print(f"Review submission error: {e}")
        flash('Failed to submit review. Please try again.', 'danger')
        return redirect(url_for('product_view', product_id=product_id))


# ==================== CART OPERATIONS ====================
@app.route('/cart')
@login_required
def cart():
    """View cart"""
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT c.*, p.name, p.price, p.image_path, p.product_id,
                       (c.quantity * p.price) as total
                FROM cart c
                JOIN products p ON c.product_id = p.product_id
                WHERE c.user_id = :user_id AND p.status = 'approved'
            """)
            cart_items = conn.execute(query, {'user_id': session['user_id']}).mappings().all()
            
            total = sum(float(item.total) for item in cart_items)
            
            return render_template('cart.html', cart_items=cart_items, total=total)
    except Exception as e:
        print(f"Cart error: {e}")
        return render_template('cart.html', cart_items=[], total=0)


@app.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def cart_add(product_id):
    """Add product to cart"""
    try:
        with engine.connect() as conn:
            # Check if product exists and is approved
            product_query = text("SELECT product_id, stock FROM products WHERE product_id = :product_id AND status = 'approved'")
            product = conn.execute(product_query, {'product_id': product_id}).mappings().first()
            
            if not product:
                flash('Product not available', 'danger')
                return redirect(url_for('products'))
            
            # NULL-safe stock — treat None as 0
            available_stock = int(product['stock'] or 0)
            
            # Check if already in cart
            check_query = text("SELECT cart_id, quantity FROM cart WHERE user_id = :user_id AND product_id = :product_id")
            existing = conn.execute(check_query, {'user_id': session['user_id'], 'product_id': product_id}).mappings().first()
            
            if existing:
                if existing['quantity'] + 1 > available_stock:
                    flash('Cannot add more than available stock', 'warning')
                    return redirect(url_for('cart'))
                # Update quantity
                update_query = text("UPDATE cart SET quantity = quantity + 1 WHERE cart_id = :cart_id")
                conn.execute(update_query, {'cart_id': existing['cart_id']})
            else:
                if available_stock < 1:
                    flash('This product is out of stock', 'warning')
                    return redirect(url_for('products'))
                # Insert new cart item
                insert_query = text("INSERT INTO cart (user_id, product_id, quantity) VALUES (:user_id, :product_id, 1)")
                conn.execute(insert_query, {'user_id': session['user_id'], 'product_id': product_id})
            
            conn.commit()
            flash('Product added to cart', 'success')
    except Exception as e:
        print(f"Cart add error: {e}")
        flash('Failed to add product to cart', 'danger')
    
    return redirect(url_for('cart'))


@app.route('/cart/update/<int:cart_id>', methods=['POST'])
@login_required
def cart_update(cart_id):
    """Update cart item quantity"""
    quantity = request.form.get('quantity', '1')
    try:
        quantity = int(quantity)
        if quantity <= 0:
            quantity = 1
    except ValueError:
        quantity = 1
    
    try:
        with engine.connect() as conn:
            update_query = text("""
                UPDATE cart 
                SET quantity = :quantity 
                WHERE cart_id = :cart_id AND user_id = :user_id
            """)
            conn.execute(update_query, {'cart_id': cart_id, 'user_id': session['user_id'], 'quantity': quantity})
            conn.commit()
    except Exception as e:
        print(f"Cart update error: {e}")
    
    return redirect(url_for('cart'))


@app.route('/cart/remove/<int:cart_id>', methods=['POST'])
@login_required
def cart_remove(cart_id):
    """Remove item from cart"""
    try:
        with engine.connect() as conn:
            delete_query = text("DELETE FROM cart WHERE cart_id = :cart_id AND user_id = :user_id")
            conn.execute(delete_query, {'cart_id': cart_id, 'user_id': session['user_id']})
            conn.commit()
            flash('Item removed from cart', 'success')
    except Exception as e:
        print(f"Cart remove error: {e}")
        flash('Failed to remove item', 'danger')
    
    return redirect(url_for('cart'))


# ==================== ORDER PLACEMENT ====================
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout and place order"""
    if request.method == 'POST':
        try:
            with engine.connect() as conn:
                if not session.get('user_id'):
                    error_msg = 'User not logged in'
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({'success': False, 'message': error_msg}), 401
                    flash(error_msg, 'error')
                    return redirect(url_for('login'))
                    
                # Get cart items
                cart_query = text("""
                    SELECT c.*, p.price, p.name, p.stock
                    FROM cart c
                    JOIN products p ON c.product_id = p.product_id
                    WHERE c.user_id = :user_id AND p.status = 'approved'
                """)
                cart_items = conn.execute(cart_query, {'user_id': session['user_id']}).mappings().all()
                
                if not cart_items:
                    error_msg = 'Your cart is empty'
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return jsonify({'success': False, 'message': error_msg}), 400
                    flash(error_msg, 'warning')
                    return redirect(url_for('cart'))
                
                # Calculate total (using dict access because mappings() returns dict-like objects)
                total = sum(float(item['quantity'] * item['price']) for item in cart_items)
                
                # Extract address details from form submission
                address = request.form.get('address', '').strip()
                city = request.form.get('city', '').strip()
                zip_code = request.form.get('zip_code', '').strip()
                
                # Check for database dialect to execute correct query and fetch order_id
                dialect = engine.dialect.name
                if dialect == 'postgresql':
                    # Use RETURNING order_id for PostgreSQL
                    order_query = text("""
                        INSERT INTO orders (buyer_id, total_amount, status, address, city, zip_code)
                        VALUES (:buyer_id, :total_amount, 'pending', :address, :city, :zip_code)
                        RETURNING order_id
                    """)
                    result = conn.execute(order_query, {
                        'buyer_id': session['user_id'],
                        'total_amount': total,
                        'address': address,
                        'city': city,
                        'zip_code': zip_code
                    })
                    order_id = result.scalar()
                else:
                    # MySQL / SQLite insert
                    order_query = text("""
                        INSERT INTO orders (buyer_id, total_amount, status, address, city, zip_code)
                        VALUES (:buyer_id, :total_amount, 'pending', :address, :city, :zip_code)
                    """)
                    result = conn.execute(order_query, {
                        'buyer_id': session['user_id'],
                        'total_amount': total,
                        'address': address,
                        'city': city,
                        'zip_code': zip_code
                    })
                    # Reliable way to get last inserted ID on MySQL/SQLite
                    if hasattr(result, 'lastrowid') and result.lastrowid:
                        order_id = result.lastrowid
                    elif hasattr(result, 'inserted_primary_key') and result.inserted_primary_key:
                        order_id = result.inserted_primary_key[0]
                    else:
                        order_id = conn.execute(text("SELECT LAST_INSERT_ID()")).scalar()
                
                
                # Create order items — check stock and deduct atomically
                for item in cart_items:
                    item_stock = int(item['stock'] or 0)  # NULL-safe
                    if item['quantity'] > item_stock:
                        raise ValueError(f"Not enough stock for '{item['name']}'. Available: {item_stock}, Requested: {item['quantity']}")
                
                    item_query = text("""
                        INSERT INTO order_items (order_id, product_id, quantity, price)
                        VALUES (:order_id, :product_id, :quantity, :price)
                    """)
                    conn.execute(item_query, {
                        'order_id': order_id,
                        'product_id': item['product_id'],
                        'quantity': item['quantity'],
                        'price': item['price']
                    })
                    
                    # Deduct stock
                    update_stock_query = text("UPDATE products SET stock = stock - :quantity WHERE product_id = :product_id")
                    conn.execute(update_stock_query, {
                        'quantity': item['quantity'],
                        'product_id': item['product_id']
                    })
                
                # Clear cart
                clear_cart_query = text("DELETE FROM cart WHERE user_id = :user_id")
                conn.execute(clear_cart_query, {'user_id': session['user_id']})
                
                conn.commit()
                
                success_msg = 'Order placed successfully!'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'success': True, 'message': success_msg, 'order_id': order_id})
                
                flash(success_msg, 'success')
                return redirect(url_for('order_history'))
        except Exception as e:
            print("!!! CHECKOUT ERROR !!!")
            traceback.print_exc()
            error_msg = str(e)
            print(f"Error details: {error_msg}")
            
            # Check for common database errors
            if "Field 'address' doesn't have a default value" in error_msg:
                flash('Database Error: Missing address field. Please ask admin to update database.', 'danger')
            else:
                flash(f'Failed to place order. Error: {error_msg}', 'danger')
                
            return redirect(url_for('cart'))
    
    # GET request - show checkout page
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT c.*, p.name, p.price, p.image_path, p.product_id,
                       (c.quantity * p.price) as total
                FROM cart c
                JOIN products p ON c.product_id = p.product_id
                WHERE c.user_id = :user_id AND p.status = 'approved'
            """)
            cart_items = conn.execute(query, {'user_id': session['user_id']}).mappings().all()
            total = sum(float(item.total) for item in cart_items)
            
            if not cart_items:
                flash('Your cart is empty', 'warning')
                return redirect(url_for('cart'))
            
            return render_template('checkout.html', cart_items=cart_items, total=total)
    except Exception as e:
        print(f"Checkout GET error: {e}")
        return redirect(url_for('cart'))


# ==================== ORDER HISTORY ====================
@app.route('/orders')
@login_required
def order_history():
    """Order history page"""
    try:
        user_id = session.get('user_id')
        
        with engine.connect() as conn:
            dialect = engine.dialect.name
            if dialect == 'postgresql':
                group_concat_expr = "STRING_AGG(p.name, ', ')"
            elif dialect == 'sqlite':
                group_concat_expr = "GROUP_CONCAT(p.name, ', ')"
            else:  # mysql
                group_concat_expr = "GROUP_CONCAT(p.name SEPARATOR ', ')"

            query = text(f"""
                SELECT o.order_id, o.buyer_id, o.total_amount, o.status, o.created_at,
                       {group_concat_expr} as product_names,
                       COUNT(oi.order_item_id) as item_count
                FROM orders o
                LEFT JOIN order_items oi ON o.order_id = oi.order_id
                LEFT JOIN products p ON oi.product_id = p.product_id
                WHERE o.buyer_id = :user_id
                GROUP BY o.order_id, o.buyer_id, o.total_amount, o.status, o.created_at
                ORDER BY o.created_at DESC
            """)
            result = conn.execute(query, {'user_id': user_id})
            orders_raw = result.mappings().all()
            
            # Convert to list of dicts to ensure template can access
            orders = [dict(order) for order in orders_raw]
            
            return render_template('order_history.html', orders=orders)
    except Exception as e:
        print(f"Order history error: {e}")
        traceback.print_exc()
        return render_template('order_history.html', orders=[])


# ==================== ADMIN DASHBOARD ====================
@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    try:
        with engine.connect() as conn:
            # Get pending products
            pending_query = text("""
                SELECT p.*, COALESCE(u.username, 'Unknown') as username, COALESCE(u.full_name, 'Unknown') as full_name 
                FROM products p 
                LEFT JOIN users u ON p.seller_id = u.user_id 
                WHERE p.status = 'pending'
                ORDER BY p.created_at DESC
            """)
            pending_products = conn.execute(pending_query).mappings().all()
            
            # Get all users
            users_query = text("SELECT * FROM users WHERE role = 'student' ORDER BY created_at DESC")
            users = conn.execute(users_query).mappings().all()
            
            # Get statistics
            stats_query = text("""
                SELECT 
                    (SELECT COUNT(*) FROM users WHERE role = 'student') as total_students,
                    (SELECT COUNT(*) FROM products WHERE status = 'approved') as approved_products,
                    (SELECT COUNT(*) FROM products WHERE status = 'pending') as pending_products,
                    (SELECT COUNT(*) FROM orders) as total_orders
            """)
            stats_result = conn.execute(stats_query).mappings().first()
            stats = dict(stats_result) if stats_result else {}
            
            dialect = engine.dialect.name
            if dialect == 'postgresql':
                group_concat_expr = "STRING_AGG(p.name, ', ')"
            elif dialect == 'sqlite':
                group_concat_expr = "GROUP_CONCAT(p.name, ', ')"
            else:  # mysql
                group_concat_expr = "GROUP_CONCAT(p.name SEPARATOR ', ')"

            # Get all orders with user information
            orders_query = text(f"""
                SELECT o.*, 
                       u.username, 
                       u.full_name, 
                       u.email,
                       u.phone,
                       COUNT(oi.order_item_id) as item_count,
                       {group_concat_expr} as product_names
                FROM orders o
                JOIN users u ON o.buyer_id = u.user_id
                LEFT JOIN order_items oi ON o.order_id = oi.order_id
                LEFT JOIN products p ON oi.product_id = p.product_id
                GROUP BY o.order_id, u.user_id, u.username, u.full_name, u.email, u.phone
                ORDER BY o.created_at DESC
                LIMIT 50
            """)
            orders = conn.execute(orders_query).mappings().all()
            
            return render_template('admin_dashboard.html', 
                                 pending_products=pending_products, 
                                 users=users,
                                 stats=stats,
                                 orders=orders)
    except Exception as e:
        print(f"Admin dashboard error: {e}")
        return render_template('admin_dashboard.html', pending_products=[], users=[], stats={}, orders=[])


# ==================== ADMIN PRODUCT APPROVAL ====================
@app.route('/admin/product/approve/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def admin_approve_product(product_id):
    """Approve product"""
    try:
        with engine.connect() as conn:
            update_query = text("UPDATE products SET status = 'approved' WHERE product_id = :product_id")
            conn.execute(update_query, {'product_id': product_id})
            conn.commit()
            flash('Product approved successfully', 'success')
    except Exception as e:
        print(f"Approve product error: {e}")
        flash('Failed to approve product', 'danger')
    
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/product/reject/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def admin_reject_product(product_id):
    """Reject product"""
    try:
        with engine.connect() as conn:
            update_query = text("UPDATE products SET status = 'rejected' WHERE product_id = :product_id")
            conn.execute(update_query, {'product_id': product_id})
            conn.commit()
            flash('Product rejected', 'info')
    except Exception as e:
        print(f"Reject product error: {e}")
        flash('Failed to reject product', 'danger')
    
    return redirect(url_for('admin_dashboard'))


# ==================== ADMIN ORDER STATUS MANAGEMENT ====================
@app.route('/admin/order/update_status/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def admin_update_order_status(order_id):
    """
    Update order status (Pending, Approved, Rejected, Completed)
    Only admin can update order status
    """
    try:
        # Get new status from form data
        new_status = request.form.get('status', '').strip().lower()
        
        # Validate status
        valid_statuses = ['pending', 'approved', 'rejected', 'completed', 'cancelled']
        if new_status not in valid_statuses:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'success': False, 'message': 'Invalid order status'}), 400
            flash('Invalid order status', 'danger')
            return redirect(url_for('admin_dashboard'))
        
        with engine.connect() as conn:
            # Check if order exists
            check_query = text("SELECT order_id, status FROM orders WHERE order_id = :order_id")
            order_result = conn.execute(check_query, {'order_id': order_id}).mappings().first()
            
            if not order_result:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({'success': False, 'message': 'Order not found'}), 404
                flash('Order not found', 'danger')
                return redirect(url_for('admin_dashboard'))
            
            old_status = order_result['status']
            
            # Check if status is already correct (Idempotency)
            if old_status == new_status:
                msg = f'Order is already {new_status}'
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return jsonify({
                        'success': True,
                        'message': msg,
                        'order_id': order_id,
                        'new_status': new_status,
                        'old_status': old_status
                    }), 200
                flash(msg, 'info')
                return redirect(url_for('admin_dashboard'))

            # Update the order status
            update_query = text("""
                UPDATE orders 
                SET status = :status 
                WHERE order_id = :order_id
            """)
            conn.execute(update_query, {'status': new_status, 'order_id': order_id})
            conn.commit()
            
            # Success message based on status
            status_messages = {
                'pending': 'Order status updated to Pending',
                'approved': 'Order approved successfully',
                'rejected': 'Order rejected',
                'completed': 'Order marked as Completed',
                'cancelled': 'Order cancelled'
            }
            
            # Return JSON response for AJAX requests (MUST RETURN HERE for AJAX)
            is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            
            if is_ajax:
                return jsonify({
                    'success': True,
                    'message': status_messages.get(new_status, 'Order status updated'),
                    'order_id': order_id,
                    'new_status': new_status,
                    'old_status': old_status
                }), 200
            else:
                flash(status_messages.get(new_status, 'Order status updated successfully'), 'success')
                return redirect(url_for('admin_dashboard'))
            
    except Exception as e:
        error_msg = str(e)
        print(f"Update order status error: {e}")
        traceback.print_exc()
        
        # Return JSON error for AJAX requests
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if is_ajax:
            return jsonify({
                'success': False,
                'message': f'Failed to update order status: {error_msg}'
            }), 500
        else:
            flash(f'Failed to update order status: {error_msg}', 'danger')
            return redirect(url_for('admin_dashboard'))


# ==================== ADMIN USER MANAGEMENT ====================
@app.route('/admin/user/block/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def admin_block_user(user_id):
    """Block user"""
    try:
        with engine.connect() as conn:
            update_query = text("UPDATE users SET status = 'blocked' WHERE user_id = :user_id")
            conn.execute(update_query, {'user_id': user_id})
            conn.commit()
            flash('User blocked successfully', 'success')
    except Exception as e:
        print(f"Block user error: {e}")
        flash('Failed to block user', 'danger')
    
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/user/unblock/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def admin_unblock_user(user_id):
    """Unblock user"""
    try:
        with engine.connect() as conn:
            update_query = text("UPDATE users SET status = 'active' WHERE user_id = :user_id")
            conn.execute(update_query, {'user_id': user_id})
            conn.commit()
            flash('User unblocked successfully', 'success')
    except Exception as e:
        print(f"Unblock user error: {e}")
        flash('Failed to unblock user', 'danger')
    
    return redirect(url_for('admin_dashboard'))


# ==================== LOGOUT ====================
@app.route('/logout')
def logout():
    """Logout page"""
    session.clear()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('index'))


# ==================== STATIC FILES ====================
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files (alternative route for direct access)"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


# ==================== USER ORDER DELETE ====================
@app.route('/order/delete/<int:order_id>', methods=['POST'])
@login_required
def order_delete(order_id):
    """Delete order (only if pending or cancelled)"""
    try:
        with engine.connect() as conn:
            # Check ownership and status
            check_query = text("SELECT buyer_id, status FROM orders WHERE order_id = :order_id")
            order = conn.execute(check_query, {'order_id': order_id}).mappings().first()
            
            if not order:
                flash('Order not found', 'danger')
                return redirect(url_for('order_history'))
            
            if order['buyer_id'] != session['user_id']:
                flash('You can only delete your own orders', 'danger')
                return redirect(url_for('order_history'))
            
            # Allow deletion only for pending or cancelled orders
            if order['status'] not in ['pending', 'cancelled', 'rejected']:
                flash('Cannot delete active or completed orders', 'warning')
                return redirect(url_for('order_history'))
            
            # Delete order items first
            delete_items_query = text("DELETE FROM order_items WHERE order_id = :order_id")
            conn.execute(delete_items_query, {'order_id': order_id})
            
            # Delete the order
            delete_order_query = text("DELETE FROM orders WHERE order_id = :order_id")
            conn.execute(delete_order_query, {'order_id': order_id})
            
            conn.commit()
            flash('Order deleted successfully', 'success')
            
    except Exception as e:
        print(f"Order delete error: {e}")
        flash('Failed to delete order', 'danger')
    
    return redirect(url_for('order_history'))


# ==================== ADMIN SETUP / RESET ROUTE ====================
@app.route('/setup-admin')
def setup_admin():
    """
    Admin creation / password-reset route.
    Secured by SETUP_TOKEN env var (default: 'setup2024').

    Usage:
      /setup-admin?token=setup2024
      /setup-admin?token=setup2024&username=Aditya&password=Aditya@2103
    """
    setup_token = os.getenv('SETUP_TOKEN', 'setup2024')
    provided    = request.args.get('token', '')

    if provided != setup_token:
        return jsonify({
            'error': 'Unauthorized',
            'hint': 'Provide ?token=<SETUP_TOKEN> query parameter'
        }), 403

    try:
        username = request.args.get('username', os.getenv('ADMIN_USERNAME', 'Aditya'))
        password = request.args.get('password', os.getenv('ADMIN_PASSWORD', 'Aditya@2103'))
        email    = request.args.get('email',    os.getenv('ADMIN_EMAIL', 'admin@marketplace.com'))

        # Always generate a fresh hash in Python — never copy-paste from shell
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        with engine.connect() as conn:
            check = conn.execute(
                text("SELECT user_id FROM users WHERE username = :username"),
                {'username': username}
            ).mappings().first()

            if check:
                conn.execute(text("""
                    UPDATE users
                    SET email = :email, password = :password, role = 'admin', status = 'active'
                    WHERE username = :username
                """), {
                    'username':  username,
                    'email':     email,
                    'password':  hashed,
                })
            else:
                conn.execute(text("""
                    INSERT INTO users (username, email, password, full_name, role, status)
                    VALUES (:username, :email, :password, :full_name, 'admin', 'active')
                """), {
                    'username':  username,
                    'email':     email,
                    'password':  hashed,
                    'full_name': username,
                })
            conn.commit()

            row = conn.execute(
                text("SELECT user_id, username, role, status FROM users WHERE username = :u"),
                {'u': username}
            ).mappings().first()

        return jsonify({
            'success': True,
            'message': f'Admin "{username}" created / password reset successfully!',
            'user': dict(row),
            'login_url': '/admin/login',
            'credentials': {
                'username': username,
                'password': password,
                'note':     'Save this — password is not stored in plain text'
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== RUN APPLICATION ====================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

