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

def scrape_doctor_data(proxy):
    # Initialize WebDriver with Proxy
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    user_agent = UserAgent()
    random_user_agent = user_agent.random
    chrome_options.add_argument(f'user-agent={random_user_agent}')
    chrome_options.add_argument(f'--proxy-server={proxy["https"]}')
    driver = webdriver.Chrome(options=chrome_options)



    driver.get("https://airomedical.com/doctors")
    load_full_page(driver)

    # File where the data will be saved
    output_file = "/Volumes/Hardisc/lawsikho/output/doctors_data.csv"

    # Check if output file exists and create it with headers if not
    if not os.path.exists(output_file):
        pd.DataFrame(columns=["Doctor Name", "About the Doctor"]).to_csv(output_file, index=False)

    # Retrieve the hospital URLs 
    doctors_urls = [element.get_attribute('href') for element in driver.find_elements(By.CSS_SELECTOR, "div.DoctorCard_title__m0_Dy a")]
    

    for url in doctors_urls:
        driver.get(url)
        time.sleep(4)  # Adjust based on your connection speed

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        name_element = soup.find("h1", class_="MainInfoSection_name__WV8ab")
        about_element = soup.find("div", class_="AboutBlock_message__oiMr8")
        

        # Using .get_text(strip=True) if element is found, otherwise use a default value
        name = name_element.get_text(strip=True) if name_element else ''
        about = about_element.get_text(strip=True) if about_element else ''
        

        row = {
            "Doctor Name": name,
            "About the Doctor": about
        }
        
        # Append each doctor's data to the CSV file
        append_to_csv(row, output_file)

    print("Data scraping completed and saved to doctor_data.csv")
    driver.quit()

# Proxy Setup
num_proxy = 15
swift = Proxy(countries=['IN', 'PK', 'BD', 'MY', 'TH', 'KR', 'AE', 'DE'], protocol='https', autoRotate=True, maxProxies=num_proxy, cacheFolder='/Volumes/Hardisc/lawsikho/cachefolder')

# Get a proxy from swift
proxy = swift.proxy()

# Run the scraper with the proxy
scrape_doctor_data(proxy)