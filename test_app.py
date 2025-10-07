import streamlit as st
import pandas as pd
from google_sheets_manager import GoogleSheetsManager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    st.set_page_config(
        page_title="LinkedIn Contact Scraper - Test Mode",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 LinkedIn Contact Scraper - Test Mode")
    st.markdown("**Testing Google Sheets integration without LinkedIn scraping**")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Google Sheets configuration
    st.sidebar.subheader("Google Sheets")
    google_sheet_id = st.sidebar.text_input("Google Sheet ID (optional)")
    use_existing_sheet = st.sidebar.checkbox("Use existing sheet", value=False)
    
    # Main content area
    tab1, tab2 = st.tabs(["🧪 Test Google Sheets", "📊 Results"])
    
    with tab1:
        st.header("Test Google Sheets Integration")
        
        if st.button("🧪 Test Google Sheets Connection", type="primary"):
            try:
                # Test Google Sheets connection
                sheets_manager = GoogleSheetsManager()
                
                if use_existing_sheet and google_sheet_id:
                    if sheets_manager.connect_to_sheet(google_sheet_id):
                        st.success("✅ Successfully connected to existing Google Sheet!")
                        st.info(f"Sheet URL: {sheets_manager.get_sheet_url()}")
                    else:
                        st.error("❌ Failed to connect to existing Google Sheet")
                else:
                    # Create new sheet
                    sheet_id = sheets_manager.create_sheet_with_headers("LinkedIn Contacts Test")
                    if sheet_id:
                        st.success("✅ Successfully created new Google Sheet!")
                        st.info(f"Sheet ID: {sheet_id}")
                        st.info(f"Sheet URL: {sheets_manager.get_sheet_url()}")
                        
                        # Add some test data
                        test_data = [
                            {
                                'name': 'John Doe',
                                'title': 'Software Engineer',
                                'company': 'Google',
                                'location': 'Mountain View, CA',
                                'profile_url': 'https://linkedin.com/in/johndoe',
                                'is_scu_alumni': True
                            },
                            {
                                'name': 'Jane Smith',
                                'title': 'Data Scientist',
                                'company': 'Meta',
                                'location': 'Menlo Park, CA',
                                'profile_url': 'https://linkedin.com/in/janesmith',
                                'is_scu_alumni': False
                            },
                            {
                                'name': 'Bob Johnson',
                                'title': 'Product Manager',
                                'company': 'TikTok',
                                'location': 'Los Angeles, CA',
                                'profile_url': 'https://linkedin.com/in/bobjohnson',
                                'is_scu_alumni': True
                            }
                        ]
                        
                        if sheets_manager.add_people_data(test_data):
                            st.success("✅ Successfully added test data to Google Sheet!")
                        else:
                            st.error("❌ Failed to add test data to Google Sheet")
                    else:
                        st.error("❌ Failed to create new Google Sheet")
                        
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("Make sure your credentials.json file is in the project directory and properly configured.")
    
    with tab2:
        st.header("Test Results")
        
        st.markdown("""
        ### What This Test Does:
        1. **Tests Google Sheets API connection** using your credentials.json
        2. **Creates a new Google Sheet** (if no existing sheet specified)
        3. **Adds test data** with the proper format
        4. **Verifies the integration** is working
        
        ### Next Steps:
        Once this test passes, we can work on fixing the LinkedIn scraping functionality.
        
        ### Expected Google Sheet Columns:
        - Name, Title, Company, Location, Profile URL
        - SCU Alumni (Yes/No)
        - Email (blank for manual entry)
        - Date Added, Status, Notes
        """)

if __name__ == "__main__":
    main()