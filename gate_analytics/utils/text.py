def deduplicate_slashes(url: str) -> str:
    while "//" in url:
        url = url.replace("//", "/")
    url = url.replace(":/", "://")
    return url
