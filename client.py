from typing import Tuple, Dict
from openai import OpenAI

from config import Config

class Client:
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key = config.OPENAI_API_KEY)
        self.model = config.MODEL_NAME

    def generate(self, prompt: str, max_tokens: int | None = None) -> str:
        response = self.client.chat.completions.create(
            model = self.model,
            messages = [{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content