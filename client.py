from openai import OpenAI

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