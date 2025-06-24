import logging
import os
import sys
import time
import random
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Environment variables
current_path = os.path.dirname(os.path.abspath(__file__)) + os.sep
ORIGINAL_RESUME_PATH = os.environ.get("ORIGINAL_RESUME_PATH", current_path+"Resume.pdf")
USERNAME = os.environ["NAUKRI_USERNAME"]
PASSWORD = os.environ["NAUKRI_PASSWORD"]
NAUKRI_LOGIN_URL = os.environ.get("NAUKRI_LOGIN_URL", "https://www.naukri.com/nlogin/login")
NAUKRI_PROFILE_URL = os.environ.get("NAUKRI_PROFILE_URL", "https://www.naukri.com/mnjuser/profile")

# User configuration
originalResumePath = ORIGINAL_RESUME_PATH
username = USERNAME
password = PASSWORD
headless = True
NaukriURL = NAUKRI_LOGIN_URL

logging.basicConfig(
    level=logging.INFO, filename="naukri.log", filemode='a',
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def log_msg(message, level=logging.INFO):
    print(message)
    logging.log(level, message)

def catch(error):
    _, _, exc_tb = sys.exc_info()
    lineNo = exc_tb.tb_lineno if exc_tb else "?"
    msg = f"ERROR: {type(error).__name__}: {error} at Line {lineNo}."
    print(msg)
    logging.error(msg)

def human_delay(min_delay=1, max_delay=3):
    """Add random human-like delays"""
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)

def type_like_human(element, text, typing_speed=0.1):
    """Type text with human-like speed and occasional pauses"""
    for char in text:
        element.send_keys(char)
        # Random typing speed with occasional longer pauses
        if random.random() < 0.1:  # 10% chance of longer pause
            time.sleep(random.uniform(0.3, 0.8))
        else:
            time.sleep(random.uniform(0.05, typing_speed))



def handle_popups_and_notifications(driver):
    """Handle common popups and notifications in a human-like way"""
    try:
        # Check for common popup elements
        popup_selectors = [
            "button[aria-label='Close']",
            ".close-button",
            "[data-dismiss='modal']",
            ".modal-close",
            "button:contains('Not now')",
            "button:contains('Later')",
            "button:contains('Skip')"
        ]

        for selector in popup_selectors:
            try:
                popup = driver.find_element(By.CSS_SELECTOR, selector)
                if popup.is_displayed():
                    human_delay(0.5, 1.5)  # Hesitate before closing
                    popup.click()
                    log_msg("Closed a popup/notification")
                    human_delay(0.5, 1.0)
                    break
            except:
                continue
    except Exception as e:
        log_msg(f"Popup handling failed: {e}")

def LoadNaukri(headless_mode):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    options.add_argument("--disable-popups")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Add user agent to appear more human
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    # Required for Docker environment
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if headless_mode:
        options.add_argument("--headless=new")  # Use new headless mode for better compatibility
        options.add_argument("--window-size=1920,1080")

    try:
        # Explicitly specify ChromeDriver path in the container
        service = ChromeService(executable_path="/usr/bin/chromedriver")
        driver = webdriver.Chrome(options=options, service=service)
        
        # Execute script to hide webdriver property
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        log_msg("Google Chrome launched with human-like settings.")
        driver.implicitly_wait(5)

        # Navigate with human-like behavior
        log_msg("Navigating to Naukri...")
        driver.get(NaukriURL)

        # Simulate initial page load waiting
        human_delay(2, 4)

        return driver
    except WebDriverException as e:
        catch(e)
        log_msg("Could not launch Chrome. Check your ChromeDriver and PATH.", level=logging.CRITICAL)
        return None

