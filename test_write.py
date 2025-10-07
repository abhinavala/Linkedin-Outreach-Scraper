#!/usr/bin/env python3
"""
Test writing to Google Sheet
"""
import gspread
from google.oauth2.service_account import Credentials
from config import Config

def test_write():
    """Test writing to Google Sheet"""
    sheet_id = "1J-kMNJAmRmrzBI_D_bTxgAf6pEkXB6z3y52GwlmFDD0"
    
    try:
        print("🔧 Testing write access to Google Sheet...")
        
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
        
        # Open the sheet
        spreadsheet = client.open_by_key(sheet_id)
        worksheet = spreadsheet.sheet1
        
        print("✅ Connected to sheet successfully")
        
        # Test writing headers
        headers = ['Name', 'Title', 'Company', 'Location', 'Profile URL']
        print(f"📝 Adding headers: {headers}")
        
        worksheet.update('A1:E1', [headers])
        print("✅ Successfully added headers!")
        
        # Test writing some sample data
        sample_data = [
            ['John Doe', 'Software Engineer', 'Tech Corp', 'San Francisco', 'https://linkedin.com/in/johndoe'],
            ['Jane Smith', 'Product Manager', 'Startup Inc', 'New York', 'https://linkedin.com/in/janesmith']
        ]
        
        print(f"📝 Adding sample data...")
        worksheet.update('A2:E3', sample_data)
        print("✅ Successfully added sample data!")
        
        print(f"🔗 Sheet URL: {worksheet.url}")
        print("🎉 Write test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error writing to sheet: {e}")
        return False

if __name__ == "__main__":
    test_write()
