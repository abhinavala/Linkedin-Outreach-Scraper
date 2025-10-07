#!/usr/bin/env python3
"""
CSV Export Manager for LinkedIn Contact Data
"""
import csv
import os
from datetime import datetime
import logging

class CSVManager:
    def __init__(self):
        self.setup_logging()
        # Set output directory to Downloads folder
        home_dir = os.path.expanduser("~")
        self.output_dir = os.path.join(home_dir, "Downloads")
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def export_contacts(self, contacts, filename=None):
        """Export contacts to CSV file"""
        if not contacts:
            self.logger.warning("No contacts to export")
            return None
            
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"linkedin_contacts_{timestamp}.csv"
        
        try:
            # Ensure filename has .csv extension
            if not filename.endswith('.csv'):
                filename += '.csv'
            
            filepath = os.path.join(self.output_dir, filename)
            
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                if contacts:
                    writer = csv.writer(csvfile)
                    
                    # Write headers
                    headers = ['Name', 'Title', 'Company', 'Location', 'SCU Alumni', 'Profile URL']
                    writer.writerow(headers)
                    
                    # Write contact data
                    for contact in contacts:
                        row = [
                            contact.get('name', ''),
                            contact.get('title', ''),
                            contact.get('company', ''),
                            contact.get('location', ''),
                            'Yes' if contact.get('is_scu_alumni', False) else 'No',
                            contact.get('profile_url', '')
                        ]
                        writer.writerow(row)
            
            self.logger.info(f"Successfully exported {len(contacts)} contacts to {filename}")
            return {
                'success': True,
                'filename': filename,
                'filepath': os.path.abspath(filepath),
                'contact_count': len(contacts)
            }
            
        except Exception as e:
            self.logger.error(f"Error exporting to CSV: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def get_export_info(self, filename):
        """Get information about the exported file"""
        try:
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                return {
                    'exists': True,
                    'size': file_size,
                    'path': os.path.abspath(filename)
                }
            else:
                return {'exists': False}
        except Exception as e:
            self.logger.error(f"Error getting file info: {e}")
            return {'exists': False, 'error': str(e)}
