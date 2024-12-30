from typing import List, Dict
import logging
from dataclasses import dataclass
import json
from openai import OpenAI
import os
from dotenv import load_dotenv

@dataclass
class ProductComparison:
    item_requested: str
    store1_product: Dict
    store2_product: Dict
    best_price: str

class PriceComparisonAIAgent:
    """
    Agente de IA que usa el modelo o1-mini de OpenAI para:
    1. Comparar productos entre supermercados
    2. Identificar mejores precios
    3. Generar recomendaciones de compra
    """

    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.logger = logging.getLogger(__name__)

    def compare_prices(self, store1_products: List[Dict], store2_products: List[Dict], item_list: List[str]) -> Dict:
        """Compara precios usando el modelo o1-mini de OpenAI"""
        
        prompt = (
            "Eres un agente que compara precios de productos entre Supermami y Carrefour para planificar \n"
            "dónde conviene hacer el pedido y optimizar el costo total de la compra \n"
            "Cuando encuentres múltiples coincidencias, SIEMPRE elige el de menor precio.\n\n"
            "- Has un listado con los productos que tomaste de cada lista y sus correspondientes precios \n\n"
            " - Considera productos base y sus variantes (ej: 'leche' → 'leche entera 1L') para lograr coincidencias\n\n"
            " - Evita falsos positivos (ej: 'leche' NO debe matchear con 'dulce de leche')\n\n"
            "Reglas:\n"
            "1. Solo selecciona productos que existan EXACTAMENTE en las listas y el que más se asemeje a cada item solicitado\n"
            "2. No inventes ni modifiques nombres de productos\n"
            "3. Para múltiples coincidencias, elige el de menor precio\n"
            "4. Si no hay match, usa 'No disponible' en el precio\n\n"
            "5. Haz un breve análisis de los precios y la diferencia y decide quien tiene mejores precios\n\n"
            f"Datos para comparar:\n{json.dumps({'productos_solicitados': item_list, 'supermami': store1_products, 'carrefour': store2_products}, indent=2)}"
        )

        try:
            response = self.client.chat.completions.create(
                model="o1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            if not response or not response.choices:
                self.logger.error("La respuesta de OpenAI no contiene choices")
                return None

            ai_response = response.choices[0].message.content
            return ai_response

        except Exception as e:
            self.logger.error(f"Error inesperado: {e}")
            return None

    def format_results(self, comparison_text: str) -> str:
        """Devuelve el texto de comparación sin procesar"""
        return comparison_text

    def get_summary(self, comparison_text: str) -> str:
        """Devuelve el texto de comparación sin procesar"""
        return comparison_text 