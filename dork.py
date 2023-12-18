import requests
from bs4 import BeautifulSoup
import os
import socket
import pandas as pd
import time

# Set timeout for requests
timeout = 5
socket.setdefaulttimeout(timeout)

def fetch_url(url):
    try:
        response = requests.get(url, timeout=timeout)
        return response
    except requests.RequestException as e:
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
            soup = BeautifulSoup(html_content.text, 'html.parser')
            title = soup.title.text
            print(f"Domain: {domain} | Title: {title}")

            # Save the result to results.csv
            result = {
                'Keyword': keyword,
                'URL': url,
                'Domain': domain,
                'Title': title,
                'Status Code': html_content.status_code
            }
            return result
    return None

def scrape_domain(keyword):
    print(f"Searching for: {keyword}")
    results = []
    count = 0

    bing_search_url = f"https://www.bing.com/search?q={keyword}"
    yahoo_search_url = f"https://search.yahoo.com/search?p={keyword}"

    for search_url in [bing_search_url, yahoo_search_url]:
        try:
            html_content = fetch_url(search_url)
            if html_content:
                soup = BeautifulSoup(html_content.text, 'html.parser')
                search_results = soup.select('h2 a[href^="http"]')

                for result in search_results:
                    url = result['href']
                    print(f"Found URL: {url}")
                    scraped_result = scrape_atsameip(url, keyword)
                    if scraped_result:
                        results.append(scraped_result)
                        count += 1

                    if count >= 5:
                        break
        except Exception as e:
            print(f"Error during scraping: {e}")

    return results

def main():
    file_path_keywords = 'katakunci.txt'
    all_results = []

    keywords = get_keywords_from_file(file_path_keywords)

    for keyword in keywords:
        results = scrape_domain(keyword)
        all_results.extend(results)

    # Convert results to a DataFrame and save to CSV
    df = pd.DataFrame(all_results)
    df.to_csv('results_dorking.csv', index=False)

if __name__ == "__main__":
    main()
