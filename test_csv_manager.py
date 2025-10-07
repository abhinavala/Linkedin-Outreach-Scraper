#!/usr/bin/env python3
"""
Test CSV Manager functionality
"""
from csv_manager import CSVManager

def test_csv_manager():
    """Test CSV manager with sample data"""
    print("🔧 Testing CSV Manager...")
    
    # Sample contact data
    sample_contacts = [
        {
            'name': 'John Doe',
            'title': 'Software Engineer',
            'company': 'Tech Corp',
            'location': 'San Francisco, CA',
            'profile_url': 'https://linkedin.com/in/johndoe'
        },
        {
            'name': 'Jane Smith',
            'title': 'Product Manager',
            'company': 'Startup Inc',
            'location': 'New York, NY',
            'profile_url': 'https://linkedin.com/in/janesmith'
        },
        {
            'name': 'Mike Johnson',
            'title': 'Data Scientist',
            'company': 'AI Company',
            'location': 'Seattle, WA',
            'profile_url': 'https://linkedin.com/in/mikejohnson'
        }
    ]
    
    # Test CSV manager
    csv_manager = CSVManager()
    
    # Test export
    result = csv_manager.export_contacts(sample_contacts, "test_contacts.csv")
    
    if result['success']:
        print(f"✅ Successfully exported {result['contact_count']} contacts to {result['filename']}")
        print(f"📁 File path: {result['filepath']}")
        
        # Test file info
        file_info = csv_manager.get_export_info(result['filename'])
        if file_info['exists']:
            print(f"📊 File size: {file_info['size']} bytes")
            print(f"📂 File path: {file_info['path']}")
        
        return True
    else:
        print(f"❌ Export failed: {result['error']}")
        return False

if __name__ == "__main__":
    test_csv_manager()
