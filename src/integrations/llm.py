from openai import OpenAI

from config import settings


class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(
        self,
        input_user: str,
        system_prompt: str | None = None,
        temperature: float = 1,
        model: str = "gpt-5-mini-2025-08-07",
    ):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": input_user})

        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )

        return response.choices[0].message.content

    def generate_with_websearch(self, query: str) -> dict:
        """Perform a search using OpenAI's API."""
        completion = self.client.chat.completions.create(
            model="gpt-4o-search-preview",
            web_search_options={},
            messages=[
                {
                    "role": "user",
                    "content": "What was a positive news story from today?",
                }
            ],
        )

        return completion.choices[0].message.content


if __name__ == "__main__":
    llm_client = LLMClient()
    result = llm_client.generate("Hai Apakabar?")
    print(result)
