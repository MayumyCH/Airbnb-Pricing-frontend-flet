
import httpx
from typing import List, Dict, Any, TypedDict, Literal

# --- Tipos para el cuerpo de la solicitud ---
class ApiRequestBody(TypedDict):
    latitude: float
    longitude: float
    accommodates: int
    bedrooms: int
    beds: int
    minimum_nights: int

# --- Tipos para la respuesta de la API ---
class JustificationItem(TypedDict):
    description: str
    impact: float
    type: Literal["positive", "negative"]

class CompetitiveAnalysis(TypedDict):
    your_price: float
    neighborhood_average: float
    neighborhood_max: float

class ApiResponse(TypedDict):
    suggested_price: float
    percentage_vs_average: float
    justification: List[JustificationItem]
    competitive_analysis: CompetitiveAnalysis

# URL del endpoint de la API (ajustar si es necesario)
PRICE_API_URL = "http://127.0.0.1:8000/api/v1/predict"
AVERAGE_API_URL = "http://127.0.0.1:8000/api/v1/average_price" 

async def get_price_suggestion(data: ApiRequestBody) -> Dict[str, Any]:
    """
    Realiza una llamada asíncrona a la API de predicción de precios.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(PRICE_API_URL, json=data, timeout=20.0)
            response.raise_for_status()  # Lanza una excepción para respuestas 4xx/5xx
            return response.json()
        except httpx.ConnectError:
            return {"error": "No se pudo conectar a la API. ¿El servidor está en funcionamiento?"}
        except httpx.HTTPStatusError as e:
            return {"error": f"Error de la API: {e.response.status_code} - {e.response.text}"}
        except Exception as e:
            return {"error": f"Ocurrió un error inesperado: {str(e)}"}

async def get_average_price(data: ApiRequestBody) -> Dict[str, Any]:
    """
    Realiza una llamada asíncrona a la API de precios promedio.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(AVERAGE_API_URL, json=data, timeout=20.0)
            response.raise_for_status()
            return response.json()
        except httpx.ConnectError:
            return {"error": "No se pudo conectar a la API de promedios."}
        except httpx.HTTPStatusError as e:
            return {"error": f"Error de la API de promedios: {e.response.status_code} - {e.response.text}"}
        except Exception as e:
            return {"error": f"Ocurrió un error inesperado en promedios: {str(e)}"}
