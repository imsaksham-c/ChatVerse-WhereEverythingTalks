from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup

def get_links(url):
    """
    Retrieve all the links from a given URL.

    Args:
    url (str): The URL to scrape.

    Returns:
    list: A list of links found on the webpage.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [link.get('href') for link in soup.find_all('a', href=True)]
            return links
        else:
            print(f"Failed to retrieve page {url}: {response.status_code}")
            return []
    except Exception as e:
        print(f"An error occurred while retrieving page {url}: {str(e)}")
        return []

def normalize_url(url):
    """
    Normalize a URL by removing 'www.' from the netloc and trailing slashes from the path.

    Args:
    url (str): The URL to normalize.

    Returns:
    str: The normalized URL.
    """
    parsed_url = urlparse(url)
    scheme = parsed_url.scheme.lower()
    netloc = parsed_url.netloc.lower().replace('www.', '')  # Remove 'www.' if present
    path = parsed_url.path.rstrip('/')  # Remove trailing slashes
    normalized_url = f"{scheme}://{netloc}{path}"
    return normalized_url

def filter_links(links, base_domain):
    """
    Filter out links based on the base domain and media file extensions.

    Args:
    links (list): A list of links to be filtered.
    base_domain (str): The base domain of the website.

    Returns:
    list: A list of filtered links.
    """
    valid_links = []
    for link in links:
        if link is None:
            continue
        parsed_url = urlparse(link)
        normalized_url = normalize_url(link)
        if base_domain in parsed_url.netloc.lower() or base_domain in parsed_url.path.lower():
            if not any(normalized_url.lower().endswith(ext) for ext in ('.jpg', '.png', '.gif', '.mp4', '.avi', '.mp3')):
                valid_links.append(normalized_url)
    return valid_links

def scrape_website(url, base_domain, depth, visited=None):
    """
    Scrape a website recursively up to a specified depth and collect all the links.

    Args:
    url (str): The URL of the website to scrape.
    base_domain (str): The base domain of the website.
    depth (int): The depth to scrape links.
    visited (set, optional): A set to store visited URLs to avoid duplicates.

    Returns:
    list: A list of unique links found on the website up to the specified depth.
    """
    if visited is None:
        visited = set()

    if depth == 0 or url in visited:
        return [url]

    visited.add(url)

    links = get_links(url)
    filtered_links = filter_links(links, base_domain)

    collected_links = [url]
    for link in filtered_links:
        absolute_url = urljoin(url, link)
        collected_links.extend(scrape_website(absolute_url, base_domain, depth - 1, visited))

    return list(set(collected_links))


def scrape_urls(website, depth=0):
    """
    Scrape URLs from a website up to a specified depth.

    Args:
    website (str): The URL of the website to scrape.
    depth (int): The depth to scrape links.

    Returns:
    list: A list of URLs found on the website up to the specified depth.
    """
    base_domain = urlparse(website).netloc.split('.')[0]
    links = scrape_website(website, base_domain, depth)
    return links