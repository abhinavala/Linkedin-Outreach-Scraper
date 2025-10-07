import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import logging
from config import Config

class LinkedInScraper:
    def __init__(self):
        self.driver = None
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        # Enable debug logging for title extraction
        self.logger.setLevel(logging.DEBUG)
        
    def setup_driver(self):
        """Setup Chrome driver with appropriate options"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
            # Try using chromedriver-autoinstaller first
            try:
                import chromedriver_autoinstaller
                chromedriver_autoinstaller.install()
                self.driver = webdriver.Chrome(options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                self.logger.info("Using chromedriver-autoinstaller")
                return
            except Exception as e:
                self.logger.warning(f"ChromeDriver autoinstaller failed: {str(e)}")
            
            # Try using system-installed chromedriver
            try:
                import shutil
                chromedriver_path = shutil.which("chromedriver")
                if chromedriver_path:
                    service = Service(chromedriver_path)
                    self.driver = webdriver.Chrome(service=service, options=chrome_options)
                    self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    self.logger.info("Using system-installed Chrome driver")
                    return
            except Exception as e:
                self.logger.warning(f"System Chrome driver failed: {str(e)}")
            
            # Fallback to webdriver-manager
            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                self.logger.info("Using webdriver-manager Chrome driver")
                
            except Exception as e2:
                self.logger.error(f"Webdriver-manager failed: {str(e2)}")
                raise Exception("Could not setup Chrome driver. Please ensure Chrome and ChromeDriver are installed.")
                
        except Exception as e:
            self.logger.error(f"Error setting up Chrome driver: {str(e)}")
            raise Exception("Could not setup Chrome driver. Please ensure Chrome is installed and try again.")
    
    def login_to_linkedin(self):
        """Login to LinkedIn - Manual login required"""
        try:
            self.logger.info("Opening LinkedIn login page...")
            self.driver.get(Config.LINKEDIN_BASE_URL + "/login")
            
            # Wait for login form to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            
            self.logger.info("Please manually log into LinkedIn in the browser window that opened.")
            self.logger.info("Once logged in, the scraper will continue automatically...")
            
            # Wait for user to manually log in
            # Check for successful login by looking for the global navigation
            max_wait_time = 300  # 5 minutes
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                try:
                    # Check if we're on the main LinkedIn page (logged in)
                    if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url or "jobs" in self.driver.current_url:
                        self.logger.info("Successfully logged into LinkedIn!")
                        return True
                    
                    # Also check for global nav element
                    try:
                        WebDriverWait(self.driver, 2).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "global-nav"))
                        )
                        self.logger.info("Successfully logged into LinkedIn!")
                        return True
                    except:
                        pass
                    
                    time.sleep(2)  # Check every 2 seconds
                    
                except Exception as e:
                    time.sleep(2)
                    continue
            
            self.logger.error("Login timeout - please try again")
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to open LinkedIn login page: {str(e)}")
            return False
    
    def search_people_by_company(self, company_name, keywords=None):
        """Search for people at a specific company"""
        try:
            self.logger.info(f"Searching for people at {company_name}")
            
            # Use simpler search approach - search by company name first
            search_url = f"{Config.LINKEDIN_SEARCH_URL}?keywords={company_name}"
            
            self.logger.info(f"Navigating to: {search_url}")
            self.driver.get(search_url)
            time.sleep(random.uniform(3, 5))
            
            # Wait for page to load and look for people results
            try:
                # Wait for any search results to appear with multiple fallbacks
                WebDriverWait(self.driver, 15).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CLASS_NAME, "search-results-container")),
                        EC.presence_of_element_located((By.CLASS_NAME, "search-results")),
                        EC.presence_of_element_located((By.CLASS_NAME, "reusable-search__result-container")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-id='search-results']")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".search-results-container")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".reusable-search__result-container")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "main")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[role='main']"))
                    )
                )
                
                # Additional wait for content to load
                time.sleep(3)
                
                # Check if we're on the right page
                current_url = self.driver.current_url
                self.logger.info(f"Current URL after search: {current_url}")
                
                # If we're not on a search results page, try to navigate properly
                if "search/results/people" not in current_url:
                    self.logger.warning("Not on people search page, trying to navigate properly")
                    # Try to click on "People" tab if it exists
                    try:
                        people_tab = self.driver.find_element(By.XPATH, "//button[contains(text(), 'People')]")
                        people_tab.click()
                        time.sleep(3)
                    except:
                        pass
                        
            except Exception as e:
                self.logger.warning(f"No search results found for {company_name}: {str(e)}")
                return []
            
            # Scroll to load more results
            self._scroll_to_load_more()
            
            # Parse search results
            people_data = self._parse_search_results()
            
            # Add company name and check for SCU alumni status
            for person in people_data:
                person['company'] = company_name
                person['is_scu_alumni'] = self._check_scu_alumni(person)
            
            self.logger.info(f"Found {len(people_data)} people at {company_name}")
            return people_data
            
        except Exception as e:
            self.logger.error(f"Error searching for people at {company_name}: {str(e)}")
            return []
    
    def _scroll_to_load_more(self):
        """Scroll down to load more search results"""
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load
            time.sleep(random.uniform(2, 4))
            
            # Calculate new scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                break
                
            last_height = new_height
    
    def _parse_search_results(self):
        """Parse LinkedIn search results to extract people information"""
        people_data = []
        
        try:
            # Get page source and parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Try multiple selectors for people cards
            people_cards = []
            
            # Try different selectors for LinkedIn's current structure (2024)
            selectors = [
                'li.reusable-search__result-container',
                'div.reusable-search__result-container',
                'li[data-test-id="search-result"]',
                'div[data-test-id="search-result"]',
                'li.search-results-container li',
                'div.search-results-container li',
                'div.entity-result__item',
                'li.entity-result__item',
                'div[data-test-id="search-results"] li',
                'div[data-test-id="search-results"] div',
                '.search-results-container .reusable-search__result-container',
                '.search-results-container .entity-result__item'
            ]
            
            for selector in selectors:
                cards = soup.select(selector)
                if cards:
                    people_cards = cards
                    self.logger.info(f"Found {len(cards)} people cards using selector: {selector}")
                    break
            
            if not people_cards:
                self.logger.warning("No people cards found with any selector")
                # Debug: Save page source to see what LinkedIn is actually showing
                try:
                    with open('linkedin_debug.html', 'w', encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                    self.logger.info("Saved page source to linkedin_debug.html for debugging")
                except:
                    pass
                return []
            
            for card in people_cards[:Config.MAX_PEOPLE_PER_COMPANY]:
                try:
                    person_data = self._extract_person_data(card)
                    if person_data:
                        people_data.append(person_data)
                except Exception as e:
                    self.logger.warning(f"Error parsing person card: {str(e)}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"Error parsing search results: {str(e)}")
            
        return people_data
    
    def _extract_person_data(self, card):
        """Extract person data from a single card"""
        try:
            person_data = {}
            
            # Debug: Log card structure for first few cards
            if not hasattr(self, '_debug_count'):
                self._debug_count = 0
            if self._debug_count < 3:
                self.logger.debug(f"Card HTML (first 800 chars): {str(card)[:800]}")
                self._debug_count += 1
            
            # Extract name - try multiple selectors for current LinkedIn (including obfuscated classes)
            name_selectors = [
                'a[data-test-id="search-result__profile-name"]',
                'a.app-aware-link',
                'a[href*="/in/"]',
                'a.entity-result__title-text',
                'span.entity-result__title-text a',
                'a[href*="linkedin.com/in/"]',
                '.reusable-search__result-container a[href*="/in/"]',
                'a[data-control-name="search_srp_result"]',
                # New obfuscated class selectors based on debug output
                'a[data-test-app-aware-link]',
                'a[class*="TAkGWjHhmVmkmMDJGaNOrxvCVcOPkgho"]',
                'a[class*="scale-down"]',
                'a[href*="miniProfileUrn"]',
                # More specific selectors for current LinkedIn structure
                'span[class*="AzxytMuSGtChzWbrEEuKWgMtBymQ"] a',
                'span[class*="AzxytMuSGtChzWbrEEuKWgMtBymQ"]',
                'div[class*="display-flex"] a[href*="/in/"]',
                'span[dir="ltr"] span[aria-hidden="true"]'
            ]
            
            for selector in name_selectors:
                name_element = card.select_one(selector)
                if name_element:
                    name_text = name_element.get_text(strip=True)
                    if name_text and name_text not in ['', ' ', 'Status is offline']:
                        # Clean up the name text - remove "View [Name]'s profile" suffix
                        if "View" in name_text and "'s profile" in name_text:
                            name_text = name_text.split("View")[0].strip()
                        
                        # Skip if it looks like status text or connection info
                        if any(skip in name_text.lower() for skip in ['status', 'offline', 'online', 'degree connection', 'mutual connection', 'verified member', 'has verifications']):
                            continue
                            
                        # Only use if it looks like a real name (2-50 chars, not too many numbers/special chars)
                        if (2 <= len(name_text) <= 50 and 
                            not name_text.isdigit() and 
                            not any(char in name_text for char in ['•', '|', '@', '#', '$', '%', '^', '&', '*']) and
                            name_text.count(' ') <= 4):  # Most names have 1-4 spaces max
                            
                            person_data['name'] = name_text
                            href = name_element.get('href', '')
                            if href and not href.startswith('http'):
                                href = f"{Config.LINKEDIN_BASE_URL}{href}"
                            person_data['profile_url'] = href
                            self.logger.debug(f"Found name with selector '{selector}': {name_text}")
                            break
            
            # Extract title/position - try multiple selectors for current LinkedIn (including obfuscated classes)
            title_selectors = [
                'div[data-test-id="search-result__subtitle"]',
                'div.entity-result__primary-subtitle',
                'p.entity-result__primary-subtitle',
                'span.entity-result__primary-subtitle',
                '.search-results-container .entity-result__primary-subtitle',
                '.reusable-search__result-container .entity-result__primary-subtitle',
                'div[data-test-id="search-result__subtitle"]',
                'p[data-test-id="search-result__subtitle"]',
                'span[data-test-id="search-result__subtitle"]',
                '.entity-result__summary-info .entity-result__primary-subtitle',
                '.reusable-search__result-container p',
                '.reusable-search__result-container div',
                # New obfuscated class selectors - look for text elements near the name
                'div[class*="YsVvmMjCAfogaNEnItpvFjIuQeSlkCSdOE"] p',
                'div[class*="YsVvmMjCAfogaNEnItpvFjIuQeSlkCSdOE"] span',
                'div[class*="YsVvmMjCAfogaNEnItpvFjIuQeSlkCSdOE"] div',
                'div[class*="MogfbxfXFPhiMvLCYiWhJSyKHPHnkkAoWjes"] p',
                'div[class*="MogfbxfXFPhiMvLCYiWhJSyKHPHnkkAoWjes"] span',
                'div[class*="MogfbxfXFPhiMvLCYiWhJSyKHPHnkkAoWjes"] div'
            ]
            
            for selector in title_selectors:
                title_element = card.select_one(selector)
                if title_element:
                    title_text = title_element.get_text(strip=True)
                    if title_text and title_text not in ['', ' ', 'Status is offline']:
                        person_data['title'] = title_text
                        self.logger.debug(f"Found title with selector '{selector}': {title_text}")
                        break
            
            # Extract company - try multiple selectors (including obfuscated classes)
            company_selectors = [
                'div[data-test-id="search-result__secondary-subtitle"]',
                'div.entity-result__secondary-subtitle',
                'p.entity-result__secondary-subtitle',
                'span.entity-result__secondary-subtitle',
                # New obfuscated class selectors
                'div[class*="YsVvmMjCAfogaNEnItpvFjIuQeSlkCSdOE"] div[class*="secondary"]',
                'div[class*="MogfbxfXFPhiMvLCYiWhJSyKHPHnkkAoWjes"] div[class*="secondary"]'
            ]
            
            for selector in company_selectors:
                company_element = card.select_one(selector)
                if company_element:
                    person_data['company'] = company_element.get_text(strip=True)
                    break
            
            # Extract location - try multiple selectors
            location_selectors = [
                'div[data-test-id="search-result__summary-info"]',
                'div.entity-result__summary-info',
                'p.entity-result__summary-info',
                'span.entity-result__summary-info'
            ]
            
            for selector in location_selectors:
                location_element = card.select_one(selector)
                if location_element:
                    person_data['location'] = location_element.get_text(strip=True)
                    break
            
            # If we still don't have a title, try a more comprehensive approach
            if not person_data.get('title'):
                # Look for any text that might be a job title in the card
                card_text = card.get_text(strip=True)
                lines = [line.strip() for line in card_text.split('\n') if line.strip()]
                
                # Skip the name (first line) and look for job-related text
                for i, line in enumerate(lines[1:], 1):
                    # Skip common non-job text
                    if line.lower() in ['connect', 'message', 'follow', 'status is offline', 'more', 'view profile']:
                        continue
                    # If the line looks like a job title (not too long, contains common job words)
                    if (len(line) < 100 and len(line) > 3 and
                        any(word in line.lower() for word in ['engineer', 'manager', 'director', 'analyst', 'developer', 'designer', 'consultant', 'specialist', 'coordinator', 'lead', 'architect', 'consultant', 'executive', 'president', 'ceo', 'cto', 'cfo', 'vp', 'senior', 'principal', 'head', 'chief', 'officer', 'founder', 'co-founder', 'product', 'sales', 'marketing', 'hr', 'operations', 'strategy', 'business', 'data', 'software', 'technical', 'research', 'innovation', 'growth', 'partnership', 'customer', 'client', 'account', 'project', 'program', 'team', 'department'])):
                        person_data['title'] = line
                        self.logger.debug(f"Found title through text analysis: {line}")
                        break
                
                # If still no title, try to find any text that looks like a professional role
                if not person_data.get('title'):
                    for line in lines[1:]:
                        if (len(line) > 5 and len(line) < 80 and 
                            not any(skip in line.lower() for skip in ['connect', 'message', 'follow', 'status', 'offline', 'more', 'view', 'profile', 'linkedin', 'atlassian', 'google', 'microsoft', 'amazon', 'facebook', 'apple']) and
                            any(char in line for char in ['@', '•', '|', 'at ', ' - ', '–', '—'])):
                            person_data['title'] = line
                            self.logger.debug(f"Found title through pattern matching: {line}")
                            break
            
            # If we still don't have a name, try to extract from the card text
            if not person_data.get('name'):
                card_text = card.get_text(strip=True)
                lines = [line.strip() for line in card_text.split('\n') if line.strip()]
                
                # Look for the first line that looks like a name (not too long, not a job title)
                for line in lines:
                    if (len(line) > 2 and len(line) < 50 and 
                        not any(word in line.lower() for word in ['current:', 'past:', 'summary:', 'skills:', 'connect', 'message', 'follow', 'status', 'offline', 'online', 'more', 'view', 'profile', 'linkedin', 'engineer', 'manager', 'director', 'analyst', 'developer', 'designer', 'consultant', 'specialist', 'coordinator', 'lead', 'architect', 'executive', 'president', 'ceo', 'cto', 'cfo', 'vp', 'senior', 'principal', 'head', 'chief', 'officer', 'founder', 'co-founder', 'product', 'sales', 'marketing', 'hr', 'operations', 'strategy', 'business', 'data', 'software', 'technical', 'research', 'innovation', 'growth', 'partnership', 'customer', 'client', 'account', 'project', 'program', 'team', 'department', 'at ', ' - ', '–', '—', '@', '•', '|', 'degree connection', 'mutual connection', 'verified member', 'has verifications']) and
                        not line.isdigit() and 
                        not any(char in line for char in ['•', '|', '@', '#', '$', '%', '^', '&', '*']) and
                        line.count(' ') <= 4):
                        person_data['name'] = line
                        self.logger.debug(f"Found name through text analysis: {line}")
                        break
                
                # If still no name, try to extract from the first meaningful line
                if not person_data.get('name'):
                    for line in lines:
                        if (len(line) > 1 and len(line) < 100 and 
                            not any(skip in line.lower() for skip in ['current:', 'past:', 'summary:', 'skills:', 'connect', 'message', 'follow', 'status', 'offline', 'online', 'more', 'view', 'profile', 'linkedin', '•', '2nd', 'degree', 'connection', 'mutual', 'verified', 'member', 'has', 'verifications', 'engineer', 'manager', 'director', 'analyst', 'developer', 'designer', 'consultant', 'specialist', 'coordinator', 'lead', 'architect', 'executive', 'president', 'ceo', 'cto', 'cfo', 'vp', 'senior', 'principal', 'head', 'chief', 'officer', 'founder', 'co-founder', 'product', 'sales', 'marketing', 'hr', 'operations', 'strategy', 'business', 'data', 'software', 'technical', 'research', 'innovation', 'growth', 'partnership', 'customer', 'client', 'account', 'project', 'program', 'team', 'department']) and
                            not line.isdigit() and 
                            not any(char in line for char in ['•', '|', '@', '#', '$', '%', '^', '&', '*']) and
                            line.count(' ') <= 6):
                            person_data['name'] = line
                            self.logger.debug(f"Found name through fallback analysis: {line}")
                            break
            
            # Only return if we have essential data
            if person_data.get('name'):
                # Check if this person is an SCU alumni
                person_data['is_scu_alumni'] = self._check_scu_alumni(person_data)
                return person_data
                
        except Exception as e:
            self.logger.warning(f"Error extracting person data: {str(e)}")
            
        return None
    
    def _check_scu_alumni(self, person_data):
        """Check if the person is an SCU alumni based on their profile data"""
        try:
            # Look for SCU-related keywords in title, company, or location
            scu_keywords = [
                'santa clara university', 'scu', 'santa clara', 
                'bronco', 'broncos', 'santa clara university',
                'scu broncos', 'scu alumni', 'santa clara broncos'
            ]
            
            profile_text = ' '.join([
                person_data.get('title', ''),
                person_data.get('company', ''),
                person_data.get('location', ''),
                person_data.get('name', '')
            ]).lower()
            
            for keyword in scu_keywords:
                if keyword in profile_text:
                    self.logger.debug(f"Found SCU alumni: {person_data.get('name')} - matched keyword: {keyword}")
                    return True
                    
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking SCU alumni status: {str(e)}")
            return False
    
    def search_scu_alumni(self):
        """Search specifically for SCU alumni/current students/faculty"""
        try:
            self.logger.info("Searching for SCU alumni/faculty/students...")
            
            # Search for people at Santa Clara University
            scu_search_url = f"{Config.LINKEDIN_BASE_URL}/search/results/people/?keywords=Santa Clara University"
            self.driver.get(scu_search_url)
            
            # Wait for results
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-results-container"))
            )
            
            # Parse results
            people_data = self._parse_search_results()
            
            # Mark all as SCU alumni since they're from SCU search
            for person in people_data:
                person['is_scu_alumni'] = True
                person['company'] = 'Santa Clara University'  # Ensure company is set to SCU
            
            self.logger.info(f"Found {len(people_data)} SCU alumni/faculty/students")
            return people_data
            
        except Exception as e:
            self.logger.error(f"Error searching SCU alumni: {str(e)}")
            return []
    
    def search_company_alumni(self, company_name):
        """Search for company, then click 'X people from your company were hired here' link directly from search results"""
        try:
            self.logger.info(f"Searching for SCU alumni at {company_name}...")
            
            # Step 1: Use the main LinkedIn search bar (not people tab)
            search_url = f"{Config.LINKEDIN_BASE_URL}/search/results/all/?keywords={company_name}"
            self.logger.info(f"Searching for company in main search: {company_name}")
            self.driver.get(search_url)
            
            # Wait for search results to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-results-container"))
            )
            
            # Step 2: Look for the "X people from your company were hired here" link directly in search results
            self.logger.info("Looking for alumni hiring link directly in search results...")
            
            # Find all elements that might contain the alumni hiring link
            alumni_link = None
            
            # Approach 1: Look for text containing "hired here" anywhere on the page
            try:
                elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'hired here')]")
                self.logger.info(f"Found {len(elements)} elements with 'hired here' text")
                
                for element in elements:
                    try:
                        element_text = element.text
                        self.logger.info(f"Element text: {element_text}")
                        
                        # Check if it contains the alumni hiring text
                        if "people from your company were hired here" in element_text or "people from your school were hired here" in element_text:
                            # Try to find a clickable parent or the element itself
                            if element.tag_name == 'a':
                                alumni_link = element
                                break
                            else:
                                # Look for parent link
                                try:
                                    parent_link = element.find_element(By.XPATH, "./ancestor::a")
                                    if parent_link:
                                        alumni_link = parent_link
                                        break
                                except:
                                    # Try clicking the element itself if it's clickable
                                    if element.is_enabled() and element.is_displayed():
                                        alumni_link = element
                                        break
                    except Exception as e:
                        continue
            except Exception as e:
                self.logger.warning(f"Error searching for alumni link: {str(e)}")
            
            # Approach 2: Look for links with specific patterns in the search results
            if not alumni_link:
                try:
                    # Look for links that might be the alumni hiring link
                    link_patterns = [
                        "a[href*='people'][href*='hired']",
                        "a[href*='search/results/people'][href*='company']",
                        "a[href*='company'][href*='people']",
                        "a:contains('people from your company were hired here')",
                        "a:contains('hired here')"
                    ]
                    
                    for pattern in link_patterns:
                        try:
                            if ':contains(' in pattern:
                                # Use XPath for text-based search
                                xpath = f"//a[contains(text(), 'people from your company were hired here')] | //a[contains(text(), 'hired here')]"
                                elements = self.driver.find_elements(By.XPATH, xpath)
                            else:
                                elements = self.driver.find_elements(By.CSS_SELECTOR, pattern)
                            
                            if elements:
                                for element in elements:
                                    element_text = element.text.lower()
                                    if "hired" in element_text and "people" in element_text:
                                        alumni_link = element
                                        break
                            if alumni_link:
                                break
                        except Exception as e:
                            continue
                except Exception as e:
                    self.logger.warning(f"Error with link patterns: {str(e)}")
            
            # Approach 3: Look for any clickable element containing the text
            if not alumni_link:
                try:
                    # Search for any clickable element with the hiring text
                    clickable_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'people from your company were hired here')]")
                    for element in clickable_elements:
                        if element.is_enabled() and element.is_displayed():
                            alumni_link = element
                            break
                except Exception as e:
                    self.logger.warning(f"Error with clickable elements: {str(e)}")
            
            if alumni_link:
                self.logger.info(f"Found alumni hiring link for {company_name}: {alumni_link.text}")
                
                # Step 3: Click the alumni hiring link directly from search results
                self.driver.execute_script("arguments[0].scrollIntoView(true);", alumni_link)
                time.sleep(2)
                
                # Try regular click first, if that fails, use JavaScript click
                try:
                    alumni_link.click()
                except Exception as e:
                    self.logger.info(f"Regular click failed, trying JavaScript click: {str(e)}")
                    self.driver.execute_script("arguments[0].click();", alumni_link)
                
                time.sleep(3)
                
                # Step 4: Wait for the alumni results page to load
                WebDriverWait(self.driver, 10).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div.search-results-container")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".people-search-results")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "ul.reusable-search__result-container"))
                    )
                )
                
                # Step 5: Parse the alumni results
                people_data = self._parse_search_results()
                
                # Mark all as SCU alumni since they're from the alumni hiring page
                for person in people_data:
                    person['is_scu_alumni'] = True
                    person['company'] = company_name
                
                self.logger.info(f"Found {len(people_data)} SCU alumni at {company_name}")
                return people_data
                
            else:
                self.logger.warning(f"Could not find 'people from your company were hired here' link for {company_name}")
                
                # Save page source for debugging
                try:
                    with open(f"linkedin_search_debug_{company_name.replace(' ', '_')}.html", 'w', encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                    self.logger.info(f"Saved page source for debugging: linkedin_search_debug_{company_name.replace(' ', '_')}.html")
                except:
                    pass
                
                return []
                
        except Exception as e:
            self.logger.error(f"Error searching company alumni for {company_name}: {str(e)}")
            return []
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            self.logger.info("Browser closed")