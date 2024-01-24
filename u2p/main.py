#!/usr/bin/python3
import os, sys
import argparse
import requests
from urllib.parse import urlparse, parse_qs, urlencode
from threading import Thread


HARDCODED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".pdf", ".svg", ".json", ".css", ".js", ".webp", ".woff", ".woff2", ".eot", ".ttf", ".otf", ".mp4", ".txt"]

p = argparse.ArgumentParser()
p.add_argument('-p', '--payload', required=True, help='Specify payload then we roll')
p.add_argument('-k', '--keyword', default='FUZZ', help='URL keyword, default is FUZZ')
# p.add_argument('-d', '--url-dir', help='Specify URL Directory')
p.add_argument('-mt', '--match-content-type', help='Matched content-type')
p.add_argument('-mc', '--match-status-code', type=int, help='Matched status code')
p.add_argument('-mt', '--match-text', help='Matched text')
# p.add_argument('-mr', '--match-regex', help='Matched regex')
p.add_argument('-x', '--proxy', help='Specify your proxy, like http://127.0.0.1:8080')
p.add_argument('-t', '--threads', type=int, default=64, help='Max Concurrency')
args = p.parse_args()

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

def battering_ram(url, payload, headers=None, proxies=None):
    headers = headers if headers else dict()  # todo://
    proxies = proxies if proxies else dict()
    url = url.replace(args.keyword, payload)
    try:
        r = requests.get(url, headers=headers, proxies=proxies, verify=False)
    except requests.exceptions.RequestException as e:
        return
    if args.match_content_type and (args.match_content_type not in r.headers['Content-Type']):
        return
    if args.match_status_code and (args.match_status_code != r.status_code):
        return
    if args.match_text and (args.match_text not in r.text):
        return
    # todo://args.match_regex
    sys.stdout.write(f'{url}\n')

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
            cleaned_params = {key: args.keyword for key in query_params}
            cleaned_query = urlencode(cleaned_params, doseq=True)
            cleaned_url = parsed_url._replace(query=cleaned_query).geturl()
            cleaned_urls.add(cleaned_url)
    cleaned_urls = list(cleaned_urls)
    ts = []
    for url in cleaned_urls:
        if '?' in url:
            t = Thread(target=battering_ram, args=(url, args.payload,))


if __name__ == '__main__':
    main()