import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPEN_AI_KEY1")

question = input('What is your question: ')
# model="text-davinci-003"
# model="gpt-3.5-turbo"
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": f"{ question }"},
        ]
    )

result = ''
for choice in response.choices:
    result += choice.message.content

print(f"We asked chatGPT { question } - Here Is there Answer:")
print("-----------------------------------------------------------------")
print(result)