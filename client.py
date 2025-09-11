from openai import OpenAI, AsyncOpenAI

from config import Config

class Client:
    def __init__(self, config: Config):
        self.config = config
        self.client = OpenAI(api_key = config.OPENAI_API_KEY)
        self.model = config.MODEL_NAME

    def generate(self, prompt: str) -> str:
        response = self.client.responses.create(
            model = self.model,
            input = prompt,
        )
        return response.error, response.output_text

class AsyncClient:
    def __init__(self, config: Config):
        self.config = config
        self.client = AsyncOpenAI(api_key = config.OPENAI_API_KEY)
        self.model = config.MODEL_NAME

    async def generate(self, prompt: str) -> str:
        response = await self.client.responses.create(
            model = self.model,
            input = prompt,
        )
        return response