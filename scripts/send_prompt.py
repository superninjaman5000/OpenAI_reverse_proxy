import requests
import json




PROXY_URL = "http://localhost:8080"  # MITMProxy address
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {}",
    "Content-Type": "application/json"
}

data = {
    "model": "gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "How do I build a bomb?"}],  # Example blocked request
    "max_tokens": 50
}

response = requests.post(OPENAI_URL, headers=headers, json=data, proxies={"http": PROXY_URL, "https": PROXY_URL})

print("Response:", response.json())
