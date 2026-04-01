"""
WSGI entry point for Vercel deployment
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import Flask app
from app import app

# Export app for Vercel
export = app
