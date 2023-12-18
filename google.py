import requests
from bs4 import BeautifulSoup
from googlesearch import search
from tornado import ioloop, httpclient
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

            # Check if title tag exists
            title_tag = soup.title
            if title_tag:
                title = title_tag.text
                print(f"Domain: {domain} | Title: {title}")

                # Save the result to results.csv
                result = {
                    'Keyword': keyword,
                    'URL': url,
                    'Domain': domain,
                    'Title': title
                }
                return result

    return None

def scrape_domain(keyword):
    print(f"Searching for: {keyword}")
    results = []
    count = 0

    for url in search(keyword):
        print(f"Found URL: {url}")
        result = scrape_atsameip(url, keyword)
        if result:
            results.append(result)
            count += 1

        if count >= 5:
            break

        # Introduce a delay to avoid sending requests too quickly
        time.sleep(2)  # You can adjust the sleep time based on your needs

    return results


def main():
    file_path_keywords = 'katakunci.txt'
    file_path_domains = 'input.txt'

    keywords = get_keywords_from_file(file_path_keywords)
    all_results = []

    with open(file_path_domains, 'r', encoding='utf-8', errors='replace') as domains_file:
        domain_extensions = domains_file.read().splitlines()

    for keyword in keywords:
        for domain_extension in domain_extensions:
            keyword_with_extension = f"{keyword}{domain_extension}"
            results = scrape_domain(keyword_with_extension)
            all_results.extend(results)

    # Convert results to a DataFrame and save to CSV
    df = pd.DataFrame(all_results)
    df.to_csv('results.csv', index=False)

def async_main():
    file_path_keywords = 'katakunci.txt'
    file_path_domains = 'input.txt'

    keywords = get_keywords_from_file(file_path_keywords)
    all_results = []

    with open(file_path_domains, 'r', encoding='utf-8', errors='replace') as domains_file:
        domain_extensions = domains_file.read().splitlines()

    for keyword in keywords:
        for domain_extension in domain_extensions:
            keyword_with_extension = f"{keyword}{domain_extension}"
            results = ioloop.IOLoop.current().run_sync(lambda: scrape_domain(keyword_with_extension))
            all_results.extend(results)

    # Convert results to a DataFrame and save to CSV
    df = pd.DataFrame(all_results)
    df.to_csv('results.csv', index=False)

if __name__ == "__main__":
    main()
    # Uncomment line below to run the asynchronous version
    # async_main()
