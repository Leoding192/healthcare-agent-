"""
Healthcare Data Ingestion & Classification Agent
Data Source : arXiv API
LLM Backend : Groq (llama-3.3-70b-versatile) — free tier
"""

from fetcher import fetch_all_papers
from classifier import is_healthcare, classify_specialty
from storage import save_paper, discard_paper, logger


def run():
    logger.info("=" * 50)
    logger.info("Agent started")

    # Step 1: Fetch papers
    papers = fetch_all_papers(max_per_query=5)
    logger.info(f"Fetched {len(papers)} papers — starting classification...")

    stats = {"total": len(papers), "healthcare": 0, "discarded": 0, "specialties": {}}

    for i, paper in enumerate(papers, 1):
        print(f"\n[{i}/{len(papers)}] {paper['title'][:70]}...")

        # Step 2: Check if paper is healthcare-related
        is_health, reason = is_healthcare(paper)

        if not is_health:
            discard_paper(paper, reason)
            stats["discarded"] += 1
            continue

        # Step 3: Classify into a medical specialty
        specialty = classify_specialty(paper)
        save_paper(paper, specialty)

        stats["healthcare"] += 1
        stats["specialties"][specialty] = stats["specialties"].get(specialty, 0) + 1

    # Print summary
    logger.info("=" * 50)
    logger.info(f"Run complete | Total: {stats['total']} | Healthcare: {stats['healthcare']} | Discarded: {stats['discarded']}")
    for sp, count in stats["specialties"].items():
        logger.info(f"  {sp}: {count} paper(s)")
    logger.info("=" * 50)


if __name__ == "__main__":
    run()
