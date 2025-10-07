import logging
import time
from linkedin_scraper import LinkedInScraper
from email_finder import EmailFinder
from google_sheets_manager import GoogleSheetsManager
from gmass_integration import GMassIntegration
from ai_message_generator import AIMessageGenerator
from config import Config

class LinkedInOutreachWorkflow:
    def __init__(self):
        self.setup_logging()
        self.linkedin_scraper = LinkedInScraper()
        self.email_finder = EmailFinder()
        self.sheets_manager = GoogleSheetsManager()
        self.gmass_integration = GMassIntegration()
        self.ai_generator = AIMessageGenerator()
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def run_complete_workflow(self, companies, create_new_sheet=True, sheet_id=None):
        """Run the complete outreach workflow"""
        try:
            self.logger.info("Starting LinkedIn Outreach Workflow")
            
            # Step 1: Setup LinkedIn scraper and login
            self.logger.info("Step 1: Setting up LinkedIn scraper...")
            self.linkedin_scraper.setup_driver()
            
            if not self.linkedin_scraper.login_to_linkedin():
                self.logger.error("Failed to login to LinkedIn. Exiting workflow.")
                return False
            
            # Step 2: Setup Google Sheets
            self.logger.info("Step 2: Setting up Google Sheets...")
            if create_new_sheet:
                sheet_id = self.sheets_manager.create_sheet_with_headers("LinkedIn Outreach Leads")
                if not sheet_id:
                    self.logger.error("Failed to create Google Sheet. Exiting workflow.")
                    return False
            else:
                if not self.sheets_manager.connect_to_sheet(sheet_id):
                    self.logger.error("Failed to connect to Google Sheet. Exiting workflow.")
                    return False
            
            # Step 3: Process each company
            all_people_data = []
            
            for company in companies:
                self.logger.info(f"Processing company: {company}")
                
                # Search for people at the company
                people_data = self.linkedin_scraper.search_people_by_company(company)
                
                if people_data:
                    # Find emails for the people
                    people_with_emails = self.email_finder.find_emails_for_people(people_data)
                    
                    # Generate personalized messages
                    people_with_messages = self.ai_generator.generate_bulk_messages(people_with_emails)
                    
                    all_people_data.extend(people_with_messages)
                    
                    # Add to Google Sheets
                    self.sheets_manager.add_people_data(people_with_messages)
                    
                    self.logger.info(f"Processed {len(people_with_messages)} people from {company}")
                else:
                    self.logger.warning(f"No people found for company: {company}")
                
                # Add delay between companies to avoid rate limiting
                time.sleep(5)
            
            # Step 4: Create GMass campaigns
            self.logger.info("Step 4: Creating GMass campaigns...")
            self._create_gmass_campaigns(all_people_data)
            
            # Step 5: Generate summary report
            self._generate_summary_report(all_people_data)
            
            self.logger.info("Workflow completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in workflow: {str(e)}")
            return False
        finally:
            # Cleanup
            self.linkedin_scraper.close()
    
    def _create_gmass_campaigns(self, people_data):
        """Create GMass campaigns for different groups of people"""
        try:
            # Separate SCU alumni and non-alumni
            scu_alumni = [p for p in people_data if p.get('is_scu_alumni', False) and p.get('email')]
            non_alumni = [p for p in people_data if not p.get('is_scu_alumni', False) and p.get('email')]
            
            # Create campaign for SCU alumni
            if scu_alumni:
                campaign_name = "SCU Alumni Outreach Campaign"
                subject = "Coffee Chat Request - SCU Connection"
                
                # Use the first person's message as template (they should all be similar)
                body = scu_alumni[0].get('message_body', '') if scu_alumni else ''
                
                result = self.gmass_integration.create_campaign(
                    campaign_name, subject, body, scu_alumni
                )
                
                if result:
                    self.logger.info(f"Created SCU alumni campaign: {result.get('campaign_id')}")
            
            # Create campaign for non-alumni
            if non_alumni:
                campaign_name = "Professional Networking Campaign"
                subject = "Connecting - Professional Networking"
                
                # Use the first person's message as template
                body = non_alumni[0].get('message_body', '') if non_alumni else ''
                
                result = self.gmass_integration.create_campaign(
                    campaign_name, subject, body, non_alumni
                )
                
                if result:
                    self.logger.info(f"Created non-alumni campaign: {result.get('campaign_id')}")
                    
        except Exception as e:
            self.logger.error(f"Error creating GMass campaigns: {str(e)}")
    
    def _generate_summary_report(self, people_data):
        """Generate a summary report of the workflow results"""
        try:
            total_people = len(people_data)
            people_with_emails = len([p for p in people_data if p.get('email')])
            scu_alumni = len([p for p in people_data if p.get('is_scu_alumni', False)])
            
            companies = list(set([p.get('company', 'Unknown') for p in people_data]))
            
            report = f"""
            LinkedIn Outreach Workflow Summary
            ===================================
            
            Total People Found: {total_people}
            People with Emails: {people_with_emails}
            SCU Alumni: {scu_alumni}
            Non-Alumni: {total_people - scu_alumni}
            
            Companies Processed: {len(companies)}
            {', '.join(companies)}
            
            Google Sheet URL: {self.sheets_manager.get_sheet_url()}
            
            Next Steps:
            1. Review the Google Sheet for accuracy
            2. Test the GMass campaigns with a small group
            3. Schedule the campaigns for optimal send times
            4. Track responses and follow up accordingly
            """
            
            self.logger.info(report)
            
            # Save report to file
            with open('workflow_summary.txt', 'w') as f:
                f.write(report)
                
        except Exception as e:
            self.logger.error(f"Error generating summary report: {str(e)}")
    
    def run_company_specific_workflow(self, company_name, max_people=50):
        """Run workflow for a single company"""
        try:
            self.logger.info(f"Running workflow for company: {company_name}")
            
            # Setup LinkedIn scraper
            self.linkedin_scraper.setup_driver()
            
            if not self.linkedin_scraper.login_to_linkedin():
                return False
            
            # Search for people
            people_data = self.linkedin_scraper.search_people_by_company(company_name)
            
            if not people_data:
                self.logger.warning(f"No people found for {company_name}")
                return False
            
            # Limit to max_people
            people_data = people_data[:max_people]
            
            # Find emails
            people_with_emails = self.email_finder.find_emails_for_people(people_data)
            
            # Generate messages
            people_with_messages = self.ai_generator.generate_bulk_messages(people_with_emails)
            
            return people_with_messages
            
        except Exception as e:
            self.logger.error(f"Error in company-specific workflow: {str(e)}")
            return None
        finally:
            self.linkedin_scraper.close()

def main():
    """Main function to run the workflow"""
    # Example usage
    companies = [
        "TikTok",
        "Pinterest", 
        "Google",
        "Meta",
        "Apple"
    ]
    
    workflow = LinkedInOutreachWorkflow()
    
    # Run the complete workflow
    success = workflow.run_complete_workflow(companies, create_new_sheet=True)
    
    if success:
        print("Workflow completed successfully!")
    else:
        print("Workflow failed. Check logs for details.")

if __name__ == "__main__":
    main()