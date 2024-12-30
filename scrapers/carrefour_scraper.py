from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from scrapers.base_scraper import BaseScraper
import logging
import time

class CarrefourScraper(BaseScraper):
    def __init__(self, selenium_agent):
        super().__init__(selenium_agent)
        self.url = "https://www.carrefour.com.ar"
        
    def scrape_products(self, item_list):
        logging.info("=== Iniciando scraping de Carrefour ===")
        logging.info(f"Items a buscar: {', '.join(item_list)}")
        results = []
        driver = self.selenium_agent.driver
        
        try:
            for item in item_list:
                try:
                    # Navegación inicial
                    driver.get(self.url)
                    search_box = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='¿Qué estás buscando?']"))
                    )
                    search_box.clear()
                    search_box.send_keys(item)
                    search_box.send_keys(Keys.RETURN)

                    # Esperar y hacer scroll para cargar todo el contenido
                    time.sleep(1)
                    for _ in range(3):
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(1)
                    
                    # Volver al inicio
                    driver.execute_script("window.scrollTo(0, 0);")

                    # Obtener artículos
                    articles = driver.find_elements(By.XPATH, "//article")
                    logging.info(f"Encontrados {len(articles)} productos en Carrefour para '{item}'")
                    
                    for article in articles:
                        try:
                            # Intentar diferentes patrones para encontrar el nombre
                            name = None
                            name_patterns = [
                                ".//span[contains(@class, 'vtex-product-summary-2-x-productBrand')]",
                                ".//span[contains(@class, 'brandName')]",
                                ".//h3[contains(@class, 'vtex-product-summary-2-x-brandName')]//span",
                                ".//div[contains(@class, 'nameContainer')]//span",
                                ".//span[contains(@class, 'productBrand')]"
                            ]

                            for pattern in name_patterns:
                                try:
                                    name_element = article.find_element(By.XPATH, pattern)
                                    name = name_element.text.strip()
                                    if name:
                                        break
                                except:  # Silenciosamente continuar si no encuentra el elemento
                                    continue

                            # Si no se encontró nombre, saltar este artículo silenciosamente
                            if not name:
                                continue

                            # Obtener precio
                            try:
                                price_text = article.find_element(
                                    By.XPATH, 
                                    ".//span[@class='valtech-carrefourar-product-price-0-x-sellingPriceValue']"
                                )
                                price_clean = price_text.text.strip()
                                price_clean = price_clean.replace('$', '').strip()
                                price_clean = price_clean.replace('.', '')
                                price_clean = price_clean.replace(',', '.')
                                price_clean = price_clean.split()[0]  # Solo el precio base
                                price = float(price_clean)
                            except Exception as e:
                                logging.warning(f"Error al procesar precio: {e}")
                                continue

                            # Obtener nombre del producto
                            name = None
                            name_patterns = [
                                ".//span[contains(@class, 'vtex-product-summary-2-x-productBrand')]",
                                ".//span[contains(@class, 'brandName')]",
                                ".//h3[contains(@class, 'vtex-product-summary-2-x-brandName')]//span",
                                ".//div[contains(@class, 'nameContainer')]//span",
                                ".//span[contains(@class, 'productBrand')]"  # Mantener el patrón original como fallback
                            ]

                            for pattern in name_patterns:
                                try:
                                    name_element = article.find_element(By.XPATH, pattern)
                                    name = name_element.text.strip()
                                    if name:
                                        break
                                except Exception:
                                    continue

                            if not name:
                                logging.warning("No se pudo encontrar el nombre del producto")
                                continue

                            # Obtener precio por unidad (opcional)
                            unit_price = "N/A"
                            try:
                                unit_price_element = article.find_element(
                                    By.XPATH,
                                    ".//span[contains(@class, 'unit')]"
                                )
                                unit_price = unit_price_element.text.strip()
                            except Exception:
                                pass

                            # Agregar producto si tenemos nombre y precio válidos
                            if name and price:
                                results.append({
                                    'name': name.strip(),
                                    'price': price,
                                    'unit_price': unit_price,
                                    'brand': "N/A",
                                    'weight': "N/A"
                                })
                                logging.info(f"Producto procesado: {name} - ${price}")

                        except Exception as e:
                            logging.warning(f"Error al procesar artículo: {e}")

                except TimeoutException as e:
                    logging.warning(f"Timeout al buscar '{item}': {e}")
                except Exception as e:
                    logging.warning(f"Error procesando búsqueda de '{item}': {e}")

        except Exception as e:
            logging.error(f"Error general en Carrefour scraper: {e}")
            
        return results