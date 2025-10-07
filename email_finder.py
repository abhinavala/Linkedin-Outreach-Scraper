import requests
import time
import logging
from config import Config

class EmailFinder:
    def __init__(self):
        self.api_key = Config.HUNTER_API_KEY
        self.base_url = Config.HUNTER_BASE_URL
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def find_email(self, first_name, last_name, company_domain):
        """Find email using Hunter.io API"""
        try:
            self.logger.info(f"Searching for email: {first_name} {last_name} at {company_domain}")
            
            # Hunter.io email finder endpoint
            url = f"{self.base_url}/email-finder"
            
            params = {
                'api_key': self.api_key,
                'domain': company_domain,
                'first_name': first_name,
                'last_name': last_name
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('data') and data['data'].get('email'):
                email_data = data['data']
                return {
                    'email': email_data['email'],
                    'confidence': email_data.get('score', 0),
                    'sources': email_data.get('sources', []),
                    'status': 'found'
                }
            else:
                self.logger.warning(f"No email found for {first_name} {last_name} at {company_domain}")
                return {
                    'email': None,
                    'confidence': 0,
                    'sources': [],
                    'status': 'not_found'
                }
                
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            return {
                'email': None,
                'confidence': 0,
                'sources': [],
                'status': 'error'
            }
        except Exception as e:
            self.logger.error(f"Error finding email: {str(e)}")
            return {
                'email': None,
                'confidence': 0,
                'sources': [],
                'status': 'error'
            }
    
    def verify_email(self, email):
        """Verify email using Hunter.io verification API"""
        try:
            self.logger.info(f"Verifying email: {email}")
            
            url = f"{self.base_url}/email-verifier"
            
            params = {
                'api_key': self.api_key,
                'email': email
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('data'):
                verification_data = data['data']
                return {
                    'email': email,
                    'status': verification_data.get('result', 'unknown'),
                    'score': verification_data.get('score', 0),
                    'sources': verification_data.get('sources', []),
                    'smtp_server': verification_data.get('smtp_server'),
                    'smtp_check': verification_data.get('smtp_check', False)
                }
            else:
                return {
                    'email': email,
                    'status': 'unknown',
                    'score': 0,
                    'sources': [],
                    'smtp_server': None,
                    'smtp_check': False
                }
                
        except Exception as e:
            self.logger.error(f"Error verifying email {email}: {str(e)}")
            return {
                'email': email,
                'status': 'error',
                'score': 0,
                'sources': [],
                'smtp_server': None,
                'smtp_check': False
            }
    
    def get_company_domain(self, company_name):
        """Extract domain from company name (simplified approach)"""
        # This is a simplified approach - in practice, you might want to use
        # a more sophisticated method to get the actual company domain
        company_domain = company_name.lower().replace(' ', '').replace('inc', '').replace('llc', '').replace('corp', '')
        return f"{company_domain}.com"
    
    def find_emails_for_people(self, people_data):
        """Find emails for a list of people"""
        results = []
        
        for person in people_data:
            try:
                # Extract first and last name
                name_parts = person.get('name', '').split()
                if len(name_parts) >= 2:
                    first_name = name_parts[0]
                    last_name = ' '.join(name_parts[1:])
                else:
                    first_name = name_parts[0] if name_parts else ''
                    last_name = ''
                
                # Get company domain
                company = person.get('company', '')
                company_domain = self.get_company_domain(company)
                
                # Find email
                email_result = self.find_email(first_name, last_name, company_domain)
                
                # Combine person data with email data
                person_with_email = {
                    **person,
                    'first_name': first_name,
                    'last_name': last_name,
                    'company_domain': company_domain,
                    'email': email_result['email'],
                    'email_confidence': email_result['confidence'],
                    'email_sources': email_result['sources'],
                    'email_status': email_result['status']
                }
                
                results.append(person_with_email)
                
                # Rate limiting - Hunter.io has limits
                time.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Error processing person {person.get('name', 'Unknown')}: {str(e)}")
                # Add person without email data
                results.append({
                    **person,
                    'email': None,
                    'email_confidence': 0,
                    'email_sources': [],
                    'email_status': 'error'
                })
        
        return results