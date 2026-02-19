import httpx
from app.core.config import settings
from typing import Dict, Any

class GrokService:
    def __init__(self):
        self.api_key = settings.GROK_API_KEY
        self.base_url = "https://api.x.ai/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    async def process_command(self, user_text: str) -> str:
        """
        Sends user text to Grok-4 for intent parsing and response generation.
        """
        system_prompt = """
        You are AI Time OS, an intelligent scheduling assistant.
        Your goal is to parse the user's voice command and return a structured JSON-like response,
        but for now, return a concise, natural language confirmation of what action you will take.
        Keep it under 2 sentences.
        If the user asks to schedule something, confirm the time and details.
        """
        
        payload = {
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_text}
            ],
            "model": "grok-4-latest",
            "stream": False,
            "temperature": 0
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url, 
                    headers=self.headers, 
                    json=payload,
                    timeout=30.0
                )
                
            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]
            else:
                print(f"Grok API Error: {response.status_code} - {response.text}")
                return "I'm having trouble connecting to my brain right now."
                
        except Exception as e:
            print(f"Grok Service Exception: {e}")
            return "Something went wrong processing your request."
