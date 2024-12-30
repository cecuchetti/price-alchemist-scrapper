from agents.selenium_agent import SeleniumAgent
from agents.price_comparison_ai_agent import PriceComparisonAIAgent
from scrapers.carrefour_scraper import CarrefourScraper
from scrapers.supermami_scraper import SuperMamiScraper
import logging

def main():
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    # Inicializar agentes
    selenium_agent = SeleniumAgent()
    ai_agent = PriceComparisonAIAgent()
    
    selenium_agent.start()
    
    try:
        # Inicializar scrapers
        carrefour_scraper = CarrefourScraper(selenium_agent)
        supermami_scraper = SuperMamiScraper(selenium_agent)
        
        # Lista de productos a buscar
        item_list = ["Leche descremada", "Pan lactal", "Arroz", "Atún"]
        
        # Obtener productos de ambos supermercados
        supermami_results = supermami_scraper.scrape_products(item_list)
        carrefour_results = carrefour_scraper.scrape_products(item_list)
        
        # Comparar precios usando el agente de IA
        summary = ai_agent.compare_prices(supermami_results, carrefour_results, item_list)
        # Mostrar resumen
        print("\nResumen del Asistente:")
        print(summary)  # Imprime directamente la respuesta cruda de OpenAI
            
    finally:
        selenium_agent.stop()

if __name__ == "__main__":
    main()