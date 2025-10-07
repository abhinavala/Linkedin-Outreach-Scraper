#!/usr/bin/env python3
"""
Create a new Google Sheet that the service account can access
"""
import gspread
from google.oauth2.service_account import Credentials
from config import Config

def create_new_sheet():
    """Create a new Google Sheet"""
    try:
        print("🔧 Creating a new Google Sheet...")
        
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
        print("✅ Client authorized successfully")
        
        # Create a new spreadsheet
        print("📊 Creating new spreadsheet...")
        spreadsheet = client.create("LinkedIn Contacts Test")
        print("✅ Successfully created new spreadsheet!")
        
        # Get the worksheet
        worksheet = spreadsheet.sheet1
        print(f"📝 Worksheet title: {worksheet.title}")
        print(f"🔗 Sheet URL: {worksheet.url}")
        print(f"📊 Sheet ID: {spreadsheet.id}")
        
        # Add some test data
        headers = ['Name', 'Title', 'Company', 'Location', 'Profile URL']
        worksheet.append_row(headers)
        print("✅ Added headers to the sheet")
        
        return spreadsheet.id, spreadsheet.url
        
    except Exception as e:
        print(f"❌ Error creating sheet: {e}")
        return None, None

if __name__ == "__main__":
    sheet_id, sheet_url = create_new_sheet()
    if sheet_id:
        print(f"\n🎉 SUCCESS! Use this Sheet ID in your app: {sheet_id}")
        print(f"🔗 Sheet URL: {sheet_url}")
    else:
        print("\n❌ Failed to create sheet. Check your Google Drive quota.")
