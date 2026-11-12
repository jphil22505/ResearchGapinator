
import requests
import json
from pathlib import Path

OPENALEX_URL = "https://api.openalex.org/works"


def reconstruct_abstract(inverted_index):
    """
    Reconstruct a readable abstract from OpenAlex's
    inverted-index representation.
    """

    if not inverted_index:
        return None

    words = {}

    for word, positions in inverted_index.items():
        for position in positions:
            words[position] = word

    ordered_words = [
        words[position]
        for position in sorted(words)
    ]

    return " ".join(ordered_words)


def search_papers(query, limit=5):

    params = {
        "search": query,
        "per_page": limit,
        "select": (
            "id,doi,title,publication_year,"
            "authorships,cited_by_count,"
            "abstract_inverted_index"
        )
    }

    try:
        response = requests.get(
            OPENALEX_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        papers = []

        for item in data["results"]:

            authors = [
                author["author"]["display_name"]
                for author in item.get("authorships", [])
            ]

            abstract = reconstruct_abstract(
                item.get("abstract_inverted_index")
            )

            paper = {
                "openalex_id": item.get("id"),
                "title": item.get("title"),
                "year": item.get("publication_year"),
                "doi": item.get("doi"),
                "citations": item.get("cited_by_count"),
                "authors": authors,
                "abstract": abstract
            }

            papers.append(paper)

        return papers

    except requests.exceptions.RequestException as error:

        print(f"API request failed: {error}")
        return []


if __name__ == "__main__":

    query = "graph neural networks"

    results = search_papers(query, limit=5)
    
    # Determine the project's data directory
    data_dir = Path(__file__).resolve().parent.parent / "data"

    # Create the directory if it doesn't exist
    data_dir.mkdir(parents=True, exist_ok=True)

    # Define where the results will be stored
    output_file = data_dir / "papers.json"

    # Save the complete research records
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(
            results,
            file,
            ensure_ascii=False,
            indent=4
        )

    print(f"\nComplete dataset saved to: {output_file}")

    print(f"\nFound {len(results)} papers:\n")

    for index, paper in enumerate(results, start=1):

        print("=" * 70)

        print(f"\nPaper {index}")
        print(f"Title: {paper['title']}")
        print(f"Year: {paper['year']}")
        print(f"Authors: {', '.join(paper['authors'][:5])}")
        print(f"Citations: {paper['citations']}")
        print(f"DOI: {paper['doi']}")

        print("\nAbstract:")

        if paper["abstract"]:
            print(paper["abstract"][:600])
        else:
            print("Abstract unavailable.")

        print()
