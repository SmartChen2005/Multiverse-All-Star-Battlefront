from openai import OpenAI
import os


class Agent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required.")
        
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=self.api_key
        )
        self.model = "gpt-4o-mini"
        self.chat_history = []

    def add_context(self, context):
        self.chat_history.append({"role": "system", "content": context})

    def start_new_chat(self):
        self.chat_history = []

    def call(self, user_message):
        self.chat_history.append({"role": "user", "content": user_message})
        return self._get_response()
    
    def _get_response(self):
        chat_completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.chat_history
        )
        response = chat_completion.choices[0].message.content
        self.chat_history.append({"role": "assistant", "content": response})
        return response
    
    def get_chat_history(self):
        return self.chat_history