#!/usr/bin/env python3
import subprocess
import sys
import os

# Change to the correct directory
os.chdir('/Users/abhinavala/linkedin_outreach_platform')

# Run streamlit
try:
    print("🚀 Starting LinkedIn Contact Scraper...")
    print("🌐 The app will open in your browser at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run', 'simple_app.py',
        '--server.port', '8501',
        '--server.address', 'localhost'
    ])
except KeyboardInterrupt:
    print("\n🛑 App stopped")
except Exception as e:
    print(f"❌ Error: {e}")
