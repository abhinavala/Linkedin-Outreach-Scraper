#!/bin/bash

# LinkedIn Contact Scraper Startup Script
echo "🚀 Starting LinkedIn Contact Scraper..."

# Navigate to project directory
cd /Users/abhinavala/linkedin_outreach_platform

# Activate virtual environment
source venv/bin/activate

# Run streamlit
echo "🌐 The app will open in your browser at: http://localhost:8501"
echo "Press Ctrl+C to stop the app"
streamlit run simple_app.py
