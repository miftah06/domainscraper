import requests
from bs4 import BeautifulSoup
import webbrowser
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

            # Save the result to results.csv
            result = {
                'Keyword': keyword,
                'URL': url,
                'Domain': domain,
                'Title': title
            }
            return result
    return None

def scrape_domain_bing(keyword):
    print(f"Searching for: {keyword}")
    results = []
    count = 0

    bing_search_url = f"https://www.bing.com/search?q={keyword}"
    webbrowser.open_new_tab(bing_search_url)

    # Introduce a delay for the user to interact with the search results
    time.sleep(10)

    # For demonstration purposes, manually enter the URLs you find in the Bing search results
    bing_results_urls = [
        "https://www.bing.com/search?form=&q={keyword}&form=QBLH&sp=-1&lq=0&pq=3d+modellin&sc=11-11&qs=n&sk=&cvid=E71E970AAEBC4214A9B168F894A9DD38&ghsh=0&ghacc=0&ghpl=",
        "https://www.bing.com/search?go=Search&q={keyword}&qs=ds&form=QBRE",
        "https://www.bing.com/search?q={keyword}&qs=n&form=QBRE&sp=-1&lq=0&pq=&sc=0-0&sk=&cvid=DBCB08AF48E84F03A9CAFC41F024E7F5&ghsh=0&ghacc=0&ghpl=",
    ]

    for url in bing_results_urls:
        print(f"Found URL: {url}")
        result = scrape_atsameip(url, keyword)
        if result:
            results.append(result)
            count += 1

        if count >= 5:
            break

    return results

def scrape_domain_yahoo(keyword):
    print(f"Searching for: {keyword}")
    results = []
    count = 0

    yahoo_search_url = f"https://search.yahoo.com/search?p={keyword}"
    webbrowser.open_new_tab(yahoo_search_url)

    # Introduce a delay for the user to interact with the search results
    time.sleep(10)

    # For demonstration purposes, manually enter the URLs you find in the Yahoo search results
    yahoo_results_urls = [
        "https://search.yahoo.com/search?p={keyword}&fr=yfp-t&fr2=p%3Afp%2Cm%3Asb&ei=UTF-8&fp=1",
        "https://search.yahoo.com/search;_ylt=AwrO6XPb0H9l_s0uQIhXNyoA;_ylc=X1MDMjc2NjY3OQRfcgMyBGZyA3lmcC10BGZyMgNzYi10b3AEZ3ByaWQDBG5fcnNsdAMwBG5fc3VnZwMwBG9yaWdpbgNzZWFyY2gueWFob28uY29tBHBvcwMwBHBxc3RyAwRwcXN0cmwDMARxc3RybAMxMgRxdWVyeQMzZCUyMG1vZGVsbGluZwR0X3N0bXADMTcwMjg3NTM1OA--?p={keyword}&fr2=sb-top&fr=yfp-t&fp=1",
        "https://search.yahoo.com/search;_ylt=Awrjah3f0H9lpr0ungVXNyoA;_ylc=X1MDMjc2NjY3OQRfcgMyBGZyA3lmcC10BGZyMgNzYi10b3AEZ3ByaWQDN2ZCYzdrb0xTWldscWJXSDRwYkdHQQRuX3JzbHQDMARuX3N1Z2cDMTAEb3JpZ2luA3NlYXJjaC55YWhvby5jb20EcG9zAzAEcHFzdHIDBHBxc3RybAMwBHFzdHJsAzEyBHF1ZXJ5AzNkJTIwbW9kZWxsaW5nBHRfc3RtcAMxNzAyODc1Mzc1?p={keyword}&fr2=sb-top&fr=yfp-t&fp=1",
    ]

    for url in yahoo_results_urls:
        print(f"Found URL: {url}")
        result = scrape_atsameip(url, keyword)
        if result:
            results.append(result)
            count += 1

        if count >= 5:
            break

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
            # Use Bing search
            results_bing = scrape_domain_bing(keyword_with_extension)
            all_results.extend(results_bing)

            # Use Yahoo search
            results_yahoo = scrape_domain_yahoo(keyword_with_extension)
            all_results.extend(results_yahoo)

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
            # Use Bing search asynchronously
            results_bing = ioloop.IOLoop.current().run_sync(lambda: scrape_domain_bing(keyword_with_extension))
            all_results.extend(results_bing)

            # Use Yahoo search asynchronously
            results_yahoo = ioloop.IOLoop.current().run_sync(lambda: scrape_domain_yahoo(keyword_with_extension))
            all_results.extend(results_yahoo)

    # Convert results to a DataFrame and save to CSV
    df = pd.DataFrame(all_results)
    df.to_csv('results.csv', index=False)

if __name__ == "__main__":
    main()
    # Uncomment line below to run the asynchronous version
    # async_main()
