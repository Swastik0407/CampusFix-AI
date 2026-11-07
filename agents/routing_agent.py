
import json
import os
import re
import time

from dotenv import load_dotenv
from openai import (
    OpenAI,
    APIConnectionError,
    APITimeoutError,
    RateLimitError,
    InternalServerError,
    APIStatusError
)

# Load environment variables
load_dotenv()

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")

NVIDIA_MODEL = os.getenv(
    "NVIDIA_MODEL",
    "nvidia/nemotron-3.5-bolt-e4b"
)

NVIDIA_BASE_URL = os.getenv(
    "NVIDIA_BASE_URL",
    "https://integrate.api.nvidia.com/v1"
)


# Allowed departments
ALLOWED_DEPARTMENTS = [
    "Maintenance",
    "Electrical",
    "Plumbing",
    "IT Support",
    "Sanitation",
    "Security",
    "Administration"
]


def route_complaint(description: str, category: str, priority: str):

    # Check NVIDIA API key
    if not NVIDIA_API_KEY:
        return {
            "success": False,
            "agent": "Routing Agent",
            "error": "NVIDIA API key is missing."
        }

    if not isinstance(description, str) or not description.strip():
        return {
            "success": False,
            "agent": "Routing Agent",
            "error": "Complaint description cannot be empty."
        }

    if not isinstance(category, str) or not category.strip():
        return {
            "success": False,
            "agent": "Routing Agent",
            "error": "Complaint category cannot be empty."
        }

    if priority not in ["High", "Medium", "Low"]:
        return {
            "success": False,
            "agent": "Routing Agent",
            "error": "Invalid complaint priority."
        }

    try:

        # Initialize NVIDIA client
        client = OpenAI(
            base_url=NVIDIA_BASE_URL,
            api_key=NVIDIA_API_KEY,
            timeout=45.0,
            max_retries=0
        )

        prompt = f"""
You are the Department Routing Agent of CampusFix AI.

Your job is to route campus complaints to the appropriate department.

Complaint: {description}
Category: {category}
Priority: {priority}

Choose the most appropriate department from:

{", ".join(ALLOWED_DEPARTMENTS)}

Return ONLY valid JSON in this exact format:

{{
    "department": "Maintenance",
    "routing_reason": "Why this department was selected",
    "recommended_team": "Team responsible for handling the issue"
}}

Rules:
- Select only from the listed departments.
- Use the complaint category and description.
- Do not invent information.
- Consider priority when recommending the response.
- Keep explanations concise.
- Return valid JSON only without Markdown.
"""

        response = None

        # Retry NVIDIA API for temporary errors
        for attempt in range(3):

            try:

                print(
                    f"[Routing Agent] NVIDIA API attempt "
                    f"{attempt + 1}/3",
                    flush=True
                )

                response = client.chat.completions.create(
                    model=NVIDIA_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are CampusFix AI's Department "
                                "Routing Agent. Route campus complaints "
                                "accurately and return only valid JSON."
                            )
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.1,
                    max_tokens=500
                )

                break

            except (
                APIConnectionError,
                APITimeoutError,
                RateLimitError,
                InternalServerError
            ) as e:

                print(
                    f"[Routing Agent] Temporary NVIDIA API error: {e}",
                    flush=True
                )

                if attempt == 2:
                    raise

                wait_time = 3 * (attempt + 1)
                time.sleep(wait_time)

            except APIStatusError as e:

                if e.status_code == 429 or e.status_code >= 500:

                    print(
                        f"[Routing Agent] NVIDIA API status: "
                        f"{e.status_code}",
                        flush=True
                    )

                    if attempt == 2:
                        raise

                    time.sleep(3 * (attempt + 1))

                else:
                    raise

        # Validate NVIDIA response
        if not response or not response.choices:
            raise ValueError("NVIDIA returned an empty response.")

        response_text = response.choices[0].message.content

        if not response_text:
            raise ValueError("NVIDIA returned empty response content.")

        # Remove Markdown code fences
        response_text = response_text.strip()

        response_text = re.sub(
            r"^```(?:json)?\s*",
            "",
            response_text,
            flags=re.IGNORECASE
        )

        response_text = re.sub(
            r"\s*```$",
            "",
            response_text
        )

        # Extract JSON object
        json_start = response_text.find("{")

        if json_start == -1:
            raise ValueError("No JSON object found in NVIDIA response.")

        result, _ = json.JSONDecoder().raw_decode(
            response_text[json_start:]
        )

        if not isinstance(result, dict):
            raise ValueError("NVIDIA response is not a JSON object.")

        # Validate required fields
        required_fields = [
            "department",
            "routing_reason",
            "recommended_team"
        ]

        for field in required_fields:

            value = result.get(field)

            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"Missing or invalid field: {field}"
                )

            result[field] = value.strip()

        # Validate department
        if result["department"] not in ALLOWED_DEPARTMENTS:
            raise ValueError(
                f"Invalid department: {result['department']}"
            )

        print(
            "[Routing Agent] NVIDIA routing completed successfully.",
            flush=True
        )

        # Preserve original return structure
        return {
            "success": True,
            "agent": "Routing Agent",
            "routing": result
        }

    except Exception as e:

        print(
            f"[Routing Agent ERROR] {type(e).__name__}: {e}",
            flush=True
        )

        return {
            "success": False,
            "agent": "Routing Agent",
            "error": str(e)
        }
