
from backend.database import (
    initialize_database,
    create_complaint,
    get_all_complaints,
    update_complaint
)


def save_ticket(ticket: dict):

    try:
        # Initialize database if required.
        initialize_database()

        # Save basic complaint details.
        create_complaint(
            ticket_id=ticket["ticket_id"],
            description=ticket["description"],
            location=ticket["location"],
            student_name=ticket.get("student_name")
        )

        # Update AI-generated classification details.
        update_complaint(
            ticket_id=ticket["ticket_id"],
            category=ticket["category"],
            priority=ticket["priority"],
            department=ticket["department"]
        )

        print(
            f"[Database Agent] Ticket saved: {ticket['ticket_id']}",
            flush=True
        )

        return {
            "success": True,
            "agent": "Database Agent",
            "message": "Ticket saved successfully.",
            "ticket_id": ticket["ticket_id"]
        }

    except Exception as e:

        print(
            f"[Database Agent ERROR] {type(e).__name__}: {e}",
            flush=True
        )

        return {
            "success": False,
            "agent": "Database Agent",
            "error": str(e)
        }


def fetch_all_tickets():

    try:
        initialize_database()

        tickets = get_all_complaints()

        return {
            "success": True,
            "agent": "Database Agent",
            "tickets": tickets
        }

    except Exception as e:

        print(
            f"[Database Agent ERROR] {type(e).__name__}: {e}",
            flush=True
        )

        return {
            "success": False,
            "agent": "Database Agent",
            "error": str(e)
        }
