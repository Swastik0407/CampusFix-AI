
from uuid import uuid4
from datetime import datetime


def generate_ticket(
    description: str,
    location: str,
    category: str,
    priority: str,
    department: str,
    student_name: str = None
):

    try:
        # Generate a unique ticket ID.
        ticket_id = f"CF-{uuid4().hex[:8].upper()}"

        # Generate ticket details.
        ticket = {
            "ticket_id": ticket_id,
            "student_name": student_name or "Anonymous",
            "description": description,
            "location": location,
            "category": category,
            "priority": priority,
            "department": department,
            "status": "Pending",
            "created_at": datetime.now().isoformat()
        }

        print(
            f"[Ticket Agent] Ticket generated: {ticket_id}",
            flush=True
        )

        return {
            "success": True,
            "agent": "Ticket Agent",
            "ticket": ticket
        }

    except Exception as e:

        print(
            f"[Ticket Agent ERROR] {type(e).__name__}: {e}",
            flush=True
        )

        return {
            "success": False,
            "agent": "Ticket Agent",
            "error": str(e)
        }
