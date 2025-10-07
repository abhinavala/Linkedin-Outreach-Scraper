#!/usr/bin/env python3
"""
Script to run the LinkedIn Contact Scraper with proper setup
"""
import subprocess
import sys
import os
import time

def main():
    print("🚀 Starting LinkedIn Contact Scraper...")
    
    # Set environment variables to skip Streamlit setup
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Run streamlit
    try:
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 'simple_app.py',
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--browser.gatherUsageStats', 'false',
            '--server.headless', 'false'
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        print("🌐 The app will open in your browser at: http://localhost:8501")
        print("Press Ctrl+C to stop the app")
        
        # Run streamlit
        process = subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Stopping LinkedIn Contact Scraper...")
    except Exception as e:
        print(f"❌ Error running the app: {e}")

if __name__ == "__main__":
    main()
