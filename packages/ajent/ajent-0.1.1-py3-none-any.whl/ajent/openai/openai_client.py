from ajent import LLMClient
from openai import OpenAI
from typing import Any, Dict, List
from ..response_serializer import ResponseSerializer


class OpenAIClient(LLMClient):
    def __init__(self, token: str):
        self._client = OpenAI(api_key=token)

    def send(self, messages: List[Dict], tools: List[Dict], model: str) -> Any:
        response = self._client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools
        )
        message = response.choices[0].message
        return self.serialize_response(message)
    
    def serialize_response(self, response: Any) -> Dict:
        return ResponseSerializer.serialize_message(response)