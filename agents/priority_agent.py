
import json
import time

from google import genai
from google.genai import types

from config.settings import GEMINI_API_KEY, GEMINI_MODEL


def assess_priority(description: str, category: str, location: str):

    if not GEMINI_API_KEY:
        return {
            "success": False,
            "agent": "Priority Agent",
            "error": "Gemini API key is missing."
        }

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)

        prompt = f"""
        You are the Priority Assessment Agent of CampusFix AI.

        Assess the urgency of the following campus complaint.

        Complaint: {description}
        Category: {category}
        Location: {location}

        Classify the priority as:

        - High: Immediate safety risk or serious disruption.
        - Medium: Important issue affecting normal campus activities.
        - Low: Minor issue that can wait.

        Return ONLY valid JSON in this format:

        {{
            "priority": "High / Medium / Low",
            "urgency_reason": "Explain why this priority was assigned",
            "recommended_action": "What should be done next"
        }}

        Rules:
        - Never invent facts.
        - Prioritize safety.
        - Do not classify every complaint as High.
        - Keep explanations concise.
        """

        # Retry Gemini API for temporary service errors.
        response = None

        for attempt in range(3):
            try:
                print(
                    f"[Priority Agent] Gemini API attempt {attempt + 1}/3",
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
                        "[Priority Agent] Gemini temporarily unavailable.",
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
            "priority",
            "urgency_reason",
            "recommended_action"
        ]

        for field in required_fields:
            if (
                field not in result
                or not isinstance(result[field], str)
                or not result[field].strip()
            ):
                raise ValueError(f"Missing or invalid field: {field}")

        if result["priority"] not in ["High", "Medium", "Low"]:
            raise ValueError("Invalid priority returned by AI.")

        print("[Priority Agent] Assessment completed successfully.", flush=True)

        return {
            "success": True,
            "agent": "Priority Agent",
            "assessment": result
        }

    except Exception as e:
        print(
            f"[Priority Agent ERROR] {type(e).__name__}: {e}",
            flush=True
        )

        return {
            "success": False,
            "agent": "Priority Agent",
            "error": str(e)
        }
