import os
import requests
import openai  # ✅ Correct import
from dotenv import load_dotenv
import re


load_dotenv("../.env")
openai_api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(prompt, token_count, top_p=0.1, temperature=0.3, presence_penalty=0.0, frequency_penalty=0.0, developer_prompt=""):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    payload = {
        "model": "gpt-4o",
        "messages": [
            {"role": "system", "content": developer_prompt},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": token_count,
        "temperature": temperature,
        "top_p": top_p,
        "presence_penalty": presence_penalty,
        "frequency_penalty": frequency_penalty,
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    if response.status_code == 200:
        response_data = response.json()
        output = response_data['choices'][0]['message']['content']
        
        # Extract regex pattern using regex
        return output
    else:
        print(f"Failed to get response: {response.status_code}")
        print(response.text)
        return ""
