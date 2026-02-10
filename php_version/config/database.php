<?php
/**
 * Database Configuration and Connection
 * Student Marketplace - PHP Version
 * 
 * This file handles database connection using PDO
 * with prepared statements for security
 */

// Database configuration
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', 'Aditya@08'); // Change this to your MySQL password
define('DB_NAME', 'student_marketplace_php');

// Create database connection
class Database {
    private $host = DB_HOST;
    private $user = DB_USER;
    private $pass = DB_PASS;
    private $dbname = DB_NAME;
    private $conn;
    private $error;

    /**
     * Constructor - Create database connection
     */
    public function __construct() {
        $dsn = "mysql:host=" . $this->host . ";dbname=" . $this->dbname . ";charset=utf8mb4";
        
        $options = array(
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
            PDO::ATTR_EMULATE_PREPARES => false
        );

        try {
            $this->conn = new PDO($dsn, $this->user, $this->pass, $options);
        } catch(PDOException $e) {
            $this->error = $e->getMessage();
            echo "Connection Error: " . $this->error;
            die();
        }
    }

    /**
     * Get database connection
     * @return PDO
     */
    public function getConnection() {
        return $this->conn;
    }

    /**
     * Close database connection
     */
    public function closeConnection() {
        $this->conn = null;
    }
}

// Create global database instance
$database = new Database();
$db = $database->getConnection();
