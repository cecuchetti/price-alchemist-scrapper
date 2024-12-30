from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scrapers.base_scraper import BaseScraper
import logging

class SuperMamiScraper(BaseScraper):
    def __init__(self, selenium_agent):
        super().__init__(selenium_agent)
        self.url = "https://www.supermami.com.ar/super/home"
        
    def scrape_products(self, item_list):
        logging.info("=== Iniciando scraping de SuperMami ===")
        logging.info(f"Items a buscar: {', '.join(item_list)}")
        results = []
        driver = self.selenium_agent.driver
        
        try:
            driver.get(self.url)
            for item in item_list:
                logging.info(f"Buscando: {item}")
                
                # Click en botón de búsqueda
                search_button = driver.find_element(By.CLASS_NAME, 'getFullSearch')
                search_button.click()
                
                # Realizar búsqueda
                search_box = driver.find_element(By.ID, 'searchText')
                search_box.clear()
                search_box.send_keys(item)
                search_box.send_keys(Keys.RETURN)
                
                # Esperar resultados
                driver.implicitly_wait(5)
                
                # Obtener productos
                products = driver.find_elements(By.CLASS_NAME, 'item')
                logging.info(f"Encontrados {len(products)} productos")
                
                for product in products:
                    try:
                        name = product.find_element(By.CLASS_NAME, 'description').text
                        price = product.find_element(By.CLASS_NAME, 'precio-unidad').find_element(By.TAG_NAME, 'span').text
                        
                        results.append({
                            'name': name.strip(),
                            'price': price.strip().replace("$", "").replace(",", "."),
                            'brand': "N/A",
                            'weight': "N/A"
                        })
                        logging.debug(f"Producto procesado: {name}")
                    except Exception as e:
                        logging.error(f"Error procesando producto: {e}")
                        
        except Exception as e:
            logging.error(f"Error en SuperMami scraper: {e}")
            
        return results 