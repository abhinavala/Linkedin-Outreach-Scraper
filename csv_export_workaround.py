#!/usr/bin/env python3
"""
CSV Export Workaround for Google Sheets quota issues
"""
import csv
import os
from datetime import datetime

def export_to_csv(data, filename=None):
    """Export data to CSV file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"linkedin_contacts_{timestamp}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            if data:
                writer = csv.writer(csvfile)
                # Write headers
                headers = ['Name', 'Title', 'Company', 'Location', 'Profile URL']
                writer.writerow(headers)
                
                # Write data
                for row in data:
                    writer.writerow(row)
        
        print(f"✅ Successfully exported {len(data)} contacts to {filename}")
        print(f"📁 File location: {os.path.abspath(filename)}")
        return filename
        
    except Exception as e:
        print(f"❌ Error exporting to CSV: {e}")
        return None

def test_csv_export():
    """Test CSV export functionality"""
    sample_data = [
        ['John Doe', 'Software Engineer', 'Tech Corp', 'San Francisco', 'https://linkedin.com/in/johndoe'],
        ['Jane Smith', 'Product Manager', 'Startup Inc', 'New York', 'https://linkedin.com/in/janesmith'],
        ['Mike Johnson', 'Data Scientist', 'AI Company', 'Seattle', 'https://linkedin.com/in/mikejohnson']
    ]
    
    print("🔧 Testing CSV export...")
    filename = export_to_csv(sample_data)
    
    if filename:
        print(f"🎉 CSV export test successful!")
        print(f"📊 You can open the file in Excel or Google Sheets manually")
        return True
    else:
        print("❌ CSV export test failed")
        return False

if __name__ == "__main__":
    test_csv_export()
