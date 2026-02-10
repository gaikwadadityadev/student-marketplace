# Ex-Student Backend (Flask + MySQL)

## Setup

1. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv
. .venv/Scripts/activate
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create a MySQL database

```sql
CREATE DATABASE IF NOT EXISTS ex_student CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Optionally create a simple `products` table:

```sql
CREATE TABLE IF NOT EXISTS products (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  price INT NOT NULL
);
```

4. Set environment variables (PowerShell example)

```powershell
$env:MYSQL_USER="root"
$env:MYSQL_PASSWORD="yourpassword"
$env:MYSQL_HOST="127.0.0.1"
$env:MYSQL_PORT="3306"
$env:MYSQL_DB="ex_student"
$env:CORS_ORIGINS="*"
```

5. Run the server

```bash
python app.py
```

It starts on http://localhost:5000

- GET /api/health — health check with DB ping
- GET /api/products — sample static products (replace with DB query)

## Notes
- Connection uses SQLAlchemy with the `PyMySQL` driver for Windows compatibility.
- For real data, replace `/api/products` to query your `products` table.

