# Hospital and Doctor Information Scraper
This repository contains scripts and data for scraping hospital and doctor information from a specified healthcare website. The main goal is to automate the collection of detailed information about hospitals and doctors, including names, addresses, and descriptions, and to save this data for further analysis or integration into healthcare databases.


## Project Structure
 - hospital.py: Python script for scraping hospital information. It navigates through a list of hospitals, loads them dynamically by simulating page scrolls, and extracts details about each hospital.
 - doctors.py: Python script for scraping doctor information associated with the hospitals. It extracts details such as doctor names, specialties, and contact information.
 - hospital_data.csv: CSV file containing the scraped data from hospital.py. Columns include hospital name, address, and description.
 - doctors_data.csv: CSV file containing the scraped data from doctors.py. Columns include doctor name, specialty, hospital affiliation, and contact information.
