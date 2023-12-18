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

def get_domain_suffixes(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            domain_suffixes = file.read().splitlines()
        return domain_suffixes
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
        if domain.lower() == 'yahoo.com':
            return None

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

def scrape_domain(keyword, domain_suffix):
    print(f"Searching for: {keyword}")
    results = []
    count = 0

    bing_search_url = f"https://www.bing.com/search?q={keyword} {domain_suffix}"

    try:
        html_content = fetch_url(bing_search_url)
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
    file_path_input = 'input.txt'
    all_results = []
    all_domains = set()

    keywords = get_keywords_from_file(file_path_keywords)
    domain_suffixes = get_domain_suffixes(file_path_input)

    for keyword in keywords:
        for domain_suffix in domain_suffixes:
            keyword_with_extension = f"{keyword} {domain_suffix}"
            results = scrape_domain(keyword_with_extension, domain_suffix)
            all_results.extend(results)
            for result in results:
                domain = result.get('Domain')
                if domain:
                    all_domains.add(domain)

    # Save domains to domains.txt
    with open('domains.txt', 'w', encoding='utf-8') as domains_file:
        for domain in all_domains:
            domains_file.write(f"{domain}\n")

    # Convert results to a DataFrame and save to CSV
    df = pd.DataFrame(all_results)
    df.to_csv('results_dork.csv', index=False)

if __name__ == "__main__":
    main()
