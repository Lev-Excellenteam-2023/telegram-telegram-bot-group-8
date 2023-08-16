import os
import openai



import os
import openai

class OpenAIChatAPI:
    def __init__(self):
        self.system_role = ""
        openai.api_key = keys.OPENAI_API_KEY

    async def generate_response(self, prompt: str):
        completion = openai.Completion.create(
            model="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=1
        )
        chat_response = completion.choices[0].text.strip()
        return chat_response

    def set_system_role(self, role: str):
        self.system_role = role



