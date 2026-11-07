
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

response = client.chat.completions.create(
    model=os.getenv(
        "NVIDIA_MODEL",
        "nvidia/nemotron-3.5-bolt-e4b"
    ),
    messages=[
        {
            "role": "system",
            "content": "You are a campus complaint classification AI. Return ONLY valid JSON. No markdown."
        },
        {
            "role": "user",
            "content": """
            Classify this complaint:
            Water pipe leaking in hostel.

            Return JSON in this format:
            {
                "category": "Plumbing",
                "priority": "High",
                "department": "Maintenance",
                "reason": "Water pipe leakage in hostel"
            }
            """
        }
    ],
    temperature=0.2,
    max_tokens=300
)

print(response.choices[0].message.content)
