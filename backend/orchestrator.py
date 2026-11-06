
import time

from agents.triage_agent import analyze_complaint
from agents.priority_agent import assess_priority
from agents.routing_agent import route_complaint
from agents.ticket_agent import generate_ticket
from agents.database_agent import save_ticket
from agents.notification_agent import prepare_notification

from tools.complaint_tools import prepare_complaint
from tools.duplicate_detection import detect_duplicates
from tools.ticket_tools import validate_ticket


def process_complaint(
    description: str,
    location: str,
    student_name: str = None
):
    total_start = time.time()

    def log_stage(message):
        elapsed = time.time() - total_start
        print(f"[CampusFix | {elapsed:.2f}s] {message}", flush=True)

    try:
        # STEP 1: Validation
        log_stage("STEP 1: Validating complaint...")
        validation = prepare_complaint(description, location)

        if not validation["success"]:
            return {
                "success": False,
                "stage": "Validation",
                "errors": validation["errors"]
            }

        complaint = validation["complaint"]
        description = complaint["description"]
        location = complaint["location"]

        log_stage("Validation completed.")

        # STEP 2: Duplicate Detection
        log_stage("STEP 2: Checking duplicates...")
        duplicate_result = detect_duplicates(
            description=description,
            location=location
        )

        if not duplicate_result["success"]:
            return {
                "success": False,
                "stage": "Duplicate Detection",
                "error": duplicate_result["error"]
            }

        log_stage("Duplicate detection completed.")

        # STEP 3: Triage
        log_stage("STEP 3: Starting Triage Agent...")
        triage_result = analyze_complaint(
            description=description,
            location=location
        )

        if not triage_result["success"]:
            return triage_result

        triage = triage_result["analysis"]
        log_stage("Triage Agent completed.")

        # STEP 4: Priority
        log_stage("STEP 4: Starting Priority Agent...")
        priority_result = assess_priority(
            description=description,
            category=triage["category"],
            location=location
        )

        if not priority_result["success"]:
            return priority_result

        priority = priority_result["assessment"]
        log_stage("Priority Agent completed.")

        # STEP 5: Routing
        log_stage("STEP 5: Starting Routing Agent...")
        routing_result = route_complaint(
            description=description,
            category=triage["category"],
            priority=priority["priority"]
        )

        if not routing_result["success"]:
            return routing_result

        routing = routing_result["routing"]
        log_stage("Routing Agent completed.")

        # STEP 6: Ticket Generation
        log_stage("STEP 6: Generating ticket...")
        ticket_result = generate_ticket(
            description=description,
            location=location,
            category=triage["category"],
            priority=priority["priority"],
            department=routing["department"],
            student_name=student_name
        )

        if not ticket_result["success"]:
            return ticket_result

        ticket = ticket_result["ticket"]
        log_stage("Ticket generated.")

        # STEP 7: Ticket Validation
        log_stage("STEP 7: Validating generated ticket...")
        ticket_validation = validate_ticket(ticket)

        if not ticket_validation["valid"]:
            return {
                "success": False,
                "stage": "Ticket Validation",
                "error": ticket_validation
            }

        # STEP 8: Database
        log_stage("STEP 8: Saving ticket to database...")
        database_result = save_ticket(ticket)

        if not database_result["success"]:
            return database_result

        log_stage("Database save completed.")

        # STEP 9: Notifications
        log_stage("STEP 9: Preparing notifications...")
        notification_result = prepare_notification(ticket)

        if not notification_result["success"]:
            return notification_result

        log_stage("Notifications prepared.")

        # STEP 10: Final response
        log_stage("ALL STEPS COMPLETED.")

        return {
            "success": True,
            "message": "Complaint processed successfully",
            "triage": triage,
            "priority_assessment": priority,
            "department_routing": routing,
            "duplicate_check": {
                "duplicate_found": duplicate_result["duplicate_found"],
                "similar_complaints": duplicate_result["similar_complaints"],
                "admin_review_required": duplicate_result["duplicate_found"]
            },
            "ticket": ticket,
            "database": database_result,
            "notifications": notification_result["notifications"]
        }

    except Exception as e:
        log_stage(f"UNEXPECTED ERROR: {str(e)}")
        return {
            "success": False,
            "stage": "Orchestration",
            "error": str(e)
        }
