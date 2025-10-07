#!/usr/bin/env python3
"""
LinkedIn Contact Scraper Launcher
"""
import subprocess
import sys
import os

def main():
    print("🚀 LinkedIn Contact Scraper Launcher")
    print("=" * 40)
    
    # Check if we're in the right directory
    if not os.path.exists('simple_app.py'):
        print("❌ Error: simple_app.py not found!")
        print("Please run this script from the project directory:")
        print("/Users/abhinavala/linkedin_outreach_platform")
        return
    
    if not os.path.exists('venv'):
        print("❌ Error: Virtual environment not found!")
        print("Please make sure you're in the correct project directory.")
        return
    
    print("✅ Project files found")
    print("🌐 Starting Streamlit app...")
    print("📱 The app will open in your browser at: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    print("=" * 40)
    
    try:
        # Run streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'simple_app.py',
            '--server.port', '8501',
            '--server.address', 'localhost'
        ])
    except KeyboardInterrupt:
        print("\n🛑 App stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")

if __name__ == "__main__":
    main()
