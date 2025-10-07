#!/usr/bin/env python3
"""
Test connection to your specific Google Sheet
"""
import gspread
from google.oauth2.service_account import Credentials
from config import Config

def test_your_sheet():
    """Test connection to your Google Sheet"""
    sheet_id = "1J-kMNJAmRmrzBI_D_bTxgAf6pEkXB6z3y52GwlmFDD0"
    
    try:
        print("🔧 Testing connection to your Google Sheet...")
        print(f"📊 Sheet ID: {sheet_id}")
        
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
        
        # Try to open the sheet
        print(f"🔍 Attempting to connect to sheet...")
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
        print("1. Make sure you've shared the sheet with: linkedin-scraper@linkedin-scraper-473920.iam.gserviceaccount.com")
        print("2. Give it 'Editor' permissions")
        print("3. Make sure the sheet exists and is accessible")
        return False

if __name__ == "__main__":
    test_your_sheet()
