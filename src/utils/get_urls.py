import requests
from urllib.parse import urlparse, urljoin
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
            return []
    except Exception as e:
        return []

def filter_links(links, main_domain):
    """
    Filter out links that do not belong to the main domain and exclude media files.

    Args:
    links (list): A list of links to be filtered.
    main_domain (str): The main domain of the website.

    Returns:
    list: A list of filtered links.
    """
    valid_links = []
    for link in links:
        if link is None:
            continue
        parsed_url = urlparse(link)
        if parsed_url.scheme not in ('http', 'https'):
            continue
        if parsed_url.netloc != main_domain:
            continue
        if parsed_url.path.lower().endswith(('.jpg', '.png', '.gif', '.mp4', '.avi', '.mp3')):
            continue
        valid_links.append(link)
    return valid_links

def scrape_website(url, depth, main_domain, visited=None):
    """
    Scrape the website for links up to a specified depth.

    Args:
    url (str): The URL of the website to scrape.
    depth (int): The depth to scrape links.
    main_domain (str): The main domain of the website.
    visited (set, optional): A set to store visited URLs to avoid duplicates.

    Returns:
    list: A list of links found on the website up to the specified depth.
    """
    if visited is None:
        visited = set()

    if depth == 0:
        return [url]

    if url in visited:
        return []

    visited.add(url)

    links = get_links(url)
    filtered_links = filter_links(links, main_domain)

    collected_links = [url]
    if depth > 1:
        for link in filtered_links:
            absolute_url = urljoin(url, link)
            collected_links.extend(scrape_website(absolute_url, depth - 1, main_domain, visited))

    return collected_links

def scrape_urls(website, depth=2):
    """
    Scrape URLs from a website up to a specified depth.

    Args:
    website (str): The URL of the website to scrape.
    depth (int): The depth to scrape links.

    Returns:
    list: A list of URLs found on the website up to the specified depth.
    """
    main_domain = urlparse(website).netloc
    links = scrape_website(website, depth, main_domain)
    return links
