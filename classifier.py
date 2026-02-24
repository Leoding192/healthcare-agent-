from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

SPECIALTIES = ["cardiology", "dermatology", "anesthesiology", "other"]

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def _ask(prompt: str) -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=50,
    )
    return response.choices[0].message.content.strip().lower()


def is_healthcare(paper: dict) -> tuple[bool, str]:
    """Determine whether a paper is related to healthcare or medicine.
    Returns (is_healthcare: bool, reason: str).
    """
    prompt = f"""Is this academic paper related to healthcare, medicine, or clinical science?
Title: {paper['title']}
Abstract: {paper['summary'][:300]}

Reply with ONLY: yes or no, then a comma, then a one-sentence reason.
Example: yes, this paper discusses cardiac surgery techniques."""

    result = _ask(prompt)

    if result.startswith("yes"):
        reason = result[4:].strip() if len(result) > 4 else "healthcare related"
        return True, reason
    else:
        reason = result[3:].strip() if len(result) > 3 else "not healthcare related"
        return False, reason


def classify_specialty(paper: dict) -> str:
    """Classify a confirmed healthcare paper into a medical specialty."""
    prompt = f"""Classify this medical paper into ONE specialty:
- cardiology (heart, cardiovascular)
- dermatology (skin, dermal)
- anesthesiology (anesthesia, pain management, sedation)
- other (anything else)

Title: {paper['title']}
Abstract: {paper['summary'][:300]}

Reply with ONLY one word: cardiology, dermatology, anesthesiology, or other"""

    result = _ask(prompt)

    for specialty in SPECIALTIES:
        if specialty in result:
            return specialty
    return "other"
