# LinkedIn Contact Scraper - Setup Guide

## Step-by-Step Setup Instructions

### 1. Install Python Dependencies

```bash
# Make sure you're in the project directory
cd /Users/abhinavala/linkedin_outreach_platform

# Install required packages
pip install -r requirements.txt
```

### 2. Set Up Google Sheets API (Required)

#### 2.1 Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "LinkedIn Scraper" (or any name you prefer)
4. Click "Create"

#### 2.2 Enable APIs
1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google Sheets API" and enable it
3. Search for "Google Drive API" and enable it

#### 2.3 Create Service Account
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "Service Account"
3. Name it "linkedin-scraper-service"
4. Click "Create and Continue"
5. Skip the optional steps and click "Done"

#### 2.4 Download Credentials
1. Click on your service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create new key"
4. Choose "JSON" format
5. Download the file and rename it to `credentials.json`
6. Move `credentials.json` to your project directory: `/Users/abhinavala/linkedin_outreach_platform/`

### 3. Test the Setup

```bash
# Test if everything is installed correctly
python -c "import selenium, gspread, streamlit; print('All packages installed successfully!')"
```

### 4. Run the Application

```bash
# Start the Streamlit app
streamlit run simple_app.py
```

The app will open in your browser at `http://localhost:8501`

## How to Use the App

### 1. Enter LinkedIn Credentials
- In the sidebar, enter your LinkedIn email and password
- **Important**: Make sure 2FA is disabled on your LinkedIn account

### 2. Add Target Companies
You can add companies in three ways:
- **Manual Input**: Type company names one by one
- **Upload CSV**: Upload a CSV file with a 'company' column
- **Paste List**: Paste a list of companies (one per line)

### 3. Configure Search Settings
- **Max people per company**: How many people to find (10-100)
- **Search Keywords**: CS/Engineering keywords (already set to focus on tech roles)

### 4. Start Scraping
- Click "🚀 Start Scraping"
- The app will:
  - Log into LinkedIn
  - Automatically create a new Google Sheet for you
  - Search for CS/Engineering people at each company
  - Export all data to the Google Sheet

### 5. Review Results
- Check the "Results & Data" tab to see the scraped data
- Download the data as CSV if needed
- The Google Sheet will have all the data organized

## What You'll Get

The Google Sheet will contain:
- **Name**: Person's full name
- **Title**: Their job title (focused on CS/Engineering roles)
- **Company**: Company they work for
- **Location**: Their location
- **Profile URL**: Link to their LinkedIn profile
- **SCU Alumni**: Yes/No if they're an SCU alumni
- **Email**: Blank column for you to fill in manually
- **Date Added**: When the record was added
- **Status**: New/Contacted/Responded/etc.
- **Notes**: Space for your notes

## Troubleshooting

### Common Issues:

1. **"Failed to login to LinkedIn"**
   - Make sure 2FA is disabled
   - Check your email/password
   - Try logging into LinkedIn manually first

2. **"Failed to create Google Sheet"**
   - Check that `credentials.json` is in the project directory
   - Verify the Google Sheets API is enabled
   - Make sure the service account has proper permissions
   - If you hit quota limits, you can use an existing sheet instead

3. **"Chrome driver issues"**
   - The app automatically downloads Chrome driver
   - Make sure you have Chrome browser installed
   - Try restarting the app

4. **"No people found"**
   - Try different company names
   - Check if the company exists on LinkedIn
   - Try adjusting the search keywords

### Getting Help:

If you encounter issues:
1. Check the terminal/console for error messages
2. Make sure all dependencies are installed
3. Verify your Google Sheets setup
4. Check that LinkedIn credentials are correct

## Next Steps After Setup

1. **Test with one company first** (e.g., "Google")
2. **Review the results** in the Google Sheet
3. **Manually research email addresses** for the people you want to contact
4. **Add emails to the Email column** in the Google Sheet
5. **Use the data for your outreach campaigns**

## Security Notes

- Keep your `credentials.json` file secure
- Don't share your LinkedIn credentials
- The app only reads public LinkedIn data
- All data is stored in your own Google Sheet

## Cost

- **Google Sheets**: Free
- **LinkedIn**: Free (your existing account)
- **Total cost**: $0

The app is completely free to use!