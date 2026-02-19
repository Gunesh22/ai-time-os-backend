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

    async def process_command(self, user_text: str) -> Dict[str, Any]:
        """
        Sends user text to Grok-4 for structured intent parsing.
        Returns a dictionary with action details.
        """
        system_prompt = """
        You are AI Time OS. Convert the user's request into a structued JSON command.
        
        Supported Actions: "create_event", "reschedule_event", "delete_event", "query_schedule", "optimize_day".
        
        Current Date: (Assume today is Monday, 9AM for now)
        
        OUTPUT FORMAT (Strict JSON):
        {
            "action": "create_event",
            "event": {
                "title": "Deep Work",
                "start_time": "09:00",
                "end_time": "11:00",
                "priority": "high",
                "is_fixed": true
            },
            "reply_text": "I've scheduled Deep Work for 9 AM."
        }
        
        If intent is unclear, return {"action": "clarify", "reply_text": "Could you clarify?"}
        Do NOT output markdown. Just the JSON object.
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
                content = data["choices"][0]["message"]["content"]
                # Sanitize and parse JSON
                try:
                    import json
                    # Remove any markdown code blocks if Grok adds them
                    clean_content = content.replace("```json", "").replace("```", "").strip()
                    return json.loads(clean_content)
                except Exception as e:
                    print(f"JSON Parse Error: {content}")
                    return {"action": "error", "reply_text": content} # Fallback to raw text
            else:
                return {"action": "error", "reply_text": "Brain connection failed."}
                
        except Exception as e:
            print(f"Grok Service Exception: {e}")
            return {"action": "error", "reply_text": "System error."}
