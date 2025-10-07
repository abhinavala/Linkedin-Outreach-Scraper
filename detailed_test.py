#!/usr/bin/env python3
"""
Detailed test with more error information
"""
import gspread
from google.oauth2.service_account import Credentials
from config import Config
import traceback

def detailed_test():
    """Detailed test with error information"""
    sheet_id = "1J-kMNJAmRmrzBI_D_bTxgAf6pEkXB6z3y52GwlmFDD0"
    
    try:
        print("🔧 Detailed connection test...")
        print(f"📊 Sheet ID: {sheet_id}")
        print(f"📁 Credentials file: {Config.GOOGLE_SHEETS_CREDENTIALS_FILE}")
        
        # Setup credentials
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        credentials = Credentials.from_service_account_file(
            Config.GOOGLE_SHEETS_CREDENTIALS_FILE, 
            scopes=scope
        )
        
        print("✅ Credentials loaded successfully")
        print(f"📧 Service account email: {credentials.service_account_email}")
        
        # Create client
        client = gspread.authorize(credentials)
        print("✅ Client authorized successfully")
        
        # Try to open the sheet
        print(f"🔍 Attempting to open sheet by ID...")
        spreadsheet = client.open_by_key(sheet_id)
        print("✅ Successfully opened spreadsheet!")
        print(f"📊 Spreadsheet title: {spreadsheet.title}")
        
        # Get the first worksheet
        worksheet = spreadsheet.sheet1
        print(f"📝 Worksheet title: {worksheet.title}")
        print(f"🔗 Sheet URL: {worksheet.url}")
        
        # Try to read a cell
        try:
            cell_value = worksheet.cell(1, 1).value
            print(f"📝 Cell A1 value: '{cell_value}'")
        except Exception as e:
            print(f"⚠️  Could not read cell A1: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print(f"❌ Error type: {type(e).__name__}")
        print("\n🔍 Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    detailed_test()
