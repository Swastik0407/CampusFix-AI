
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


# Allowed complaint categories
ALLOWED_CATEGORIES = [
    "Plumbing",
    "Electrical",
    "IT Support",
    "Sanitation",
    "Security",
    "Maintenance",
    "Administration",
    "Other"
]


def analyze_complaint(description: str, location: str):

    if not NVIDIA_API_KEY:
        return {
            "success": False,
            "agent": "Triage Agent",
            "error": "NVIDIA API key is missing."
        }

    if not isinstance(description, str) or not description.strip():
        return {
            "success": False,
            "agent": "Triage Agent",
            "error": "Complaint description cannot be empty."
        }

    if not isinstance(location, str) or not location.strip():
        return {
            "success": False,
            "agent": "Triage Agent",
            "error": "Complaint location cannot be empty."
        }

    try:

        client = OpenAI(
            base_url=NVIDIA_BASE_URL,
            api_key=NVIDIA_API_KEY,
            timeout=45.0,
            max_retries=0
        )

        prompt = f"""
You are the Triage Agent of CampusFix AI.

Analyze the following campus complaint.

Complaint: {description}
Location: {location}

Identify:
1. Complaint category.
2. Short issue summary.
3. Exact location.
4. Specific issue type.

Allowed categories:
{", ".join(ALLOWED_CATEGORIES)}

Return ONLY valid JSON in this format:

{{
    "category": "Plumbing",
    "issue_summary": "Water pipe leakage",
    "location": "Boys Hostel",
    "issue_type": "Water leakage"
}}

Rules:
- Select exactly one allowed category.
- Do not invent information.
- Keep the summary concise.
- Use only the provided complaint details.
- Preserve the supplied location exactly.
- Return valid JSON without Markdown.
"""

        response = None

        # Retry temporarily failed API requests
        for attempt in range(3):

            try:

                print(
                    f"[Triage Agent] NVIDIA API attempt "
                    f"{attempt + 1}/3",
                    flush=True
                )

                response = client.chat.completions.create(
                    model=NVIDIA_MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are CampusFix AI's Triage Agent. "
                                "Analyze campus complaints and return "
                                "only valid JSON."
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
                    f"[Triage Agent] Temporary API error: {e}",
                    flush=True
                )

                if attempt == 2:
                    raise

                wait_time = 3 * (attempt + 1)
                time.sleep(wait_time)

            except APIStatusError as e:

                if e.status_code == 429 or e.status_code >= 500:

                    if attempt == 2:
                        raise

                    time.sleep(3 * (attempt + 1))

                else:
                    raise

        # Validate API response
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

        # Extract JSON
        json_start = response_text.find("{")

        if json_start == -1:
            raise ValueError("No JSON object found in NVIDIA response.")

        result, _ = json.JSONDecoder().raw_decode(
            response_text[json_start:]
        )

        if not isinstance(result, dict):
            raise ValueError("Invalid JSON object.")

        # Validate required fields
        required_fields = [
            "category",
            "issue_summary",
            "location",
            "issue_type"
        ]

        for field in required_fields:

            value = result.get(field)

            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"Missing or invalid field: {field}"
                )

            result[field] = value.strip()

        # Validate category
        if result["category"] not in ALLOWED_CATEGORIES:
            raise ValueError(
                f"Invalid complaint category: {result['category']}"
            )

        # Preserve original user-provided location
        result["location"] = location.strip()

        print(
            "[Triage Agent] NVIDIA analysis completed successfully.",
            flush=True
        )

        return {
            "success": True,
            "agent": "Triage Agent",
            "analysis": result
        }

    except Exception as e:

        print(
            f"[Triage Agent ERROR] {type(e).__name__}: {e}",
            flush=True
        )

        return {
            "success": False,
            "agent": "Triage Agent",
            "error": str(e)
        }
