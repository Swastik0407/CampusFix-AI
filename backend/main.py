
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from config.settings import APP_NAME, APP_VERSION
from backend.database import initialize_database, get_connection
from backend.orchestrator import process_complaint
from agents.retrieval_agent import retrieve_ticket


# Initialize database
initialize_database()


# Initialize FastAPI
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="AI-powered Campus Operations Management System"
)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Complaint request model
class ComplaintRequest(BaseModel):
    description: str
    location: str
    student_name: str | None = None


# Admin status update model
class StatusUpdateRequest(BaseModel):
    status: str


# Allowed complaint statuses
ALLOWED_STATUSES = [
    "Pending",
    "Approved",
    "Rejected",
    "In Progress",
    "Resolved"
]


# Home endpoint
@app.get("/")
def home():
    return {
        "project": APP_NAME,
        "version": APP_VERSION,
        "status": "online",
        "message": "Welcome to CampusFix AI"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": APP_NAME
    }


# Submit and process a complaint using all agents
@app.post("/api/complaints")
def submit_complaint(complaint: ComplaintRequest):

    result = process_complaint(
        description=complaint.description,
        location=complaint.location,
        student_name=complaint.student_name
    )

    if not result["success"]:

        if result.get("stage") == "Validation":
            raise HTTPException(
                status_code=400,
                detail=result
            )

        raise HTTPException(
            status_code=500,
            detail=result
        )

    return result


# Retrieve all complaints
@app.get("/api/complaints")
def get_complaints():

    result = retrieve_ticket()

    if not result["success"]:
        raise HTTPException(
            status_code=500,
            detail=result
        )

    return result


# Retrieve an individual complaint using ticket ID
@app.get("/api/complaints/{ticket_id}")
def get_complaint(ticket_id: str):

    result = retrieve_ticket(ticket_id)

    if not result["success"]:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found"
        )

    return result


# Admin: Approve, reject, or update complaint status
@app.put("/api/complaints/{ticket_id}/status")
def update_complaint_status(
    ticket_id: str,
    request: StatusUpdateRequest
):

    new_status = request.status.strip().title()

    if new_status not in ALLOWED_STATUSES:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid status",
                "allowed_statuses": ALLOWED_STATUSES
            }
        )

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE complaints
            SET status = ?
            WHERE ticket_id = ?
            """,
            (new_status, ticket_id)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Complaint ticket not found"
            )

        conn.commit()

        return {
            "success": True,
            "ticket_id": ticket_id,
            "status": new_status,
            "message": f"Complaint status updated to {new_status}"
        }

    except HTTPException:
        raise

    except Exception as error:
        conn.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

    finally:
        conn.close()
