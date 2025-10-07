import streamlit as st
import pandas as pd
import time
from simple_workflow import SimpleLinkedInWorkflow
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    st.set_page_config(
        page_title="LinkedIn Contact Scraper",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 LinkedIn Contact Scraper")
    st.markdown("**Find and collect LinkedIn contacts from target companies**")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # LinkedIn Login Info
    st.sidebar.subheader("LinkedIn Login")
    st.sidebar.info("You'll be prompted to log into LinkedIn manually when the scraper starts. No credentials needed here!")
    
    # Export configuration
    st.sidebar.subheader("Export Options")
    export_method = st.sidebar.radio(
        "Choose export method:",
        ["CSV Export (Recommended)", "Google Sheets"]
    )
    
    if export_method == "CSV Export (Recommended)":
        st.sidebar.success("✅ CSV export works immediately - no setup required!")
        st.sidebar.info("📁 Files will be saved to your project folder")
        
        # CSV filename option
        csv_filename = st.sidebar.text_input(
            "CSV filename (optional)", 
            help="Leave blank for auto-generated filename with timestamp"
        )
        use_existing_sheet = False
    
    else:  # Google Sheets
        st.sidebar.subheader("Google Sheets")
        st.sidebar.info("⚠️ Requires Google Drive quota and proper permissions")
        use_existing_sheet = st.sidebar.checkbox("Use existing sheet (optional)", value=False)
    
    google_sheet_id = None
    if export_method == "Google Sheets" and use_existing_sheet:
        google_sheet_id = st.sidebar.text_input("Google Sheet ID", help="Copy the ID from your Google Sheet URL")
        
        # Instructions for getting Google Sheet ID
        with st.sidebar.expander("How to get Google Sheet ID"):
            st.markdown("""
            1. Go to [Google Sheets](https://sheets.google.com)
            2. Create a new sheet or open an existing one
            3. Copy the ID from the URL:
               - URL: `https://docs.google.com/spreadsheets/d/1ABC123...XYZ/edit`
               - ID: `1ABC123...XYZ` (the part between `/d/` and `/edit`)
            4. Make sure the service account has access to the sheet
            """)
    
    # Search configuration
    st.sidebar.subheader("Search Settings")
    max_people_per_company = st.sidebar.slider("Max people per company", 10, 100, 50)
    search_keywords = st.sidebar.text_area(
        "Search Keywords (comma-separated)", 
        value="software engineer,data scientist,product manager,marketing manager"
    )
    
    # Main content area
    tab1, tab2, tab3 = st.tabs(["🏢 Company Input", "📊 Results", "⚙️ Setup Guide"])
    
    with tab1:
        st.header("Add Target Companies")
        
        # Company input methods
        input_method = st.radio(
            "How would you like to add companies?",
            ["Manual Input", "Upload CSV", "Paste List"]
        )
        
        companies = []
        
        if input_method == "Manual Input":
            st.subheader("Enter Companies Manually")
            company_input = st.text_input("Enter company name")
            if st.button("Add Company") and company_input:
                companies.append(company_input.strip())
                st.success(f"Added: {company_input}")
        
        elif input_method == "Upload CSV":
            st.subheader("Upload CSV File")
            uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
            if uploaded_file is not None:
                df = pd.read_csv(uploaded_file)
                if 'company' in df.columns:
                    companies = df['company'].tolist()
                    st.success(f"Loaded {len(companies)} companies from CSV")
                else:
                    st.error("CSV must have a 'company' column")
        
        elif input_method == "Paste List":
            st.subheader("Paste Company List")
            company_text = st.text_area("Enter companies (one per line)")
            if company_text:
                companies = [line.strip() for line in company_text.split('\n') if line.strip()]
                st.success(f"Found {len(companies)} companies")
        
        # Display current companies
        if companies:
            st.subheader("Target Companies")
            df_companies = pd.DataFrame(companies, columns=['Company'])
            st.dataframe(df_companies, use_container_width=True)
            
            # Run workflow button
            if st.button("🚀 Start Scraping", type="primary"):
                if export_method == "Google Sheets" and use_existing_sheet and not google_sheet_id:
                    st.error("Please provide a Google Sheet ID when using an existing sheet.")
                    st.stop()
                
                # Set environment variables
                import os
                os.environ['MAX_PEOPLE_PER_COMPANY'] = str(max_people_per_company)
                os.environ['SEARCH_KEYWORDS'] = search_keywords
                if export_method == "Google Sheets" and google_sheet_id:
                    os.environ['GOOGLE_SHEET_ID'] = google_sheet_id
                
                # Run workflow
                with st.spinner("Running LinkedIn scraping workflow..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        workflow = SimpleLinkedInWorkflow()
                        
                        if export_method == "CSV Export (Recommended)":
                            # Run CSV workflow
                            progress_bar.progress(20)
                            status_text.text("Starting CSV export workflow...")
                            
                            # Set filename if provided
                            filename = csv_filename if csv_filename else None
                            
                            result = workflow.run_csv_workflow(companies, filename)
                            
                            if result['success']:
                                progress_bar.progress(100)
                                status_text.text("✅ CSV export completed!")
                                
                                # Display success message
                                st.success(f"🎉 Successfully exported {result['contact_count']} contacts to CSV!")
                                st.info(f"📁 **File saved as:** `{result['filename']}`")
                                st.info(f"📂 **Full path:** `{result['filepath']}`")
                                
                                # Show sample data
                                if result['data']:
                                    st.subheader("📊 Sample Data Preview")
                                    sample_df = pd.DataFrame(result['data'][:5])  # Show first 5 rows
                                    st.dataframe(sample_df, use_container_width=True)
                                    
                                    # Download button
                                    import io
                                    csv_buffer = io.StringIO()
                                    sample_df.to_csv(csv_buffer, index=False)
                                    st.download_button(
                                        label="📥 Download Sample CSV",
                                        data=csv_buffer.getvalue(),
                                        file_name=f"sample_{result['filename']}",
                                        mime="text/csv"
                                    )
                                
                                # Instructions for next steps
                                st.subheader("📋 Next Steps")
                                st.markdown("""
                                1. **Open the CSV file** in Excel, Google Sheets, or any spreadsheet app
                                2. **Review the data** and add any additional information you need
                                3. **Import to Google Sheets** if you want to collaborate with others
                                4. **Use the data** for your outreach campaigns
                                
                                **💡 Tip:** You can manually upload the CSV to Google Sheets:
                                - Go to [Google Sheets](https://sheets.google.com)
                                - Click "File" → "Import" → "Upload"
                                - Select your CSV file
                                """)
                            else:
                                st.error(f"❌ CSV export failed: {result['error']}")
                        
                        else:  # Google Sheets workflow
                            # Update progress
                            progress_bar.progress(20)
                            status_text.text("Opening LinkedIn login page...")
                            
                            # Setup LinkedIn scraper
                            workflow.linkedin_scraper.setup_driver()
                            
                            if not workflow.linkedin_scraper.login_to_linkedin():
                                st.error("Failed to login to LinkedIn. Please try again.")
                                return
                            
                            progress_bar.progress(40)
                            status_text.text("Setting up Google Sheets...")
                            
                            # Setup Google Sheets - either create new or use existing
                            if use_existing_sheet:
                                if not workflow.sheets_manager.connect_to_sheet(google_sheet_id):
                                    st.error("Failed to connect to Google Sheet. Please check your Sheet ID and ensure the service account has access.")
                                    return
                                
                                # Add headers to the existing sheet
                                if not workflow.sheets_manager.add_headers_if_needed():
                                    st.error("Failed to add headers to Google Sheet")
                                    return
                                
                                final_sheet_id = google_sheet_id
                            else:
                                # Create new sheet automatically
                                final_sheet_id = workflow.sheets_manager.create_sheet_with_headers("LinkedIn Outreach Leads")
                                if not final_sheet_id:
                                    st.warning("⚠️ Could not create new Google Sheet (likely due to Drive quota). Please create a Google Sheet manually and use the 'Use existing sheet' option.")
                                    st.info("**To create a Google Sheet manually:**\n1. Go to [Google Sheets](https://sheets.google.com)\n2. Create a new sheet\n3. Copy the Sheet ID from the URL\n4. Check 'Use existing sheet' and paste the ID")
                                    return
                                
                                st.success(f"✅ Created new Google Sheet! ID: {final_sheet_id}")
                            
                            progress_bar.progress(60)
                            status_text.text("Processing companies and finding people...")
                            
                            # Process companies
                            all_people_data = []
                            for i, company in enumerate(companies):
                                status_text.text(f"Processing {company}...")
                                
                                people_data = workflow.linkedin_scraper.search_people_by_company(company)
                                
                                if people_data:
                                    all_people_data.extend(people_data)
                                    workflow.sheets_manager.add_people_data(people_data)
                                
                                progress_bar.progress(60 + (20 * (i + 1) / len(companies)))
                                time.sleep(2)  # Rate limiting
                            
                            progress_bar.progress(90)
                            status_text.text("Generating summary...")
                            
                            # Generate summary
                        workflow._generate_summary_report(all_people_data, final_sheet_id)
                        
                        progress_bar.progress(100)
                        status_text.text("Workflow completed!")
                        
                        st.success("🎉 LinkedIn scraping completed successfully!")
                        
                        # Show Google Sheet info
                        if not use_existing_sheet:
                            st.info(f"📊 **Your new Google Sheet:** [Open Sheet]({workflow.sheets_manager.get_sheet_url()})")
                        
                        # Store results in session state
                        st.session_state['people_data'] = all_people_data
                        st.session_state['companies'] = companies
                        st.session_state['sheet_id'] = final_sheet_id
                        
                    except Exception as e:
                        st.error(f"Error running workflow: {str(e)}")
                    finally:
                        workflow.linkedin_scraper.close()
    
    with tab2:
        st.header("Results & Data")
        
        if 'people_data' in st.session_state and st.session_state['people_data']:
            people_data = st.session_state['people_data']
            
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total People", len(people_data))
            
            with col2:
                scu_alumni = len([p for p in people_data if p.get('is_scu_alumni', False)])
                st.metric("SCU Alumni", scu_alumni)
            
            with col3:
                non_alumni = len(people_data) - scu_alumni
                st.metric("Non-Alumni", non_alumni)
            
            with col4:
                companies_found = len(set([p.get('company', '') for p in people_data]))
                st.metric("Companies", companies_found)
            
            # Data table
            st.subheader("Contact Data")
            
            # Create DataFrame for display
            df_data = []
            for person in people_data:
                df_data.append({
                    'Name': person.get('name', ''),
                    'Title': person.get('title', ''),
                    'Company': person.get('company', ''),
                    'Location': person.get('location', ''),
                    'SCU Alumni': 'Yes' if person.get('is_scu_alumni', False) else 'No',
                    'Profile URL': person.get('profile_url', '')
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # Download options
            st.subheader("Download Data")
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="linkedin_contacts.csv",
                mime="text/csv"
            )
            
        else:
            st.info("No data available. Run the scraping workflow first.")
    
    with tab3:
        st.header("Setup Guide")
        
        st.subheader("Required Setup")
        
        st.markdown("""
        ### 1. Google Sheets Setup (Required)
        
        1. Go to [Google Cloud Console](https://console.cloud.google.com/)
        2. Create a new project or select an existing one
        3. Enable Google Sheets API and Google Drive API
        4. Create service account credentials
        5. Download the JSON file and save as `credentials.json` in the project directory
        6. Share your Google Sheet with the service account email (if using existing sheet)
        
        ### 2. LinkedIn Credentials
        - Use your regular LinkedIn email and password
        - Make sure 2FA is disabled for automation
        - Consider using a dedicated account for scraping
        
        ### 3. Running the App
        ```bash
        pip install -r requirements.txt
        streamlit run simple_app.py
        ```
        """)
        
        st.subheader("What This Tool Does")
        
        st.markdown("""
        - **Scrapes LinkedIn** for people at target companies
        - **Detects SCU alumni** automatically
        - **Creates Google Sheets automatically** with columns for:
          - Name
          - Title/Position
          - Company
          - Location
          - Profile URL
          - SCU Alumni (Yes/No)
          - Email (blank for manual entry)
          - Date Added
          - Status
          - Notes
        
        ### Next Steps After Scraping
        1. The app will automatically create a new Google Sheet for you
        2. Review the Google Sheet with all your scraped data
        3. Manually add email addresses in the Email column
        4. Use the data for your outreach campaigns
        5. Track responses and follow-ups
        """)
        
        st.subheader("File Structure")
        st.code("""
        linkedin_outreach_platform/
        ├── simple_app.py              # Streamlit web interface
        ├── simple_workflow.py         # Main workflow
        ├── linkedin_scraper.py        # LinkedIn scraping
        ├── google_sheets_manager.py   # Google Sheets integration
        ├── config.py                  # Configuration
        ├── requirements.txt           # Dependencies
        ├── credentials.json           # Google service account
        └── README.md                  # Documentation
        """)

if __name__ == "__main__":
    main()