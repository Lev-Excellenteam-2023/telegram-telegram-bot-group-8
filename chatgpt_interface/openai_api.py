import openai
import os


class OpenAIChatAPI:
    def __init__(self):
        self.system_role = ""
        openai.api_key = os.getenv("OPENAI_API_KEY")

    async def generate_response(self, prompt: str):
        completion = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=prompt,
            max_tokens=50
        )

        chat_response = completion.choices[0].message.content
        return chat_response

    def set_system_role(self, role: str):
        self.system_role = role