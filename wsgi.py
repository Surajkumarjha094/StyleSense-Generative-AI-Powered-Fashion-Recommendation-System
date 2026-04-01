"""
WSGI entry point for Vercel deployment
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Flask app
from app import app

# Vercel will use this app object
if __name__ == '__main__':
    app.run()
