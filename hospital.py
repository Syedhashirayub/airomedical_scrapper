from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import os
import time
from fake_useragent import UserAgent
from swiftshadow.classes import Proxy  

def load_full_page(driver, timeout=60):
    scroll_pause_time = 1
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    while True:
        driver.execute_script(f"window.scrollTo(0, {screen_height}*{i});")
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if (screen_height * i) > scroll_height:
            break
        timeout -= scroll_pause_time
        if timeout <= 0:
            break

def append_to_csv(row, filename):
    
    if not os.path.exists(filename):
        pd.DataFrame([row]).to_csv(filename, mode='w', index=False)
    else:
        pd.DataFrame([row]).to_csv(filename, mode='a', index=False, header=False)

def scrape_hospital_data(proxy):
    # Initialize WebDriver with Proxy
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    user_agent = UserAgent()
    random_user_agent = user_agent.random
    chrome_options.add_argument(f'user-agent={random_user_agent}')
    chrome_options.add_argument(f'--proxy-server={proxy["https"]}')
    driver = webdriver.Chrome(options=chrome_options)


    driver.get("https://airomedical.com/hospitals")
    load_full_page(driver)

    # File where the data will be saved
    output_file = "/Volumes/Hardisc/lawsikho/output/hospital_data.csv"

    # Check if output file exists and create it with headers if not
    if not os.path.exists(output_file):
        pd.DataFrame(columns=["Hospital Name", "Address", "About the Hospital"]).to_csv(output_file, index=False)

    # Retrieve the hospital URLs 
    hospital_urls = [element.get_attribute('href') for element in driver.find_elements(By.CSS_SELECTOR, "div.HospitalCard_title__Tw4ZU a")]
    

    for url in hospital_urls:
        driver.get(url)
        time.sleep(4)  # Adjust based on your connection speed

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        name_element = soup.find("h1", class_="MainInfo_titleName__rhrVM")
        about_element = soup.find("div", class_="AboutBlock_message__oiMr8")
        address_element = soup.find("p", class_="LocationSection_address__zq2y7")

        # Using .get_text(strip=True) if element is found, otherwise use a default value
        name = name_element.get_text(strip=True) if name_element else ''
        about = about_element.get_text(strip=True) if about_element else ''
        address = address_element.get_text(strip=True) if address_element else ''

        row = {
            "Hospital Name": name,
            "Address": address,
            "About the Hospital": about
        }
        
        # Append each hospital's data to the CSV file
        append_to_csv(row, output_file)

    print("Data scraping completed and saved to hospital_data.csv")
    driver.quit()

# Proxy Setup
num_proxy = 15
swift = Proxy(countries=['IN', 'PK', 'BD', 'MY', 'TH', 'KR', 'AE', 'DE'], protocol='https', autoRotate=True, maxProxies=num_proxy, cacheFolder='/Volumes/Hardisc/lawsikho/cachefolder')

# Get a proxy from swift
proxy = swift.proxy()

# Run the scraper with the proxy
scrape_hospital_data(proxy)
