#!/usr/bin/env python3
"""
Example usage of the LinkedIn Outreach Platform
"""

import os
from main_workflow import LinkedInOutreachWorkflow

def main():
    # Set up environment variables (in production, use .env file)
    os.environ['LINKEDIN_EMAIL'] = 'your_email@example.com'
    os.environ['LINKEDIN_PASSWORD'] = 'your_password'
    os.environ['HUNTER_API_KEY'] = 'your_hunter_api_key'
    os.environ['OPENAI_API_KEY'] = 'your_openai_api_key'
    os.environ['GMASS_API_KEY'] = 'your_gmass_api_key'
    os.environ['MAX_PEOPLE_PER_COMPANY'] = '20'
    os.environ['SEARCH_KEYWORDS'] = 'software engineer,data scientist,product manager'
    
    # Define target companies
    companies = [
        "TikTok",
        "Pinterest", 
        "Google",
        "Meta",
        "Apple",
        "Microsoft",
        "Amazon",
        "Netflix"
    ]
    
    print("🚀 Starting LinkedIn Outreach Platform")
    print(f"Target companies: {', '.join(companies)}")
    
    # Initialize workflow
    workflow = LinkedInOutreachWorkflow()
    
    # Run the complete workflow
    success = workflow.run_complete_workflow(
        companies=companies,
        create_new_sheet=True  # Creates a new Google Sheet
    )
    
    if success:
        print("✅ Workflow completed successfully!")
        print("Check your Google Sheet for the results.")
    else:
        print("❌ Workflow failed. Check the logs for details.")

def run_single_company_example():
    """Example of running workflow for a single company"""
    print("🏢 Running single company example...")
    
    # Set up environment variables
    os.environ['LINKEDIN_EMAIL'] = 'your_email@example.com'
    os.environ['LINKEDIN_PASSWORD'] = 'your_password'
    os.environ['HUNTER_API_KEY'] = 'your_hunter_api_key'
    os.environ['OPENAI_API_KEY'] = 'your_openai_api_key'
    
    workflow = LinkedInOutreachWorkflow()
    
    # Run for a single company
    people_data = workflow.run_company_specific_workflow(
        company_name="TikTok",
        max_people=10
    )
    
    if people_data:
        print(f"✅ Found {len(people_data)} people at TikTok")
        
        # Display results
        for person in people_data[:3]:  # Show first 3
            print(f"\nName: {person.get('name', 'N/A')}")
            print(f"Title: {person.get('title', 'N/A')}")
            print(f"Company: {person.get('company', 'N/A')}")
            print(f"Email: {person.get('email', 'N/A')}")
            print(f"SCU Alumni: {person.get('is_scu_alumni', False)}")
            print("-" * 50)
    else:
        print("❌ No people found or error occurred")

if __name__ == "__main__":
    # Choose which example to run
    print("Choose an example:")
    print("1. Complete workflow for multiple companies")
    print("2. Single company example")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        main()
    elif choice == "2":
        run_single_company_example()
    else:
        print("Invalid choice. Running complete workflow...")
        main()