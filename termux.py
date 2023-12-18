from appium import webdriver
from bs4 import BeautifulSoup
import requests
import os
import pandas as pd
import time

# Patch socket module in Termux
try:
    import android
    android_version = android.sys.version
    if '5.0' in android_version:
        import monkey
        monkey.patch_socket()
except ImportError:
    pass

# Set timeout for requests
timeout = 5
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
socket.setdefaulttimeout(timeout)

def fetch_url(url):
    try:
        response = requests.get(url, timeout=timeout, verify=False)
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def setup_appium():
    desired_caps = {
        'platformName': 'Android',
        'platformVersion': '12',
        'deviceName': 'OPPO A53',
        'appPackage': 'com.brave.browser',
        'appActivity': '.MainActivity',
        'noReset': True,
    }

    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver


    driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
    return driver

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

def scrape_domain(keyword, driver):
    print(f"Searching for: {keyword}")
    results = []
    count = 0

    google_search_url = f"https://www.google.com/search?q={keyword}"

    try:
        driver.get(google_search_url)
        time.sleep(2)  # Wait for the page to load (you can adjust the time based on your needs)

        # Extract search results using Appium
        search_results = driver.find_elements_by_xpath('//div[@class="tF2Cxc"]//a[@href]')

        for result in search_results:
            url = result.get_attribute("href")
            if url and url.startswith('http'):
                print(f"Found URL: {url}")
                scraped_result = scrape_atsameip(url, keyword)
                if scraped_result:
                    results.append(scraped_result)
                    count += 1

                if count >= 5:
                    break
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        return results

def main():
    file_path_keywords = 'katakunci.txt'
    file_path_domains = 'input.txt'

    keywords = get_keywords_from_file(file_path_keywords)
    all_results = []

    # Set up Appium driver
    driver = setup_appium()

    with open(file_path_domains, 'r', encoding='utf-8', errors='replace') as domains_file:
        domain_extensions = domains_file.read().splitlines()

    for keyword in keywords:
        for domain_extension in domain_extensions:
            keyword_with_extension = f"{keyword}{domain_extension}"
            results = scrape_domain(keyword_with_extension, driver)
            all_results.extend(results)

    # Convert results to a DataFrame and save to CSV
    df = pd.DataFrame(all_results)
    df.to_csv('results.csv', index=False)

    # Quit the Appium driver
    driver.quit()

if __name__ == "__main__":
    main()
