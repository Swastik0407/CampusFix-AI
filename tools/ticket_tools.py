
def validate_ticket(ticket: dict):

    required_fields = [
        "ticket_id",
        "description",
        "location",
        "category",
        "priority",
        "department"
    ]

    missing_fields = []

    for field in required_fields:
        if not ticket.get(field):
            missing_fields.append(field)

    if ticket.get("priority") not in ["High", "Medium", "Low"]:
        missing_fields.append("valid priority")

    if missing_fields:
        return {
            "valid": False,
            "message": "Ticket validation failed.",
            "missing_fields": missing_fields
        }

    return {
        "valid": True,
        "message": "Ticket is valid."
    }


def generate_ticket_summary(ticket: dict):

    validation = validate_ticket(ticket)

    if not validation["valid"]:
        return {
            "success": False,
            "validation": validation
        }

    summary = {
        "ticket_id": ticket["ticket_id"],
        "issue": ticket["description"],
        "location": ticket["location"],
        "category": ticket["category"],
        "priority": ticket["priority"],
        "department": ticket["department"],
        "status": ticket.get("status", "Pending")
    }

    return {
        "success": True,
        "summary": summary
    }
