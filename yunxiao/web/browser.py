from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import Optional
import time
import logging

def request_aliyun_login_ticket(headless: bool = False, timeout_minutes: int = 5) -> Optional[str]:
    """
    Open a webview using Selenium Chrome WebDriver and wait for user operations.
    
    Args:
        timeout_minutes (int): Maximum time to wait for user operations in minutes
        
    Returns:
        the aliyun login ticket
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    
    # Add additional options for better webview experience
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Solution 1: Disable the Permissions Policy enforcement
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # # Solution 2: Explicitly allow sensor access
    # chrome_options.add_argument("--enable-features=WebXR")
    # chrome_options.add_argument("--enable-features=GenericSensorExtraClasses")
    # chrome_options.add_argument("--enable-features=WebXRHandInput")

    # # Alternative: Set Permissions Policy through experimental option
    # chrome_options.add_experimental_option("prefs", {
    #     "profile.default_content_setting_values.sensors": 1,
    #     "profile.default_content_setting_values.geolocation": 1
    # })

    login_ticket = None

    try:
        # Initialize the Chrome WebDriver
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        
        # Navigate to the initial URL
        initial_url = "https://devops.aliyun.com/workbench"
        driver.get(initial_url)
        logging.info(f"Opened initial URL: {initial_url}")

        # Calculate timeout in seconds
        timeout_seconds = timeout_minutes * 60
        start_time = time.time()
        last_url = initial_url

        while True:
            current_url = driver.current_url
            if current_url != last_url:
                logging.info(f"URL changed to: {current_url}")
                last_url = current_url

            if current_url == initial_url:
                logging.info('Login successfully')
                cookies = driver.get_cookies()

                cookie_ticket = next((cookie for cookie in cookies if cookie['name'] == 'login_aliyunid_ticket'), None)
                if cookie_ticket:
                    # logging.info(f"Found cookie: {cookie_ticket}")
                    login_ticket = cookie_ticket.get('value')

                break

            # Check if timeout has been reached
            if time.time() - start_time > timeout_seconds:
                logging.warning(f"Operation timeout reached after {timeout_minutes} minutes")
                break

            time.sleep(1)  # Check every second
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
    finally:
        if 'driver' in locals():
            driver.quit()

    return login_ticket
