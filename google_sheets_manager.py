import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import logging
from config import Config

class GoogleSheetsManager:
    def __init__(self):
        self.credentials = None
        self.client = None
        self.sheet = None
        self.setup_logging()
        self.setup_credentials()
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def setup_credentials(self):
        """Setup Google Sheets credentials"""
        try:
            # Define the scope
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Load credentials from file
            self.credentials = Credentials.from_service_account_file(
                Config.GOOGLE_SHEETS_CREDENTIALS_FILE, 
                scopes=scope
            )
            
            # Create gspread client
            self.client = gspread.authorize(self.credentials)
            
            self.logger.info("Google Sheets credentials loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error setting up Google Sheets credentials: {str(e)}")
            raise
    
    def connect_to_sheet(self, sheet_id=None):
        """Connect to a specific Google Sheet"""
        try:
            sheet_id = sheet_id or Config.GOOGLE_SHEET_ID
            self.sheet = self.client.open_by_key(sheet_id).sheet1
            self.logger.info(f"Connected to Google Sheet: {sheet_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error connecting to Google Sheet: {str(e)}")
            return False
    
    def add_headers_if_needed(self):
        """Add headers to the sheet if they don't exist"""
        try:
            if not self.sheet:
                self.logger.error("No sheet connected")
                return False
            
            # Check if headers already exist
            try:
                first_row = self.sheet.row_values(1)
                if first_row and 'Name' in first_row:
                    self.logger.info("Headers already exist")
                    return True
            except:
                pass
            
            # Add headers
            headers = [
                'Name', 'Title', 'Company', 'Location', 'Profile URL',
                'SCU Alumni', 'Email', 'Date Added', 'Status', 'Notes'
            ]
            self.sheet.append_row(headers)
            
            # Format headers (make them bold)
            self.sheet.format('A1:J1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
            })
            
            self.logger.info("Added headers to Google Sheet")
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding headers: {str(e)}")
            return False
    
    def create_sheet_with_headers(self, sheet_name="LinkedIn Outreach Leads"):
        """Create a new sheet with headers"""
        try:
            # Create a new spreadsheet
            spreadsheet = self.client.create(sheet_name)
            
            # Get the first worksheet
            worksheet = spreadsheet.sheet1
            
            # Define headers
            headers = [
                'Name', 'Title', 'Company', 'Location', 'Profile URL', 
                'SCU Alumni', 'Email', 'Date Added', 'Status', 'Notes'
            ]
            
            # Add headers to the first row
            worksheet.append_row(headers)
            
            # Format headers (make them bold)
            worksheet.format('A1:J1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
            })
            
            self.logger.info(f"Created new sheet: {sheet_name}")
            return spreadsheet.id
            
        except Exception as e:
            self.logger.error(f"Error creating sheet: {str(e)}")
            return None
    
    def add_people_data(self, people_data):
        """Add people data to the Google Sheet"""
        try:
            if not self.sheet:
                self.logger.error("No sheet connected. Call connect_to_sheet() first.")
                return False
            
            # Prepare data for insertion
            rows_to_add = []
            
            for person in people_data:
                row = [
                    person.get('name', ''),
                    person.get('title', ''),
                    person.get('company', ''),
                    person.get('location', ''),
                    person.get('profile_url', ''),
                    'Yes' if person.get('is_scu_alumni', False) else 'No',
                    '',  # Empty email column for manual entry
                    pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'New',
                    ''
                ]
                rows_to_add.append(row)
            
            # Add all rows at once
            if rows_to_add:
                self.sheet.append_rows(rows_to_add)
                self.logger.info(f"Added {len(rows_to_add)} people to the sheet")
                return True
            else:
                self.logger.warning("No data to add to sheet")
                return False
                
        except Exception as e:
            self.logger.error(f"Error adding people data to sheet: {str(e)}")
            return False
    
    def get_sheet_data(self):
        """Get all data from the current sheet"""
        try:
            if not self.sheet:
                self.logger.error("No sheet connected. Call connect_to_sheet() first.")
                return None
            
            # Get all records
            records = self.sheet.get_all_records()
            return records
            
        except Exception as e:
            self.logger.error(f"Error getting sheet data: {str(e)}")
            return None
    
    def update_person_status(self, row_index, status, notes=""):
        """Update the status and notes for a specific person"""
        try:
            if not self.sheet:
                self.logger.error("No sheet connected. Call connect_to_sheet() first.")
                return False
            
            # Update status (column N)
            self.sheet.update_cell(row_index + 2, 14, status)  # +2 because of header row and 0-based index
            
            # Update notes (column O)
            if notes:
                self.sheet.update_cell(row_index + 2, 15, notes)
            
            self.logger.info(f"Updated status for row {row_index + 1}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error updating person status: {str(e)}")
            return False
    
    def export_to_csv(self, filename="linkedin_leads.csv"):
        """Export sheet data to CSV"""
        try:
            data = self.get_sheet_data()
            if data:
                df = pd.DataFrame(data)
                df.to_csv(filename, index=False)
                self.logger.info(f"Exported data to {filename}")
                return True
            else:
                self.logger.warning("No data to export")
                return False
                
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {str(e)}")
            return False
    
    def get_sheet_url(self):
        """Get the URL of the current sheet"""
        try:
            if self.sheet:
                return self.sheet.url
            return None
        except Exception as e:
            self.logger.error(f"Error getting sheet URL: {str(e)}")
            return None