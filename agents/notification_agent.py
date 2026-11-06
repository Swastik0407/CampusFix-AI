
def prepare_notification(ticket: dict):

    try:
        ticket_id = ticket["ticket_id"]
        student_name = ticket.get("student_name", "Student")
        description = ticket["description"]
        location = ticket["location"]
        priority = ticket["priority"]
        department = ticket["department"]

        # Notification for the student.
        student_message = (
            f"Hello {student_name}, your campus complaint has been "
            f"registered successfully.\n"
            f"Ticket ID: {ticket_id}\n"
            f"Issue: {description}\n"
            f"Location: {location}\n"
            f"Priority: {priority}\n"
            f"Assigned Department: {department}\n"
            f"Current Status: Pending"
        )

        # Notification for the administration.
        admin_message = (
            f"New campus complaint received.\n"
            f"Ticket ID: {ticket_id}\n"
            f"Issue: {description}\n"
            f"Location: {location}\n"
            f"Priority: {priority}\n"
            f"Assigned Department: {department}\n"
            f"Please review and take appropriate action."
        )

        notifications = {
            "student_notification": student_message,
            "admin_notification": admin_message,
            "delivery_status": "Prepared - Not Sent"
        }

        print(
            f"[Notification Agent] Notifications prepared for {ticket_id}",
            flush=True
        )

        return {
            "success": True,
            "agent": "Notification Agent",
            "notifications": notifications
        }

    except Exception as e:

        print(
            f"[Notification Agent ERROR] {type(e).__name__}: {e}",
            flush=True
        )

        return {
            "success": False,
            "agent": "Notification Agent",
            "error": str(e)
        }
