import os
import requests
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def init_dc(url, agent=None, iso=None, profile=None):
    """
    Initializes a Selenium WebDriver with configurable options for user agent, proxy, and profile.
    
    Args:
        url (str): The URL to open in the browser.
        agent (str, optional): The type of user agent. Options: "desktop", "ios", "android".
                               If not provided, defaults to "desktop" with a warning message.
        iso (str, optional): Proxy ISO and directory path in the format "path/to/proxies,XX",
                             where XX is the two-letter country code. Example: "proxies,US".
                             If not provided, no proxy will be configured.
        profile (str, optional): Path to the Chrome user profile directory. 
                                 If provided, the profile will be used.
    
    Returns:
        WebDriver: An instance of Selenium WebDriver.
    """
    try:
        # Define user agents
        user_agents = {
            "desktop": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
            "ipad": "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X; en-us) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B176 Safari/7534.48.3",
            "ios": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 "
                   "(KHTML, like Gecko) Version/13.0 Mobile/15E148 Safari/604.1",
            "android-1": 'Mozilla/5.0 (Linux; Android 8.0.0; SM-G955U Build/R16NW) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.91 Mobile Safari/537.36',
            "android": "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36"
        }
        
        # Set user agent with fallback to desktop if not provided
        if agent not in user_agents:
            if agent is None:
                print("[INFO] No agent provided, using desktop user agent.")
                agent = "desktop"
            else:
                raise ValueError(f"Invalid agent type '{agent}'. Choose from: {list(user_agents.keys())}.")
        
        user_agent = user_agents[agent]
        opt = webdriver.ChromeOptions()
        
        # Add user agent
        opt.add_argument(f'user-agent={user_agent}')

        # Add browser preferences
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "profile.default_content_setting_values.geolocation": 2,
            "download.default_directory": "NUL",
            "download.prompt_for_download": False
        }
        opt.add_experimental_option("prefs", prefs)
        opt.add_argument("start-maximized")
        opt.add_argument("disable-infobars")
        opt.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        
        # Configure proxy if ISO is provided
        if iso:
            proxy_dir, country_code = iso.split(",")
            proxy_path = os.path.join(proxy_dir, f"{country_code}.zip")
            if not os.path.exists(proxy_path):
                raise FileNotFoundError(f"Proxy file not found at: {proxy_path}")
            opt.add_extension(proxy_path)
        
        # Configure profile if provided
        if profile:
            profile_path = os.path.abspath(profile)
            opt.add_argument(f"user-data-dir={profile_path}")
        
        
        #Chrome Out Of memory
        opt.add_argument("--enable-auto-reload")
        # Configure logging
        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}
        # Initialize WebDriver
        driver = webdriver.Chrome(options=opt)
        driver.set_page_load_timeout(120)
        driver.get(url)
        return driver
    
    except Exception as e:
        print(f"[INIT ERROR] {str(e)}")
        print("Traceback:")
        traceback.print_exc()
        return None

driver = init_dc("https://www.google.com")