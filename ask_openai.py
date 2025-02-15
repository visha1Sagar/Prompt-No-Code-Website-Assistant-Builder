import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(".env")
openai_api_key = os.getenv("OPENAI_API_KEY")
OpenAI.api_key = openai_api_key

def ask_openai(prompt, token_count, top_p=0.1, temperature=0.3, presence_penalty=0.0, frequency_penalty=0.0, developer_prompt = ""):
      # Define the prompt for title and outline generation
      
        

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {openai_api_key}"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
                        {"role": "developer", "content": developer_prompt},
                         {"role": "user", "content": prompt},
                         ],
            "max_completion_tokens": token_count,
            "temperature": temperature,
            "top_p": top_p,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,

        }

        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            output = response_data['choices'][0]['message']['content']
            return output.strip()
        else:
            print(f"Failed to generate title and outline: {response.status_code}")
            print(response.text)
            return "", [], []
    


    