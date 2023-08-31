def clean_authors(authors: str) -> list:
    """
    Returns list of author names stripped of whitespace and capitalized
    """
    authors_raw = authors.split(";")
    authors_clean = [
        author.strip().title() for author in authors_raw if len(author.strip()) > 0
    ]
    return authors_clean
