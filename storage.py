import json
import logging
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")

# Configure audit logger — writes to both console and file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "audit.log"), encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("healthcare-agent")


def save_paper(paper: dict, specialty: str):
    """Save a classified paper to its specialty folder as JSON."""
    folder = os.path.join(DATA_DIR, specialty)
    os.makedirs(folder, exist_ok=True)

    safe_id = paper["id"].split("/")[-1].replace("/", "_")
    filepath = os.path.join(folder, f"{safe_id}.json")

    paper["classified_at"] = datetime.utcnow().isoformat()
    paper["specialty"] = specialty

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(paper, f, ensure_ascii=False, indent=2)

    logger.info(f"SAVED | specialty={specialty} | id={paper['id']} | title={paper['title'][:60]}")


def discard_paper(paper: dict, reason: str):
    """Save a discarded (non-healthcare) paper with its discard reason."""
    folder = os.path.join(DATA_DIR, "discarded")
    os.makedirs(folder, exist_ok=True)

    safe_id = paper["id"].split("/")[-1].replace("/", "_")
    filepath = os.path.join(folder, f"{safe_id}.json")

    paper["discarded_at"] = datetime.utcnow().isoformat()
    paper["discard_reason"] = reason

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(paper, f, ensure_ascii=False, indent=2)

    logger.info(f"DISCARDED | id={paper['id']} | reason={reason} | title={paper['title'][:60]}")
