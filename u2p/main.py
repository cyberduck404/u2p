#!/usr/bin/python3
import os, sys
from urllib.parse import urlparse, parse_qs, urlencode


placeholder = 'FUZZ'
HARDCODED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".svg", ".json", ".css", ".js", ".webp", ".woff", ".woff2", ".eot", ".ttf", ".otf", ".mp4", ".txt"]

def has_extension(url, extensions):
    parsed_url = urlparse(url)
    path = parsed_url.path
    extension = os.path.splitext(path)[1].lower()

    return extension in extensions

def clean_url(url):
    parsed = urlparse(url)

    if (parsed.port == 80 and parsed.scheme == "http") or (parsed.port == 443 and parsed.scheme == "https"):
        parsed = parsed._replace(netloc=parsed.netloc.rsplit(":", 1)[0])

    return parsed.geturl()

def main():
    if sys.stdin.isatty():
        sys.exit(0)
    extensions = HARDCODED_EXTENSIONS
    urls = []
    for line in sys.stdin.readlines():
        url = line.strip('\n')
        if '?' not in url:
            continue
        urls.append(url)

    cleaned_urls = set()
    for url in urls:
        cleaned_url = clean_url(url)
        if not has_extension(cleaned_url, extensions):
            parsed_url = urlparse(cleaned_url)
            query_params = parse_qs(parsed_url.query)
            cleaned_params = {key: placeholder for key in query_params}
            cleaned_query = urlencode(cleaned_params, doseq=True)
            cleaned_url = parsed_url._replace(query=cleaned_query).geturl()
            cleaned_urls.add(cleaned_url)
    cleaned_urls = list(cleaned_urls)
    for url in cleaned_urls:
        if '?' in url:
            sys.stdout.write(f'{url}\n')


if __name__ == '__main__':
    main()