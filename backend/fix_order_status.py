"""
Script to fix order status ENUM in database
Run this script to update the orders table to support new statuses
"""
from sqlalchemy import create_engine, text
from config import Config
import sys

def fix_order_status_enum():
    """Update orders table to include new status values"""
    try:
        engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
        
        print("=" * 60)
        print("Fixing Orders Table Status ENUM")
        print("=" * 60)
        
        with engine.connect() as conn:
            # Check current status ENUM
            check_query = text("""
                SELECT COLUMN_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'orders' 
                AND COLUMN_NAME = 'status'
            """)
            result = conn.execute(check_query).fetchone()
            
            if result:
                current_enum = result[0]
                print(f"Current status ENUM: {current_enum}")
                
                # Check if new statuses are already included
                if 'approved' in current_enum and 'rejected' in current_enum:
                    print("[OK] Status ENUM already includes 'approved' and 'rejected'")
                    return True
            
            # Update the ENUM
            print("\nUpdating status ENUM...")
            alter_query = text("""
                ALTER TABLE orders 
                MODIFY COLUMN status ENUM('pending', 'approved', 'rejected', 'completed', 'cancelled') 
                DEFAULT 'pending'
            """)
            conn.execute(alter_query)
            conn.commit()
            
            print("[SUCCESS] Successfully updated orders table status ENUM")
            print("   New statuses: pending, approved, rejected, completed, cancelled")
            
            # Verify the update
            verify_query = text("""
                SELECT COLUMN_TYPE 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = DATABASE() 
                AND TABLE_NAME = 'orders' 
                AND COLUMN_NAME = 'status'
            """)
            result = conn.execute(verify_query).fetchone()
            if result:
                print(f"[VERIFIED] New ENUM: {result[0]}")
            
            return True
            
    except Exception as e:
        print(f"[ERROR] Error updating database: {e}")
        print("\nPlease run the SQL migration manually:")
        print("  mysql -u root -p student_marketplace < backend/sql/update_orders_status.sql")
        return False

if __name__ == '__main__':
    print("\n")
    success = fix_order_status_enum()
    print("\n" + "=" * 60)
    if success:
        print("[SUCCESS] Database update complete!")
        print("You can now use the order status management feature.")
    else:
        print("[ERROR] Database update failed!")
        print("Please check the error above and try again.")
    print("=" * 60 + "\n")
    sys.exit(0 if success else 1)

