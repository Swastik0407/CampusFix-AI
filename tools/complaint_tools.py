
def validate_complaint(description: str, location: str):

    errors = []

    if not description or not description.strip():
        errors.append("Complaint description is required.")

    if not location or not location.strip():
        errors.append("Complaint location is required.")

    if description and len(description.strip()) < 10:
        errors.append(
            "Complaint description must contain at least 10 characters."
        )

    if description and len(description) > 2000:
        errors.append(
            "Complaint description cannot exceed 2000 characters."
        )

    if location and len(location) > 200:
        errors.append(
            "Location cannot exceed 200 characters."
        )

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def prepare_complaint(description: str, location: str):

    validation = validate_complaint(description, location)

    if not validation["valid"]:
        return {
            "success": False,
            "errors": validation["errors"]
        }

    return {
        "success": True,
        "complaint": {
            "description": description.strip(),
            "location": location.strip()
        }
    }