def naukriLogin(headless=False):
    status = False
    driver = LoadNaukri(headless)
    if not driver:
        return (status, None)

    try:
        log_msg("Waiting for login page to load...")
        # Wait for page to load with human-like patience
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "usernameField"))
        )
        log_msg("Naukri login page loaded successfully.")

        # Handle any initial popups
        # handle_popups_and_notifications(driver)

        # Simulate looking around the page before interacting
        # random_mouse_movement(driver)
        human_delay(1, 3)

        # Find and interact with username field
        log_msg("Locating username field...")
        user_elem = driver.find_element(By.ID, "usernameField")

        # Click on username field (human-like interaction)
        user_elem.click()
        human_delay(0.5, 1.0)

        # Clear field with human-like behavior
        user_elem.clear()
        human_delay(0.3, 0.7)

        # Type username with human-like speed
        log_msg("Entering username...")
        type_like_human(user_elem, username)

        # Brief pause before moving to password field
        human_delay(0.8, 1.5)

        # Find and interact with password field
        log_msg("Locating password field...")
        pass_elem = driver.find_element(By.ID, "passwordField")
        pass_elem.click()
        human_delay(0.5, 1.0)

        pass_elem.clear()
        human_delay(0.3, 0.7)

        # Type password with human-like speed
        log_msg("Entering password...")
        type_like_human(pass_elem, password, 0.08)  # Slightly faster for password

        # Pause before clicking login (as humans do)
        human_delay(1, 2)

        # Random mouse movement before clicking login
        # random_mouse_movement(driver)
        human_delay(0.5, 1.0)

        # Click login button
        log_msg("Clicking login button...")
        login_button = driver.find_element(By.XPATH, "//*[@type='submit' and normalize-space()='Login']")
        login_button.click()

        # Wait for login to process
        log_msg("Waiting for login to process...")
        human_delay(3, 5)

        # Check if login was successful
        try:
            log_msg("Verifying login status...")

            # Wait for a moment to allow redirect after login
            human_delay(2, 3)

            # Check if redirected to homepage or profile areas
            if "mnjuser/homepage" in driver.current_url or "mnjuser/profile" in driver.current_url:
                log_msg("Login successful - redirected to user area.")
                status = True
            else:
                # Try looking for elements that only appear when logged in
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".nI-gNb-user"))
                    )
                    log_msg("Login successful - user profile element found.")
                    status = True
                except (NoSuchElementException, TimeoutException):
                    log_msg("Login verification failed - user elements not found.")
                    status = False

        except Exception as e:
            log_msg(f"Login verification error: {e}")
            status = False



        # Handle any post-login popups
        handle_popups_and_notifications(driver)

        # Navigate to profile to confirm login
        log_msg("Navigating to profile page...")
        driver.get(NAUKRI_PROFILE_URL)
        human_delay(2, 4)



        if "profile" in driver.current_url:
            log_msg("Naukri Login Successful.")
            status = True
        else:
            log_msg("Login verification failed - not on profile page")

    except Exception as e:
        catch(e)
        log_msg("Login process failed due to an exception.", level=logging.ERROR)

    return (status, driver)

def upload_resume(driver, RESUME_PATH):
    try:
        log_msg("Preparing to upload resume...")
        driver.get(NAUKRI_PROFILE_URL)
        human_delay(3, 5)


        # Try to find the file input element
        file_input = None
        input_selectors = ["#attachCV", "#lazyAttachCV", "input[type='file']"]

        for selector in input_selectors:
            try:
                file_input = driver.find_element(By.CSS_SELECTOR, selector)
                if file_input:
                    log_msg(f"Found resume upload input: {selector}")
                    break
            except:
                continue

        if not file_input:
            log_msg("Resume upload input field not found.")
            return False

        # Human-like pause before uploading
        human_delay(1, 2)

        log_msg("Uploading resume file...")
        file_input.send_keys(RESUME_PATH)

        # Wait for upload to process
        human_delay(3, 6)

        # Simulate checking if upload was successful
        log_msg("Verifying upload completion...")
        human_delay(2, 3)

        log_msg("Resume upload completed. Please check your Naukri profile to confirm update.")
        return True

    except Exception as e:
        log_msg(f"Error during resume upload: {e}")
        return False

def cleanup_and_exit(driver):
    """Clean exit with human-like behavior"""
    try:
        if driver:
            log_msg("Cleaning up session...")
            # Simulate natural browsing end
            human_delay(1, 2)

            # Clear cookies and session data
            driver.delete_all_cookies()
            human_delay(0.5, 1.0)

            driver.quit()
            log_msg("Browser closed successfully.")
    except Exception as e:
        log_msg(f"Error during cleanup: {e}")

def main():
    log_msg("-----Naukri.py Human-like Script Run Begin-----")
    driver = None

    try:
        # Add initial human-like delay
        human_delay(1, 3)

        status, driver = naukriLogin(headless)

        if status and driver:
            log_msg("Login successful, proceeding with resume upload...")

            if os.path.exists(originalResumePath):
                upload_success = upload_resume(driver, originalResumePath)
                if upload_success:
                    log_msg("Resume upload process completed successfully.")
                else:
                    log_msg("Resume upload encountered issues.")
            else:
                log_msg(f"Resume not found at {originalResumePath}", level=logging.ERROR)
        else:
            log_msg("Login unsuccessful. Skipping resume upload.", level=logging.ERROR)

    except Exception as e:
        catch(e)
        log_msg("Exception occurred in main().", level=logging.ERROR)

    finally:
        cleanup_and_exit(driver)
        log_msg("-----Naukri.py Human-like Script Run Ended-----\n")

if __name__ == "__main__":
    main()
