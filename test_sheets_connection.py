#!/usr/bin/env python3
"""
Test Google Sheets connection
"""
import gspread
from google.oauth2.service_account import Credentials
from config import Config

def test_connection(sheet_id=None):
    """Test Google Sheets connection"""
    try:
        print("🔧 Testing Google Sheets connection...")
        
        # Setup credentials
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        credentials = Credentials.from_service_account_file(
            Config.GOOGLE_SHEETS_CREDENTIALS_FILE, 
            scopes=scope
        )
        
        # Create client
        client = gspread.authorize(credentials)
        print("✅ Credentials loaded successfully")
        
        if sheet_id:
            print(f"🔍 Testing connection to sheet: {sheet_id}")
            try:
                # Try to open the sheet
                sheet = client.open_by_key(sheet_id).sheet1
                print("✅ Successfully connected to Google Sheet!")
                print(f"📊 Sheet title: {sheet.title}")
                print(f"🔗 Sheet URL: {sheet.url}")
                
                # Try to read a cell
                try:
                    cell_value = sheet.cell(1, 1).value
                    print(f"📝 Cell A1 value: '{cell_value}'")
                except Exception as e:
                    print(f"⚠️  Could not read cell A1: {e}")
                
                return True
                
            except Exception as e:
                print(f"❌ Failed to connect to sheet: {e}")
                print("\n🔧 Troubleshooting steps:")
                print("1. Check that the Sheet ID is correct")
                print("2. Share the sheet with: linkedin-scraper@linkedin-scraper-473920.iam.gserviceaccount.com")
                print("3. Give it 'Editor' permissions")
                return False
        else:
            print("ℹ️  No sheet ID provided. Testing credential access only.")
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    # Test without sheet ID first
    print("=== Testing Credentials ===")
    test_connection()
    
    # Get sheet ID from user
    print("\n=== Testing Sheet Connection ===")
    sheet_id = input("Enter your Google Sheet ID (or press Enter to skip): ").strip()
    
    if sheet_id:
        test_connection(sheet_id)
    else:
        print("Skipping sheet connection test.")
