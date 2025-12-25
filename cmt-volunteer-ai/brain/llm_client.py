import requests
import yaml

HF_API = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HEADERS = {"Authorization": "Bearer YOUR_HF_TOKEN"}

with open("config/prompts.yaml") as f:
    PROMPTS = yaml.safe_load(f)

def call_llm(prompt, text):
    payload = {
        "inputs": f"{prompt}\nText:\n{text}"
    }
    response = requests.post(HF_API, headers=HEADERS, json=payload)
    return response.json()[0]["generated_text"]
