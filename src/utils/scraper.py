import argparse
import requests
import os
from urllib.parse import urlparse
from collections import defaultdict
from bs4 import BeautifulSoup
import json

parser = argparse.ArgumentParser()
parser.add_argument("--site", type=str, required=True)
parser.add_argument("--depth", type=int, default=3)


def cleanUrl(url: str):
    return url.replace("https://", "").replace("/", "-").replace(".", "_")


def get_response_and_save(url: str):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        response = requests.get(url, headers=headers)
        if not os.path.exists("./scrape"):
            os.mkdir("./scrape")
        parsedUrl = cleanUrl(url)
        with open("./scrape/" + parsedUrl + ".html", "wb") as f:
            f.write(response.content)
        return response
    except:
        return None


def scrape_links(
    scheme: str,
    origin: str,
    path: str,
    depth=3,
    sitemap: dict = defaultdict(lambda: ""),
):
    siteUrl = scheme + "://" + origin + path
    cleanedUrl = cleanUrl(siteUrl)

    if depth < 0:
        return
    if sitemap[cleanedUrl] != "":
        return

    sitemap[cleanedUrl] = siteUrl
    response, file_path = get_response_and_save(siteUrl)
    if response is not None:  
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a")

        for link in links:
            href = urlparse(link.get("href"))
            if (href.netloc != origin and href.netloc != "") or (
                href.scheme != "" and href.scheme != "https"
            ):
                continue
            scrape_links(
                href.scheme or "https",
                href.netloc or origin,
                href.path,
                depth=depth - 1,
                sitemap=sitemap,
            )
    
    # Create a list of dictionaries containing cleaned URL and file path
    sitemap_list = [{"cleaned_url": k, "file_path": v} for k, v in sitemap.items()]
    return sitemap, sitemap_list

def scrape_site(site, depth):
    url = urlparse(site)
    sitemap, sitemap_list = scrape_links(url.scheme, url.netloc, url.path, depth=depth)
    with open("./scrape/sitemap.json", "w") as f:
        f.write(json.dumps(sitemap))
    return sitemap, sitemap_list

