import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

def find_urls(base_url, visited_urls=None):
    if visited_urls is None:
        visited_urls = set()

    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            domain = urlparse(base_url).scheme + '://' + urlparse(base_url).netloc

            # Extract all anchor tags
            anchor_tags = soup.find_all('a', href=True)

            # Combine relative URLs with the base domain
            urls = [urljoin(domain, anchor['href']) for anchor in anchor_tags]

            # Filter out already visited URLs
            new_urls = [url for url in urls if url not in visited_urls]

            # Print or store the new URLs
            for new_url in new_urls:
                print(new_url)

            # Update visited URLs set
            visited_urls.update(new_urls)

            # Recursively find URLs for each new URL
            for url in new_urls:
                find_urls(url, visited_urls)
        else:
            print(f"Error: Unable to fetch content from {base_url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    website_url = input("Enter the website URL: ")
    find_urls(website_url)
