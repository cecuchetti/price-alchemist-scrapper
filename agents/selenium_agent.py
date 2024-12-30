from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager  # Importa WebDriver Manager

class SeleniumAgent:
    def __init__(self):
        self.options = Options()
        self.options.add_argument('--headless')  # No user interface
        self.options.add_argument('--no-sandbox')  
        self.options.add_argument('--disable-dev-shm-usage')  

        self.service = Service(ChromeDriverManager().install())
        self.driver = None

    def start(self):
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        
    def stop(self):
        if self.driver:
            self.driver.quit()
            
    def navigate_to(self, url: str):
        if self.driver:
            self.driver.get(url)
        else:
            raise Exception("Driver not started. Call 'start()' before navigating.")
