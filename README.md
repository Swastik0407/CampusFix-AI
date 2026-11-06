# CampusFix AI – Intelligent Campus Complaint Management System

CampusFix AI is an AI-powered campus operations platform designed to simplify and improve the way students report problems within an educational institution.

It uses multiple specialized AI agents to analyze complaints, identify their category and urgency, assign them to the appropriate department, generate complaint tickets, and store them for administrative review.

The goal is to make campus issue reporting faster, more organized, and more transparent.

## Problem Statement

In many educational institutions, students report problems such as electrical failures, plumbing issues, damaged classroom equipment, and maintenance requests through informal communication channels.

This often leads to:
- Delayed complaint resolution.
- Difficulty identifying urgent issues.
- Complaints being sent to the wrong departments.
- Duplicate complaints.
- Lack of centralized complaint tracking.

CampusFix AI addresses these challenges through an intelligent, centralized complaint management system.

## Key Features

- **AI-powered complaint analysis:** Understands student complaints and identifies the issue category, location, and summary.
- **Priority assessment:** Classifies complaints as High, Medium, or Low priority.
- **Department routing:** Recommends the appropriate department for handling each complaint.
- **Duplicate detection:** Uses TF-IDF-based similarity analysis to identify potentially repeated complaints.
- **Automatic ticket generation:** Generates a unique complaint ID for every submitted complaint.
- **Centralized database:** Stores complaint information using SQLite.
- **Notification preparation:** Generates notification messages for students and administrators.
- **Admin dashboard:** Displays complaint statistics and allows administrators to update complaint statuses.
- **Ticket retrieval:** Allows stored complaints to be retrieved using their ticket IDs.

## Multi-Agent Architecture

CampusFix AI follows a modular multi-agent architecture in which individual agents perform specialized tasks.

### AI Agents

| Agent | Responsibility |
|---|---|
| Triage Agent | Analyzes complaints and identifies category, summary, location, and issue type. |
| Priority Agent | Determines complaint urgency and recommends an action. |
| Routing Agent | Selects the appropriate department and responsible team. |
| Ticket Agent | Generates unique complaint ticket IDs. |
| Database Agent | Stores and retrieves complaint records. |
| Notification Agent | Prepares notification messages for students and administrators. |
| Retrieval Agent | Retrieves individual or all complaint records. |

### Supporting Tools

- Complaint validation
- Ticket validation
- TF-IDF-based duplicate detection
- Notification message preparation
- Ticket creation and retrieval

### Complaint Processing Workflow

1. A student submits a complaint through the web interface.
2. The backend validates the complaint.
3. The duplicate detection tool checks for similar existing complaints.
4. The Triage Agent analyzes the complaint.
5. The Priority Agent assigns an urgency level.
6. The Routing Agent recommends the responsible department.
7. The Ticket Agent generates a unique ticket ID.
8. The Database Agent stores the complaint.
9. The Notification Agent prepares notification messages.
10. The administrator reviews complaints and updates their statuses.

## Technology Stack

**Backend**
- Python
- FastAPI
- Pydantic
- SQLite

**Artificial Intelligence**
- Google Gemini API
- Multi-agent architecture
- Scikit-learn
- TF-IDF similarity analysis

**Frontend**
- HTML
- CSS
- JavaScript

**Development Tools**
- Visual Studio Code
- Git and GitHub
- Uvicorn

## Project Structure

```text
CampusFix1/
│
├── agents/
│   ├── triage_agent.py
│   ├── priority_agent.py
│   ├── routing_agent.py
│   ├── ticket_agent.py
│   ├── notification_agent.py
│   ├── database_agent.py
│   └── retrieval_agent.py
│
├── tools/
│   ├── complaint_tools.py
│   ├── ticket_tools.py
│   ├── notification_tools.py
│   └── duplicate_detection.py
│
├── backend/
│   ├── main.py
│   ├── database.py
│   └── orchestrator.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── data/
├── config/
│   └── settings.py
│
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd CampusFix1
```

Replace the repository URL with your actual GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Add your Gemini API configuration:

```env
GEMINI_API_KEY=your_actual_gemini_api_key
GEMINI_MODEL=your_gemini_model_name
DATABASE_PATH=data/campusfix.db
```

Use a valid Gemini API key and a model name supported by your API account.

**Important:** Never upload your `.env` file or expose your API key publicly.

### 5. Start the Backend

From the project root directory, run:

```bash
python -m uvicorn backend.main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Start the Frontend

Open a second terminal from the project root and run:

```bash
python -m http.server 5500
```

Open the frontend in your browser:

```text
http://127.0.0.1:5500/frontend/
```

Keep both servers running while using the application.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Backend welcome endpoint |
| GET | `/health` | Checks backend health |
| POST | `/api/complaints` | Submits and processes a complaint |
| GET | `/api/complaints` | Retrieves all complaints |
| GET | `/api/complaints/{ticket_id}` | Retrieves a specific complaint |
| PUT | `/api/complaints/{ticket_id}/status` | Updates complaint status |

## Complaint Statuses

The admin dashboard supports the following statuses:

- Pending
- Approved
- Rejected
- In Progress
- Resolved

## Current Limitations

- A working Gemini API key and available API quota are required for AI-powered analysis.
- Notification messages are currently prepared but are not automatically sent through email or SMS.
- Duplicate detection identifies potentially similar complaints; it does not automatically reject them.
- The current admin interface does not implement authentication or role-based access control.
- This version is an MVP/prototype and requires additional security, testing, and deployment work before production use.

## Future Enhancements

- Email and SMS notification integration.
- Secure administrator authentication.
- Role-based access control.
- Real-time complaint status notifications.
- Advanced duplicate detection.
- Complaint analytics and reporting.
- Cloud database and deployment.
- Resolution-time tracking and performance analytics.

## Project Objective

CampusFix AI aims to transform traditional campus complaint handling into a more intelligent, structured, and transparent process by combining AI-powered analysis, specialized agents, and centralized complaint management.

**Built as an AI-powered campus operations project.**