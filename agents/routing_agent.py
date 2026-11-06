
import json
import time

from google import genai
from google.genai import types

from config.settings import GEMINI_API_KEY, GEMINI_MODEL


def route_complaint(description: str, category: str, priority: str):

    if not GEMINI_API_KEY:
        return {
            "success": False,
            "agent": "Routing Agent",
            "error": "Gemini API key is missing."
        }

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = f"""
        You are the Department Routing Agent of CampusFix AI.

        Your job is to route campus complaints to the appropriate department.

        Complaint: {description}
        Category: {category}
        Priority: {priority}

        Choose the most appropriate department from:

        - Maintenance
        - Electrical
        - Plumbing
        - IT Support
        - Sanitation
        - Security
        - Administration

        Return ONLY valid JSON in this format:

        {{
            "department": "Department name",
            "routing_reason": "Why this department was selected",
            "recommended_team": "Team responsible for handling the issue"
        }}

        Rules:
        - Select only from the listed departments.
        - Use the complaint category and description.
        - Do not invent information.
        - Consider priority when recommending the response.
        - Keep explanations concise.
        """

        # Retry Gemini API for temporary service errors.
        response = None

        for attempt in range(3):
            try:
                print(
                    f"[Routing Agent] Gemini API attempt {attempt + 1}/3",
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
                        "[Routing Agent] Gemini temporarily unavailable.",
                        flush=True
                    )

                    if attempt < 2:
                        time.sleep(3 * (attempt + 1))
                    else:
                        raise
                else:
                    raise

        if not response or not response.text:
            raise ValueError("Gemini returned an empty response.")

        result = json.loads(response.text)

        required_fields = [
            "department",
            "routing_reason",
            "recommended_team"
        ]

        for field in required_fields:
            if (
                field not in result
                or not isinstance(result[field], str)
                or not result[field].strip()
            ):
                raise ValueError(f"Missing or invalid field: {field}")

        allowed_departments = [
            "Maintenance",
            "Electrical",
            "Plumbing",
            "IT Support",
            "Sanitation",
            "Security",
            "Administration"
        ]

        if result["department"] not in allowed_departments:
            raise ValueError(
                f"Invalid department: {result['department']}"
            )

        print("[Routing Agent] Routing completed successfully.", flush=True)

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
