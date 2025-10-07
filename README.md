# LinkedIn Outreach Platform

An AI-powered platform for automated LinkedIn networking and referral outreach. This tool helps you find people at target companies, discover their email addresses, and send personalized outreach messages.

## Features

- 🔍 **LinkedIn Scraping**: Automatically find people at target companies
- 📧 **Email Discovery**: Use Hunter.io to find email addresses
- 🤖 **AI-Powered Messages**: Generate personalized outreach messages using OpenAI
- 📊 **Google Sheets Integration**: Store and manage all data in Google Sheets
- 📬 **GMass Integration**: Create and manage email campaigns
- 🎯 **SCU Alumni Detection**: Automatically detect and personalize messages for SCU alumni
- 🌐 **Web Interface**: Easy-to-use Streamlit interface

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

Create a `.env` file in the project directory:

```env
# LinkedIn Credentials
LINKEDIN_EMAIL=your_linkedin_email@example.com
LINKEDIN_PASSWORD=your_linkedin_password

# Hunter.io API Key
HUNTER_API_KEY=your_hunter_api_key

# OpenAI API Key
OPENAI_API_KEY=your_openai_api_key

# GMass API Key
GMASS_API_KEY=your_gmass_api_key

# Google Sheets Configuration
GOOGLE_SHEET_ID=your_google_sheet_id
```

### 3. Google Sheets Setup

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable Google Sheets API and Google Drive API
4. Create service account credentials
5. Download the JSON file and save as `credentials.json` in the project directory
6. Share your Google Sheet with the service account email

### 4. API Keys Setup

- **Hunter.io**: Get API key from [hunter.io](https://hunter.io/)
- **OpenAI**: Get API key from [OpenAI Platform](https://platform.openai.com/)
- **GMass**: Get API key from [GMass](https://www.gmass.co/)

## Usage

### Web Interface (Recommended)

Run the Streamlit app:

```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

### Command Line

```python
from main_workflow import LinkedInOutreachWorkflow

# Define target companies
companies = ["TikTok", "Pinterest", "Google", "Meta", "Apple"]

# Run workflow
workflow = LinkedInOutreachWorkflow()
success = workflow.run_complete_workflow(companies, create_new_sheet=True)
```

## Workflow

1. **Company Input**: Enter target companies manually, upload CSV, or paste a list
2. **LinkedIn Scraping**: Automatically search for people at each company
3. **Email Discovery**: Use Hunter.io to find email addresses
4. **AI Message Generation**: Create personalized outreach messages
5. **Google Sheets Storage**: Store all data in organized spreadsheets
6. **GMass Campaigns**: Create email campaigns for outreach

## Message Personalization

The platform automatically generates personalized messages based on:

- **Company Information**: Uses AI to understand company mission and values
- **SCU Alumni Detection**: Special messages for fellow SCU alumni
- **Personal Details**: Incorporates person's name, title, and company
- **Professional Tone**: Maintains appropriate professional networking language

### Sample Messages

**For SCU Alumni:**
```
Hello Frank,

I hope this message finds you well. My name is Abhinav Ala, and I'm currently a Computer Science Engineering student at Santa Clara University. I came across your profile and was truly inspired by your path from SCU to your role at TikTok...

[Personalized content based on company and role]
```

**For Non-Alumni:**
```
Hello Graham,

I hope this message finds you well. My name is Abhinav Ala, and I'm currently a Computer Science and Engineering student at Santa Clara University. I came across your profile and was really inspired by your career journey and the path that led you to Pinterest...

[Personalized content based on company and role]
```

## File Structure

```
linkedin_outreach_platform/
├── app.py                          # Streamlit web interface
├── main_workflow.py                # Main workflow orchestrator
├── linkedin_scraper.py             # LinkedIn scraping functionality
├── email_finder.py                 # Hunter.io email discovery
├── google_sheets_manager.py        # Google Sheets integration
├── gmass_integration.py            # GMass email campaigns
├── ai_message_generator.py         # AI-powered message generation
├── config.py                       # Configuration management
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── credentials.json                # Google service account credentials
```

## Important Notes

- **Rate Limiting**: The platform includes delays to respect LinkedIn's rate limits
- **Ethical Use**: Always follow LinkedIn's terms of service and professional networking etiquette
- **Data Privacy**: Handle personal data responsibly and in compliance with privacy laws
- **API Limits**: Be aware of API rate limits for Hunter.io, OpenAI, and GMass

## Troubleshooting

### Common Issues

1. **LinkedIn Login Failed**: Check credentials and ensure 2FA is disabled
2. **Google Sheets Access Denied**: Verify service account has proper permissions
3. **API Rate Limits**: Wait and retry, or upgrade API plans
4. **Chrome Driver Issues**: The app automatically downloads the correct Chrome driver

### Support

For issues or questions, check the logs in the console output or contact the development team.

## Legal Disclaimer

This tool is for educational and professional networking purposes only. Users are responsible for complying with all applicable laws, terms of service, and professional ethics. Always respect people's privacy and professional boundaries.