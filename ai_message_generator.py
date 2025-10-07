import openai
import logging
import re
from config import Config

class AIMessageGenerator:
    def __init__(self):
        self.setup_logging()
        # Set OpenAI API key
        openai.api_key = Config.OPENAI_API_KEY
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def check_if_scu_alumni(self, person_data):
        """Check if the person is an SCU alumni based on their profile data"""
        try:
            # Look for SCU-related keywords in title, company, or location
            scu_keywords = [
                'santa clara university', 'scu', 'santa clara', 
                'bronco', 'broncos', 'santa clara university'
            ]
            
            profile_text = ' '.join([
                person_data.get('title', ''),
                person_data.get('company', ''),
                person_data.get('location', ''),
                person_data.get('name', '')
            ]).lower()
            
            for keyword in scu_keywords:
                if keyword in profile_text:
                    return True
                    
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking SCU alumni status: {str(e)}")
            return False
    
    def get_company_info(self, company_name):
        """Get company information using AI to understand their mission and values"""
        try:
            prompt = f"""
            Please provide a brief overview of {company_name} including:
            1. Their main mission/purpose
            2. What they do (products/services)
            3. Their core values
            4. Why someone might want to work there
            5. Their company culture (if known)
            
            Keep it concise and professional. Format as a structured response.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides company information for professional networking purposes."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            self.logger.error(f"Error getting company info: {str(e)}")
            return f"Information about {company_name} not available."
    
    def generate_personalized_message(self, person_data, company_info=None):
        """Generate a personalized outreach message"""
        try:
            is_scu_alumni = self.check_if_scu_alumni(person_data)
            company_name = person_data.get('company', 'this company')
            person_name = person_data.get('first_name', 'there')
            person_title = person_data.get('title', 'professional')
            
            if not company_info:
                company_info = self.get_company_info(company_name)
            
            # Create the prompt for message generation
            prompt = f"""
            Generate a personalized LinkedIn outreach message for Abhinav Ala, a Computer Science Engineering student at Santa Clara University, to reach out to {person_name} who works as a {person_title} at {company_name}.
            
            Person details:
            - Name: {person_name}
            - Title: {person_title}
            - Company: {company_name}
            - Is SCU Alumni: {is_scu_alumni}
            
            Company information:
            {company_info}
            
            Requirements:
            1. Use a professional but warm tone
            2. Mention Abhinav is a CS student at SCU
            3. Show genuine interest in their career journey
            4. If they're an SCU alumni, mention the shared connection
            5. Reference the company's mission/values if relevant
            6. Ask for a brief coffee chat or virtual call
            7. Mention interest in 2026 Software Engineer Internship
            8. Keep it concise (under 200 words)
            9. Include Abhinav's contact info: (469)-381-4729, aala@scu.edu
            
            Format the message exactly like this:
            Subject: [Appropriate subject line]
            
            [Message body]
            
            Best regards,
            Abhinav Ala
            (469)-381-4729
            aala@scu.edu
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional networking assistant that creates personalized outreach messages for students seeking internships."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.8
            )
            
            generated_message = response.choices[0].message.content.strip()
            
            # Parse subject and body
            subject, body = self._parse_message(generated_message)
            
            return {
                'subject': subject,
                'body': body,
                'is_scu_alumni': is_scu_alumni,
                'company_info': company_info
            }
            
        except Exception as e:
            self.logger.error(f"Error generating personalized message: {str(e)}")
            # Return fallback message
            return self._get_fallback_message(person_data, is_scu_alumni)
    
    def _parse_message(self, message_text):
        """Parse the generated message to extract subject and body"""
        try:
            lines = message_text.split('\n')
            subject = "Coffee Chat Request"
            body = message_text
            
            # Look for subject line
            for i, line in enumerate(lines):
                if line.strip().startswith('Subject:'):
                    subject = line.replace('Subject:', '').strip()
                    body = '\n'.join(lines[i+1:]).strip()
                    break
            
            return subject, body
            
        except Exception as e:
            self.logger.error(f"Error parsing message: {str(e)}")
            return "Coffee Chat Request", message_text
    
    def _get_fallback_message(self, person_data, is_scu_alumni):
        """Generate a fallback message if AI generation fails"""
        person_name = person_data.get('first_name', 'there')
        company_name = person_data.get('company', 'your company')
        
        if is_scu_alumni:
            subject = f"Coffee Chat Request - {person_name}"
            body = f"""Hello {person_name},

I hope this message finds you well. My name is Abhinav Ala, and I'm currently a Computer Science Engineering student at Santa Clara University. I came across your profile and was truly inspired by your path from SCU to your role at {company_name}.

{company_name} has been one of my top choices for internships because of its innovative approach and meaningful technology. I am especially interested in learning about your personal journey—how you transitioned from a fellow SCU student to where you are today. Your experience seems like a valuable source of insight as I prepare to apply for the 2026 Software Engineer Internship.

If you have some time, I would greatly appreciate the opportunity to hear your story and get any advice you might have for navigating the internship process and building a career at {company_name}.

Thank you so much for considering this request. I look forward to the possibility of hearing from you.

Best regards,
Abhinav Ala
(469)-381-4729
aala@scu.edu"""
        else:
            subject = f"Connecting with {person_name} - {company_name}"
            body = f"""Hello {person_name},

I hope this message finds you well. My name is Abhinav Ala, and I'm currently a Computer Science and Engineering student at Santa Clara University. I came across your profile and was really inspired by your career journey and the path that led you to {company_name}.

{company_name} has long been one of my top choices for internships because of its mission to inspire creativity and build meaningful technology. I'm especially interested in learning more about your own career journey—how you navigated different opportunities and what ultimately brought you to {company_name}. Your perspective would be invaluable as I prepare to apply for the 2026 Software Engineer Internship.

If you have some time, I'd greatly appreciate the chance to hear about your experiences and any advice you might have for someone aspiring to follow a similar path in tech.

Thank you so much for considering this request. I look forward to the possibility of connecting with you.

Best regards,
Abhinav Ala
(469)-381-4729
aala@scu.edu"""
        
        return {
            'subject': subject,
            'body': body,
            'is_scu_alumni': is_scu_alumni,
            'company_info': f"Information about {company_name}"
        }
    
    def generate_bulk_messages(self, people_data):
        """Generate personalized messages for multiple people"""
        results = []
        
        for person in people_data:
            try:
                message_data = self.generate_personalized_message(person)
                person_with_message = {
                    **person,
                    'message_subject': message_data['subject'],
                    'message_body': message_data['body'],
                    'is_scu_alumni': message_data['is_scu_alumni'],
                    'company_info': message_data['company_info']
                }
                results.append(person_with_message)
                
            except Exception as e:
                self.logger.error(f"Error generating message for {person.get('name', 'Unknown')}: {str(e)}")
                # Add person without message data
                results.append({
                    **person,
                    'message_subject': 'Coffee Chat Request',
                    'message_body': 'Message generation failed',
                    'is_scu_alumni': False,
                    'company_info': 'Not available'
                })
        
        return results