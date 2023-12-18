import requests
from bs4 import BeautifulSoup
import webbrowser  # Import the webbrowser module
import os
import socket
import pandas as pd
import numpy as np
import time  # Import the time module

# Set timeout for requests
timeout = 5
socket.setdefaulttimeout(timeout)

def fetch_url(url):
    try:
        response = requests.get(url, timeout=timeout)
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

async def async_fetch_url(url):
    try:
        http_client = httpclient.AsyncHTTPClient()
        response = await http_client.fetch(url)
        return response.body.decode('utf-8')
    except httpclient.HTTPError as e:
        print(f"Error fetching {url}: {e}")
        return None

def get_keywords_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            keywords = file.read().splitlines()
        return keywords
    else:
        print(f"File not found: {file_path}")
        return []

def extract_domain(url):
    try:
        domain = url.split('//')[1].split('/')[0]
        return domain
    except IndexError:
        print(f"Error extracting domain from URL: {url}")
        return None

def scrape_atsameip(url, keyword):
    domain = extract_domain(url)
    if domain:
        base_url = f"https://www.isitdownrightnow.com/{domain}.html"
        html_content = fetch_url(base_url)

        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            title = soup.title.text
            print(f"Domain: {domain} | Title: {title}")

            # Save the result to results_dorking.csv
            result = {
                'Keyword': keyword,
                'URL': url,
                'Domain': domain,
                'Title': title
            }
            return result
    return None

def scrape_domain_google(keyword):
    print(f"Searching for: {keyword}")
    results = []
    count = 0

    google_search_url = f"https://duckduckgo.com/?t=h_&q={keyword}"
    
    # Open the Google search page in a new tab
    webbrowser.open_new_tab(google_search_url)

    # Introduce a delay for the user to interact with the search results
    time.sleep(10)

    # For demonstration purposes, manually enter the URLs you find in the Google search results
    google_results_urls = [
        f"https://{keyword}.zendesk.com",
        f"https://{keyword}",
    ]

    for url in google_results_urls:
        print(f"Found URL: {url}")
        result = scrape_atsameip(url, keyword)
        if result:
            results.append(result)
            count += 1

        if count >= 5:
            break

    return results

def main():
    file_path_keywords = 'domain.txt'
    file_path_domains = 'input.txt'

    keywords = get_keywords_from_file(file_path_keywords)
    all_results = []

    with open(file_path_domains, 'r', encoding='utf-8', errors='replace') as domains_file:
        domain_extensions = domains_file.read().splitlines()

    for keyword in keywords:
        for domain_extension in domain_extensions:
            keyword_with_extension = f"{keyword}{domain_extension}"
            # Use Google search
            results_google = scrape_domain_google(keyword_with_extension)
            all_results.extend(results_google)

    # Convert results to a DataFrame and save to CSV
    df = pd.DataFrame(all_results)
    df.to_csv('results_dorking.csv', index=False)

def async_main():
    file_path_keywords = 'domain.txt'
    file_path_domains = 'input.txt'

    keywords = get_keywords_from_file(file_path_keywords)
    all_results = []

    with open(file_path_domains, 'r', encoding='utf-8', errors='replace') as domains_file:
        domain_extensions = domains_file.read().splitlines()

    for keyword in keywords:
        for domain_extension in domain_extensions:
            keyword_with_extension = f"{keyword}{domain_extension}"
            # Use Google search asynchronously
            results_google = ioloop.IOLoop.current().run_sync(lambda: scrape_domain_google(keyword_with_extension))
            all_results.extend(results_google)

    # Convert results to a DataFrame and save to CSV
    df = pd.DataFrame(all_results)
    df.to_csv('results_dorking.csv', index=False)

if __name__ == "__main__":
    main()
    # Uncomment line below to run the asynchronous version
    # async_main()
