# src/mavera/client.py
from typing import Dict, Any
import httpx
from .models import ChatRequest, ChatResponse
from .exceptions import MaveraError, AuthenticationError
from src.mavera.database import PersonaDB, PersonaNotFoundError


class Mavera:
    def __init__(
        self,
        api_key: str,
        base_url: str = "http://localhost:8000/v1"
    ):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self._client = httpx.Client(
            headers={
                "X-Mavera-API-Key": api_key,
                "Content-Type": "application/json"
            }
        )
    
    def chat(self, persona: str, message: str) -> Dict[str, Any]:
        """
        Send a chat message to a specific persona.
        """
        try:
            response = self._client.post(
                f"{self.base_url}/chat",
                json={
                    "persona": persona,
                    "message": message
                }
            )
            
            if response.status_code == 404:
                error_detail = response.json().get("detail", "Persona not found")
                raise PersonaNotFoundError(error_detail)
                
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                error_detail = e.response.json().get("detail", "Persona not found")
                raise PersonaNotFoundError(error_detail)
            raise MaveraError(f"API request failed: {str(e)}")