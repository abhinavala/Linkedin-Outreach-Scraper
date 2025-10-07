# LinkedIn Contact Scraper

A simplified LinkedIn scraping tool that finds people at target companies and exports their information to Google Sheets for manual email entry.

## Features

- 🔍 **LinkedIn Scraping**: Automatically find people at target companies
- 📊 **Google Sheets Integration**: Export data to organized spreadsheets
- 🎯 **SCU Alumni Detection**: Automatically detect SCU alumni
- 🌐 **Web Interface**: Easy-to-use Streamlit interface
- 📝 **Manual Email Entry**: Blank email column for your own research

## What You Get

The tool populates a Google Sheet with:
- **Name**: Person's full name
- **Title**: Their job title/position
- **Company**: Company they work for
- **Location**: Their location
- **Profile URL**: Link to their LinkedIn profile
- **SCU Alumni**: Yes/No if they're an SCU alumni
- **Email**: Blank column for you to fill in manually
- **Date Added**: When the record was added
- **Status**: New/Contacted/Responded/etc.
- **Notes**: Space for your notes

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Google Sheets Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable Google Sheets API and Google Drive API
4. Create service account credentials
5. Download the JSON file and save as `credentials.json` in the project directory

### 3. Run the App

```bash
streamlit run simple_app.py
```

## Usage

1. **Enter LinkedIn credentials** in the sidebar
2. **Add target companies** (manual input, CSV upload, or paste list)
3. **Click "Start Scraping"** to run the workflow
4. **Review results** in the Google Sheet
5. **Manually add email addresses** in the Email column
6. **Use the data** for your outreach campaigns

## Required API Keys

**None!** This simplified version only needs:
- Your LinkedIn credentials
- Google Sheets service account (free)

## File Structure

```
linkedin_outreach_platform/
├── simple_app.py              # Streamlit web interface
├── simple_workflow.py         # Main workflow
├── linkedin_scraper.py        # LinkedIn scraping
├── google_sheets_manager.py   # Google Sheets integration
├── config.py                  # Configuration
├── requirements.txt           # Dependencies
├── credentials.json           # Google service account (you create this)
└── SIMPLE_README.md           # This file
```

## Example Workflow

1. **Input companies**: TikTok, Pinterest, Google, Meta, Apple
2. **Scrape LinkedIn**: Find people at each company
3. **Export to Google Sheets**: All data organized in columns
4. **Manual email research**: Use tools like Hunter.io, Apollo, or manual research
5. **Outreach**: Use the data for your networking campaigns

## Benefits of This Approach

- **No API costs**: Only uses free Google Sheets
- **Full control**: You research and add emails manually
- **Better quality**: Manual email research often finds more accurate emails
- **Privacy compliant**: You control all data and outreach
- **Flexible**: Easy to customize for your specific needs

## Next Steps After Scraping

1. **Review the Google Sheet** for accuracy
2. **Research email addresses** using your preferred method
3. **Add emails manually** to the Email column
4. **Create outreach campaigns** using the organized data
5. **Track responses** using the Status and Notes columns

## Troubleshooting

- **LinkedIn Login Issues**: Make sure 2FA is disabled
- **Google Sheets Access**: Verify service account has proper permissions
- **Chrome Driver Issues**: The app automatically downloads the correct driver

## Legal Disclaimer

This tool is for educational and professional networking purposes only. Always respect LinkedIn's terms of service and professional networking etiquette.