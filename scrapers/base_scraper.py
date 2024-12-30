from abc import ABC, abstractmethod

class BaseScraper(ABC):
    def __init__(self, selenium_agent):
        self.selenium_agent = selenium_agent
        
    @abstractmethod
    def scrape_products(self, item_list):
        pass 