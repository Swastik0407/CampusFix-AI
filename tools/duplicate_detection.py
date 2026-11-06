
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from backend.database import get_all_complaints


def detect_duplicates(
    description: str,
    location: str,
    threshold: float = 0.40
):

    try:
        existing_complaints = get_all_complaints()

        if not existing_complaints:
            return {
                "success": True,
                "duplicate_found": False,
                "message": "No previous complaints found.",
                "similar_complaints": []
            }

        # Combine description and location for comparison
        new_complaint = f"{description} {location}"

        existing_texts = [
            f"{complaint['description']} {complaint['location']}"
            for complaint in existing_complaints
        ]

        # Combine new and existing complaints
        all_texts = existing_texts + [new_complaint]

        # Convert text into numerical vectors
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        vectors = vectorizer.fit_transform(all_texts)

        # Calculate similarity scores
        scores = cosine_similarity(
            vectors[-1],
            vectors[:-1]
        ).flatten()

        similar_complaints = []

        for index, score in enumerate(scores):

            if score >= threshold:

                complaint = existing_complaints[index]

                similar_complaints.append({
                    "ticket_id": complaint["ticket_id"],
                    "description": complaint["description"],
                    "location": complaint["location"],
                    "status": complaint["status"],
                    "similarity": round(float(score) * 100, 2)
                })

        # Sort by highest similarity
        similar_complaints.sort(
            key=lambda x: x["similarity"],
            reverse=True
        )

        return {
            "success": True,
            "duplicate_found": len(similar_complaints) > 0,
            "message": (
                "Potential duplicate complaints found."
                if similar_complaints
                else "No similar complaints found."
            ),
            "similar_complaints": similar_complaints
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e),
            "similar_complaints": []
        }
