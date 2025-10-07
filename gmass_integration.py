import requests
import json
import logging
from config import Config

class GMassIntegration:
    def __init__(self):
        self.api_key = Config.GMASS_API_KEY
        self.base_url = "https://api.gmass.co"
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def create_campaign(self, campaign_name, subject, body, recipients_data):
        """Create a new email campaign in GMass"""
        try:
            self.logger.info(f"Creating GMass campaign: {campaign_name}")
            
            url = f"{self.base_url}/api/campaigns"
            
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Prepare recipients
            recipients = []
            for person in recipients_data:
                if person.get('email') and person.get('email_status') == 'found':
                    recipients.append({
                        'email': person['email'],
                        'name': person.get('name', ''),
                        'first_name': person.get('first_name', ''),
                        'last_name': person.get('last_name', ''),
                        'company': person.get('company', ''),
                        'title': person.get('title', '')
                    })
            
            campaign_data = {
                'name': campaign_name,
                'subject': subject,
                'body': body,
                'recipients': recipients,
                'settings': {
                    'track_opens': True,
                    'track_clicks': True,
                    'schedule_send': False
                }
            }
            
            response = requests.post(url, headers=headers, json=campaign_data)
            response.raise_for_status()
            
            result = response.json()
            self.logger.info(f"Campaign created successfully: {result.get('campaign_id')}")
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Error creating campaign: {str(e)}")
            return None
    
    def get_campaign_templates(self):
        """Get available email templates"""
        try:
            url = f"{self.base_url}/api/templates"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Error getting templates: {str(e)}")
            return []
    
    def create_referral_template(self):
        """Create a professional referral request template"""
        template = {
            'name': 'LinkedIn Referral Request',
            'subject': 'Coffee Chat Request - {{first_name}}',
            'body': '''
Hi {{first_name}},

I hope this email finds you well. I came across your profile on LinkedIn and was impressed by your work at {{company}} as a {{title}}.

I'm currently seeking internship opportunities in the tech industry and would love to learn more about your experience and insights. Would you be open to a brief 15-20 minute coffee chat or virtual call? I'd be happy to work around your schedule.

I'm particularly interested in:
- Learning about your career journey
- Understanding the day-to-day work in your role
- Getting advice on breaking into the industry
- Potentially discussing referral opportunities

I understand you're busy, so I completely understand if you're not available. Either way, I'd be grateful for any advice you might have.

Thank you for your time, and I look forward to hearing from you.

Best regards,
[Your Name]
[Your Contact Information]
[Your LinkedIn Profile]

P.S. I found your email through professional networking - if you'd prefer I reach out through LinkedIn instead, please let me know!
'''
        }
        return template
    
    def create_networking_template(self):
        """Create a networking template"""
        template = {
            'name': 'Professional Networking',
            'subject': 'Connecting with {{first_name}} - {{company}}',
            'body': '''
Hi {{first_name}},

I hope you're doing well. I noticed your impressive background at {{company}} and thought it would be great to connect.

I'm a [your current status - student, recent grad, etc.] with a passion for [your field of interest]. I'm always looking to expand my network and learn from experienced professionals like yourself.

Would you be open to a brief virtual coffee chat? I'd love to:
- Learn about your career path and experiences
- Get insights about the industry
- Discuss potential opportunities or connections

I completely understand if you're busy - no pressure at all. Even a quick LinkedIn message exchange would be valuable.

Thank you for considering, and I hope to connect soon!

Best,
[Your Name]
[Your Contact Information]
'''
        }
        return template
    
    def send_test_email(self, campaign_id, test_email):
        """Send a test email for a campaign"""
        try:
            url = f"{self.base_url}/api/campaigns/{campaign_id}/test"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'test_email': test_email
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            self.logger.info(f"Test email sent to {test_email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending test email: {str(e)}")
            return False
    
    def schedule_campaign(self, campaign_id, send_time):
        """Schedule a campaign to be sent at a specific time"""
        try:
            url = f"{self.base_url}/api/campaigns/{campaign_id}/schedule"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'send_time': send_time
            }
            
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            self.logger.info(f"Campaign scheduled for {send_time}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error scheduling campaign: {str(e)}")
            return False
    
    def get_campaign_stats(self, campaign_id):
        """Get statistics for a campaign"""
        try:
            url = f"{self.base_url}/api/campaigns/{campaign_id}/stats"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            self.logger.error(f"Error getting campaign stats: {str(e)}")
            return None