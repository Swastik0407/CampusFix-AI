
from agents.database_agent import fetch_all_tickets


def retrieve_ticket(ticket_id: str = None):

    try:
        # Retrieve all tickets from the database.
        result = fetch_all_tickets()

        if not result["success"]:
            return result

        tickets = result["tickets"]

        # If no tickets exist.
        if not tickets:
            return {
                "success": True,
                "agent": "Retrieval Agent",
                "message": "No complaints found.",
                "tickets": []
            }

        # If a specific ticket ID is provided.
        if ticket_id:

            matching_ticket = None

            for ticket in tickets:
                if ticket["ticket_id"] == ticket_id:
                    matching_ticket = ticket
                    break

            if matching_ticket is None:
                return {
                    "success": False,
                    "agent": "Retrieval Agent",
                    "error": "Ticket not found."
                }

            return {
                "success": True,
                "agent": "Retrieval Agent",
                "ticket": matching_ticket
            }

        # If no ticket ID is provided, return all tickets.
        return {
            "success": True,
            "agent": "Retrieval Agent",
            "tickets": tickets,
            "total_tickets": len(tickets)
        }

    except Exception as e:

        print(
            f"[Retrieval Agent ERROR] {type(e).__name__}: {e}",
            flush=True
        )

        return {
            "success": False,
            "agent": "Retrieval Agent",
            "error": str(e)
        }
