def clean_authors(authors: str) -> list:
    authors_raw = authors.split(";")
    authors_clean = [author.strip().title() for author in authors_raw if len(author.strip()) > 0]
    return authors_clean
