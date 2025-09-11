from openai import OpenAI, AsyncOpenAI
from openai.types.responses import Response

from config import Config

class Client:
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key = config.OPENAI_API_KEY)
        self.model = config.MODEL_NAME

    def generate(self, prompt: str) -> Response:
        response = self.client.responses.create(
            model = self.model,
            input = prompt,
        )
        return response

class AsyncClient:
    def __init__(self, config: Config):
        self.config = config
        self.client = AsyncOpenAI(api_key = config.OPENAI_API_KEY)
        self.model = config.MODEL_NAME

    async def generate(self, prompt: str) -> Response:
        response = await self.client.responses.create(
            model = self.model,
            input = prompt,
        )
        return response