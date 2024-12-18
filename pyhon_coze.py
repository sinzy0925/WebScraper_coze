import re
from urllib.parse import urljoin
from typing import List, Dict
from requests_async import get

async def extract_and_normalize_urls(markdown: str, html: str) -> List[str]:
    url_pattern = re.compile(r'(https?://[^\s]+|href="([^"]+)"|src="([^"]+)")')
    urls = set()
    exclude_extensions = ('.js', '.css', '.svg', '.png')

    for match in url_pattern.findall(markdown + " " + html):
        for url in match:
            if url and not any(ext in url for ext in exclude_extensions):
                # Normalize URLs
                if url.startswith('href="') or url.startswith('src="'):
                    url = url[6:-1]
                urls.add(url)

    # Sort URLs and handle duplicates
    sorted_urls = sorted(urls, key=lambda x: x.strip('href="').strip('src="'))
    final_urls = []
    seen = set()
    for url in sorted_urls:
        normalized_url = url.strip('href="').strip('src="')
        if normalized_url not in seen:
            seen.add(normalized_url)
            final_urls.append(url)

    return final_urls

async def main(args: Args) -> Output:
    params = args.params
    base_url = params['url']

    urls = await extract_and_normalize_urls(params['markdown'], params['urls'])

    # Construct the output object
    ret: Output = {
        "markdown": params['markdown'],  # Return markdown as is
        "urls": urls,  # List of unique, sorted URLs
        "url": base_url,  # Return the input URL
    }
    return ret
