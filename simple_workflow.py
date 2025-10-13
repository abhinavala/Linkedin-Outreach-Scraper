import logging
import time
from linkedin_scraper import LinkedInScraper
from google_sheets_manager import GoogleSheetsManager
from csv_manager import CSVManager
from config import Config

class SimpleLinkedInWorkflow:
    def __init__(self):
        self.setup_logging()
        self.linkedin_scraper = LinkedInScraper()
        self.sheets_manager = GoogleSheetsManager()
        self.csv_manager = CSVManager()
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def run_workflow(self, companies, create_new_sheet=True, sheet_id=None):
        """Run the simplified LinkedIn scraping workflow"""
        try:
            self.logger.info("Starting Simple LinkedIn Workflow")
            
            # Step 1: Setup LinkedIn scraper and login
            self.logger.info("Step 1: Setting up LinkedIn scraper...")
            self.linkedin_scraper.setup_driver()
            
            if not self.linkedin_scraper.login_to_linkedin():
                self.logger.error("Failed to login to LinkedIn. Exiting workflow.")
                return False
            
            # Step 2: Setup Google Sheets
            self.logger.info("Step 2: Setting up Google Sheets...")
            if create_new_sheet:
                sheet_id = self.sheets_manager.create_sheet_with_headers("LinkedIn Contacts")
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
                    all_people_data.extend(people_data)
                    
                    # Add to Google Sheets
                    self.sheets_manager.add_people_data(people_data)
                    
                    self.logger.info(f"Processed {len(people_data)} people from {company}")
                else:
                    self.logger.warning(f"No people found for company: {company}")
                
                # Add delay between companies to avoid rate limiting
                time.sleep(5)
            
            # Step 4: Generate summary report
            self._generate_summary_report(all_people_data, sheet_id)
            
            self.logger.info("Workflow completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Error in workflow: {str(e)}")
            return False
        finally:
            # Cleanup
            self.linkedin_scraper.close()
    
    def _generate_summary_report(self, people_data, sheet_id):
        """Generate a summary report of the workflow results"""
        try:
            total_people = len(people_data)
            scu_alumni = len([p for p in people_data if p.get('is_scu_alumni', False)])
            
            companies = list(set([p.get('company', 'Unknown') for p in people_data]))
            
            report = f"""
            LinkedIn Scraping Workflow Summary
            ===================================
            
            Total People Found: {total_people}
            SCU Alumni: {scu_alumni}
            Non-Alumni: {total_people - scu_alumni}
            
            Companies Processed: {len(companies)}
            {', '.join(companies)}
            
            Google Sheet ID: {sheet_id}
            Google Sheet URL: {self.sheets_manager.get_sheet_url()}
            
            Next Steps:
            1. Review the Google Sheet for accuracy
            2. Manually add email addresses in the Email column
            3. Use the data for your outreach campaigns
            4. Track responses and follow up accordingly
            """
            
            self.logger.info(report)
            
            # Save report to file
            with open('workflow_summary.txt', 'w') as f:
                f.write(report)
                
        except Exception as e:
            self.logger.error(f"Error generating summary report: {str(e)}")
    
    def run_single_company(self, company_name, max_people=50):
        """Run workflow for a single company"""
        try:
            self.logger.info(f"Running workflow for company: {company_name}")
            
            # Setup LinkedIn scraper
            self.linkedin_scraper.setup_driver()
            
            if not self.linkedin_scraper.login_to_linkedin():
                return None
            
            # Search for people
            people_data = self.linkedin_scraper.search_people_by_company(company_name)
            
            if not people_data:
                self.logger.warning(f"No people found for {company_name}")
                return None
            
            # Limit to max_people
            people_data = people_data[:max_people]
            
            return people_data
            
        except Exception as e:
            self.logger.error(f"Error in single company workflow: {str(e)}")
            return None
        finally:
            self.linkedin_scraper.close()
    
    def run_csv_workflow(self, companies, filename=None):
        """Run the workflow and export to CSV instead of Google Sheets"""
        all_people_data = []  # Initialize outside try block to avoid UnboundLocalError
        
        try:
            self.logger.info("Starting CSV Export LinkedIn Workflow")
            
            # Step 1: Setup LinkedIn scraper and login
            self.logger.info("Step 1: Setting up LinkedIn scraper...")
            self.linkedin_scraper.setup_driver()
            
            if not self.linkedin_scraper.login_to_linkedin():
                self.logger.error("Failed to login to LinkedIn. Exiting workflow.")
                return {'success': False, 'error': 'LinkedIn login failed'}
            
            # Step 2: Process each company and collect data using the alumni hiring workflow
            
            for company in companies:
                self.logger.info(f"Processing company: {company}")
                
                try:
                    # Use the new alumni-specific search method
                    # This will look for "X people from your company were hired here" and click it
                    people_data = self.linkedin_scraper.search_company_alumni(company)
                    
                    if people_data:
                        all_people_data.extend(people_data)
                        self.logger.info(f"Processed {len(people_data)} SCU alumni from {company}")
                    else:
                        self.logger.warning(f"No SCU alumni found for company: {company}")
                        
                        # Fallback: try generic search if alumni search fails
                        self.logger.info(f"Trying fallback generic search for {company}")
                        try:
                            fallback_data = self.linkedin_scraper.search_people_by_company(company)
                            if fallback_data:
                                # Mark fallback data as SCU alumni too since we're looking for SCU alumni
                                for person in fallback_data:
                                    person['is_scu_alumni'] = True
                                    person['company'] = company
                                all_people_data.extend(fallback_data)
                                self.logger.info(f"Fallback found {len(fallback_data)} people from {company}")
                            else:
                                self.logger.warning(f"No results found for {company}, skipping...")
                        except Exception as fallback_error:
                            self.logger.error(f"Fallback search failed for {company}: {str(fallback_error)}")
                            self.logger.info(f"Skipping {company} and moving to next company...")
                
                except Exception as e:
                    self.logger.error(f"Error processing {company}: {str(e)}")
                    self.logger.info(f"Skipping {company} and moving to next company...")
                
                # Add delay between companies to avoid rate limiting
                time.sleep(5)
            
            # Step 3: Export to CSV
            if all_people_data:
                self.logger.info(f"Exporting {len(all_people_data)} contacts to CSV...")
                export_result = self.csv_manager.export_contacts(all_people_data, filename)
                
                if export_result['success']:
                    self.logger.info(f"Successfully exported to {export_result['filename']}")
                    return {
                        'success': True,
                        'filename': export_result['filename'],
                        'filepath': export_result['filepath'],
                        'contact_count': export_result['contact_count'],
                        'data': all_people_data
                    }
                else:
                    return {
                        'success': False,
                        'error': f"CSV export failed: {export_result['error']}"
                    }
            else:
                return {
                    'success': False,
                    'error': 'No contacts found to export'
                }
                
        except Exception as e:
            self.logger.error(f"Error in CSV workflow: {str(e)}")
            return {'success': False, 'error': str(e)}
        finally:
            # Cleanup
            self.linkedin_scraper.close()

def main():
    """Main function to run the simplified workflow"""
    # Example usage
    companies = [
        "TikTok",
        "Pinterest", 
        "Google",
        "Meta",
        "Apple"
    ]
    
    workflow = SimpleLinkedInWorkflow()
    
    # Run the workflow
    success = workflow.run_workflow(companies, create_new_sheet=True)
    
    if success:
        print("Workflow completed successfully!")
        print("Check your Google Sheet for the results.")
    else:
        print("Workflow failed. Check logs for details.")

if __name__ == "__main__":
    main()