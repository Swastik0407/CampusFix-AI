
import json
import time

from google import genai
from google.genai import types

from config.settings import GEMINI_API_KEY, GEMINI_MODEL


def analyze_complaint(description: str, location: str):

    if not GEMINI_API_KEY:
        return {
            "success": False,
            "agent": "Triage Agent",
            "error": "Gemini API key is missing."
        }

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = f"""
        You are the Triage Agent of CampusFix AI.

        Your job is to understand and classify campus complaints.

        Analyze the following complaint:

        Complaint: {description}
        Location: {location}

        Identify:
        1. The complaint category.
        2. A clear summary of the issue.
        3. The exact location.
        4. The specific type of issue.

        Select the category from:
        - Plumbing
        - Electrical
        - IT Support
        - Sanitation
        - Security
        - Maintenance
        - Administration
        - Other

        Return ONLY valid JSON in this format:

        {{
            "category": "Category name",
            "issue_summary": "Short summary of the complaint",
            "location": "Complaint location",
            "issue_type": "Specific issue type"
        }}

        Rules:
        - Do not invent information.
        - Keep the summary concise.
        - Use only the provided complaint details.
        - Return valid JSON only.
        """

        # Retry Gemini API if the service is temporarily unavailable.
        response = None

        for attempt in range(3):

            try:
                print(
                    f"[Triage Agent] Gemini API attempt {attempt + 1}/3",
                    flush=True
                )

                response = client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )

                break

            except Exception as e:

                error_message = str(e)

                if "503" in error_message or "UNAVAILABLE" in error_message:

                    print(
                        f"[Triage Agent] Gemini temporarily unavailable. "
                        f"Retrying...",
                        flush=True
                    )

                    if attempt < 2:
                        time.sleep(3 * (attempt + 1))
                    else:
                        raise

                else:
                    raise

        # Parse Gemini response.
        if not response or not response.text:
            raise ValueError("Gemini returned an empty response.")

        result = json.loads(response.text)

        # Validate required fields.
        required_fields = [
            "category",
            "issue_summary",
            "location",
            "issue_type"
        ]

        for field in required_fields:
            if field not in result or not isinstance(result[field], str) or not result[field].strip():
                raise ValueError(f"Missing or invalid field: {field}")

        allowed_categories = [
            "Plumbing",
            "Electrical",
            "IT Support",
            "Sanitation",
            "Security",
            "Maintenance",
            "Administration",
            "Other"
        ]

        if result["category"] not in allowed_categories:
            raise ValueError(
                f"Invalid complaint category: {result['category']}"
            )

        print("[Triage Agent] Analysis completed successfully.", flush=True)

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
