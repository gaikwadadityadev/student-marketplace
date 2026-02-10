-- Migration script to update orders table status ENUM
-- Adds 'approved' and 'rejected' status options
-- Run this before implementing the admin order management feature

USE student_marketplace;

-- Update the orders table to include new status values
ALTER TABLE orders 
MODIFY COLUMN status ENUM('pending', 'approved', 'rejected', 'completed', 'cancelled') 
DEFAULT 'pending';

-- Verify the update
DESCRIBE orders;

