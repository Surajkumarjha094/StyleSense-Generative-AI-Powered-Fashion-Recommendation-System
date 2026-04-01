"""
Vercel Serverless Function Handler
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables early
load_dotenv()

# Import Flask app
try:
    from app import app
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)

# Handler function for Vercel
def handler(request):
    """Handle HTTP requests from Vercel"""
    try:
        # Create a test request
        with app.test_client() as client:
            # Forward the request to Flask
            method = request.method.lower()
            path = request.path
            query_string = request.query_string.decode() if request.query_string else None
            
            # Route to Flask
            response = client.open(
                path,
                method=method,
                data=request.data,
                query_string=query_string,
                headers=dict(request.headers)
            )
            return response
    except Exception as e:
        print(f"Handler error: {e}")
        return {"statusCode": 500, "body": f"Error: {str(e)}"}
