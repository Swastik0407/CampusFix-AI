
def create_student_notification(ticket: dict):

    ticket_id = ticket.get("ticket_id", "N/A")
    student_name = ticket.get("student_name") or "Student"
    status = ticket.get("status", "Pending")

    return {
        "recipient": "Student",
        "message": (
            f"Hello {student_name}, your complaint has been registered. "
            f"Your ticket ID is {ticket_id}. "
            f"Current status: {status}."
        )
    }


def create_admin_notification(ticket: dict):

    return {
        "recipient": "Administrator",
        "message": (
            f"New campus complaint received. "
            f"Ticket ID: {ticket.get('ticket_id')}. "
            f"Department: {ticket.get('department')}. "
            f"Priority: {ticket.get('priority')}."
        )
    }


def prepare_notifications(ticket: dict):

    try:
        student_notification = create_student_notification(ticket)
        admin_notification = create_admin_notification(ticket)

        return {
            "success": True,
            "notifications": {
                "student": student_notification,
                "admin": admin_notification
            },
            "delivery_status": "Prepared - Not Sent"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
