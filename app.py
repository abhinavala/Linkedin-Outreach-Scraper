import streamlit as st
import pandas as pd
import time
from main_workflow import LinkedInOutreachWorkflow
from google_sheets_manager import GoogleSheetsManager
from gmass_integration import GMassIntegration
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    st.set_page_config(
        page_title="LinkedIn Outreach Platform",
        page_icon="🚀",
        layout="wide"
    )
    
    st.title("🚀 LinkedIn Outreach Platform")
    st.markdown("**Automate your networking and referral outreach with AI-powered personalized messages**")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # API Keys section
    st.sidebar.subheader("API Keys")
    linkedin_email = st.sidebar.text_input("LinkedIn Email", type="password")
    linkedin_password = st.sidebar.text_input("LinkedIn Password", type="password")
    hunter_api_key = st.sidebar.text_input("Hunter.io API Key", type="password")
    openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")
    gmass_api_key = st.sidebar.text_input("GMass API Key", type="password")
    
    # Google Sheets configuration
    st.sidebar.subheader("Google Sheets")
    google_sheet_id = st.sidebar.text_input("Google Sheet ID")
    use_existing_sheet = st.sidebar.checkbox("Use existing sheet", value=False)
    
    # Search configuration
    st.sidebar.subheader("Search Settings")
    max_people_per_company = st.sidebar.slider("Max people per company", 10, 100, 50)
    search_keywords = st.sidebar.text_area(
        "Search Keywords (comma-separated)", 
        value="software engineer,data scientist,product manager,marketing manager"
    )
    
    # Main content area
    tab1, tab2, tab3, tab4 = st.tabs(["🏢 Company Input", "📊 Results", "📧 Email Campaigns", "⚙️ Settings"])
    
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
            if st.button("🚀 Start Outreach Workflow", type="primary"):
                if not all([linkedin_email, linkedin_password, hunter_api_key, openai_api_key]):
                    st.error("Please provide all required API keys in the sidebar")
                else:
                    # Set environment variables
                    import os
                    os.environ['LINKEDIN_EMAIL'] = linkedin_email
                    os.environ['LINKEDIN_PASSWORD'] = linkedin_password
                    os.environ['HUNTER_API_KEY'] = hunter_api_key
                    os.environ['OPENAI_API_KEY'] = openai_api_key
                    os.environ['GMASS_API_KEY'] = gmass_api_key
                    os.environ['MAX_PEOPLE_PER_COMPANY'] = str(max_people_per_company)
                    os.environ['SEARCH_KEYWORDS'] = search_keywords
                    
                    if google_sheet_id:
                        os.environ['GOOGLE_SHEET_ID'] = google_sheet_id
                    
                    # Run workflow
                    with st.spinner("Running outreach workflow..."):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            workflow = LinkedInOutreachWorkflow()
                            
                            # Update progress
                            progress_bar.progress(20)
                            status_text.text("Logging into LinkedIn...")
                            
                            # Setup LinkedIn scraper
                            workflow.linkedin_scraper.setup_driver()
                            
                            if not workflow.linkedin_scraper.login_to_linkedin():
                                st.error("Failed to login to LinkedIn")
                                return
                            
                            progress_bar.progress(40)
                            status_text.text("Setting up Google Sheets...")
                            
                            # Setup Google Sheets
                            if use_existing_sheet and google_sheet_id:
                                if not workflow.sheets_manager.connect_to_sheet(google_sheet_id):
                                    st.error("Failed to connect to Google Sheet")
                                    return
                            else:
                                sheet_id = workflow.sheets_manager.create_sheet_with_headers("LinkedIn Outreach Leads")
                                if not sheet_id:
                                    st.error("Failed to create Google Sheet")
                                    return
                            
                            progress_bar.progress(60)
                            status_text.text("Processing companies and finding people...")
                            
                            # Process companies
                            all_people_data = []
                            for i, company in enumerate(companies):
                                status_text.text(f"Processing {company}...")
                                
                                people_data = workflow.linkedin_scraper.search_people_by_company(company)
                                
                                if people_data:
                                    people_with_emails = workflow.email_finder.find_emails_for_people(people_data)
                                    people_with_messages = workflow.ai_generator.generate_bulk_messages(people_with_emails)
                                    all_people_data.extend(people_with_messages)
                                    workflow.sheets_manager.add_people_data(people_with_messages)
                                
                                progress_bar.progress(60 + (20 * (i + 1) / len(companies)))
                                time.sleep(2)  # Rate limiting
                            
                            progress_bar.progress(90)
                            status_text.text("Creating email campaigns...")
                            
                            # Create GMass campaigns
                            workflow._create_gmass_campaigns(all_people_data)
                            
                            progress_bar.progress(100)
                            status_text.text("Workflow completed!")
                            
                            st.success("🎉 Outreach workflow completed successfully!")
                            
                            # Store results in session state
                            st.session_state['people_data'] = all_people_data
                            st.session_state['companies'] = companies
                            
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
                people_with_emails = len([p for p in people_data if p.get('email')])
                st.metric("With Emails", people_with_emails)
            
            with col3:
                scu_alumni = len([p for p in people_data if p.get('is_scu_alumni', False)])
                st.metric("SCU Alumni", scu_alumni)
            
            with col4:
                companies_found = len(set([p.get('company', '') for p in people_data]))
                st.metric("Companies", companies_found)
            
            # Data table
            st.subheader("People Data")
            
            # Create DataFrame for display
            df_data = []
            for person in people_data:
                df_data.append({
                    'Name': person.get('name', ''),
                    'Title': person.get('title', ''),
                    'Company': person.get('company', ''),
                    'Email': person.get('email', ''),
                    'Email Confidence': person.get('email_confidence', 0),
                    'SCU Alumni': 'Yes' if person.get('is_scu_alumni', False) else 'No',
                    'Location': person.get('location', '')
                })
            
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
            
            # Download options
            st.subheader("Download Data")
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="linkedin_outreach_data.csv",
                mime="text/csv"
            )
            
        else:
            st.info("No data available. Run the outreach workflow first.")
    
    with tab3:
        st.header("Email Campaigns")
        
        if 'people_data' in st.session_state and st.session_state['people_data']:
            people_data = st.session_state['people_data']
            
            # Separate SCU alumni and non-alumni
            scu_alumni = [p for p in people_data if p.get('is_scu_alumni', False) and p.get('email')]
            non_alumni = [p for p in people_data if not p.get('is_scu_alumni', False) and p.get('email')]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("SCU Alumni Campaign")
                st.metric("Recipients", len(scu_alumni))
                
                if scu_alumni:
                    # Show sample message
                    sample_person = scu_alumni[0]
                    st.text_area(
                        "Sample Message",
                        value=sample_person.get('message_body', ''),
                        height=300
                    )
            
            with col2:
                st.subheader("General Networking Campaign")
                st.metric("Recipients", len(non_alumni))
                
                if non_alumni:
                    # Show sample message
                    sample_person = non_alumni[0]
                    st.text_area(
                        "Sample Message",
                        value=sample_person.get('message_body', ''),
                        height=300
                    )
            
            # Campaign management
            st.subheader("Campaign Management")
            
            if st.button("Create GMass Campaigns"):
                if not gmass_api_key:
                    st.error("Please provide GMass API key in the sidebar")
                else:
                    with st.spinner("Creating campaigns..."):
                        try:
                            gmass = GMassIntegration()
                            
                            if scu_alumni:
                                result = gmass.create_campaign(
                                    "SCU Alumni Outreach",
                                    "Coffee Chat Request - SCU Connection",
                                    scu_alumni[0].get('message_body', ''),
                                    scu_alumni
                                )
                                if result:
                                    st.success("SCU Alumni campaign created!")
                            
                            if non_alumni:
                                result = gmass.create_campaign(
                                    "Professional Networking",
                                    "Connecting - Professional Networking",
                                    non_alumni[0].get('message_body', ''),
                                    non_alumni
                                )
                                if result:
                                    st.success("General networking campaign created!")
                            
                        except Exception as e:
                            st.error(f"Error creating campaigns: {str(e)}")
        else:
            st.info("No data available. Run the outreach workflow first.")
    
    with tab4:
        st.header("Settings & Configuration")
        
        st.subheader("Environment Variables")
        st.code("""
# Create a .env file in your project directory with:
LINKEDIN_EMAIL=your_linkedin_email@example.com
LINKEDIN_PASSWORD=your_linkedin_password
HUNTER_API_KEY=your_hunter_api_key
OPENAI_API_KEY=your_openai_api_key
GMASS_API_KEY=your_gmass_api_key
GOOGLE_SHEET_ID=your_google_sheet_id
        """)
        
        st.subheader("Google Sheets Setup")
        st.markdown("""
        1. Go to [Google Cloud Console](https://console.cloud.google.com/)
        2. Create a new project or select existing one
        3. Enable Google Sheets API and Google Drive API
        4. Create service account credentials
        5. Download the JSON file and save as `credentials.json`
        6. Share your Google Sheet with the service account email
        """)
        
        st.subheader("API Keys Setup")
        st.markdown("""
        - **Hunter.io**: Get API key from [hunter.io](https://hunter.io/)
        - **OpenAI**: Get API key from [OpenAI Platform](https://platform.openai.com/)
        - **GMass**: Get API key from [GMass](https://www.gmass.co/)
        """)

if __name__ == "__main__":
    main()