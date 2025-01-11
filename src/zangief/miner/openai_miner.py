from openai import OpenAI, APIError
from loguru import logger
from openai.types.chat.chat_completion import ChatCompletion
from base_miner import BaseMiner

class OpenAIMiner(BaseMiner):

    def __init__(self, config) -> None:
        super().__init__()
        self.config = config 
        self.max_tokens = int(str(object=config.openai.get("max_tokens"), default=1000))
        self.temperature = str(object=config.openai.get("temperature"), default=0.1)
        self.model = str(object=config.openai.get("openai_model"), default="gpt-3.5-turbo")
        api_key = str(object=config.openai.get("openai_api_key"), default=None)
        if api_key is None:
            raise ValueError(
                "OpenAI key must be specified in the env/config.ini (openai_key = YOUR_KEY_HERE)"
            )
        self.client = OpenAI(
            api_key=api_key,
            base_url=str(object=config.openai.get("openai_base_url"), default="https://api.openai.com/v1")
        )
        self.system_prompt = "You are an expert translator who can translate text from a large number of languages. You pay attention to detail providing semantically and grammatically accurate translations quickly and effectively. You will be asked by users to translate text from one language to another. You will not provide any additional context or instructions. Simply return the translated response."

    def generate_translation(
        self, prompt: str, source_language: str, target_language: str
    ) -> str | None:
        user_prompt: str = (
            f"Translate the following text from {source_language} to {target_language}: {prompt}"
        )
        system_prompt: str = self.system_prompt
        completion: ChatCompletion = self.client.chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        try:
            translation: str | None = completion.choices[0].message.content
        except APIError as e:
            logger.error(f"Error parsing OpenAI response: {e}")
            translation = None

        return translation