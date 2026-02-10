#!/usr/bin/env python3
"""Test the Flask app directly"""
import sys
sys.path.insert(0, 'backend')

try:
    from app import app
    print("✓ Flask app imported successfully")
    
    # Test app context
    with app.app_context():
        print("✓ App context created")
        
        # Try rendering a template
        from flask import render_template
        try:
            html = render_template('index.html', products=[])
            print("✓ index.html template rendered successfully")
        except Exception as e:
            print(f"✗ Error rendering index.html: {e}")
            import traceback
            traceback.print_exc()
            
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
