import json
from pathlib import Path


def load_papers():

    data_file = Path(__file__).resolve().parent.parent / "data" / "papers.json"

    with open(data_file, "r", encoding="utf-8") as file:
        papers = json.load(file)

    return papers


def inspect_papers(papers):

    total_papers = len(papers)

    papers_with_abstracts = [
        paper for paper in papers
        if paper["abstract"]
    ]

    papers_without_abstracts = [
        paper for paper in papers
        if not paper["abstract"]
    ]

    paper_ids = [
        paper["openalex_id"]
        for paper in papers
    ]

    unique_ids = set(paper_ids)

    duplicate_count = len(paper_ids) - len(unique_ids)

    print("\nPAPERTRAIL — DATA INSPECTION")
    print("-" * 40)

    print(f"Total papers: {total_papers}")
    print(f"Papers with abstracts: {len(papers_with_abstracts)}")
    print(f"Papers without abstracts: {len(papers_without_abstracts)}")
    print(f"Duplicate records: {duplicate_count}")


if __name__ == "__main__":

    papers = load_papers()

    inspect_papers(papers)