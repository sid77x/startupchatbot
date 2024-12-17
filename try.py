from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Configure Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Use Selenium Manager to initialize the driver
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the URL
    driver.get("https://mutbimanipal.org/startup/incubated")
    
    # Wait for the elements to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h5.sub-heading")))

    # Scrape data
    startups = []
    
    # Get all headings and descriptions
    headings = driver.find_elements(By.CSS_SELECTOR, "h5.sub-heading")
    descriptions = driver.find_elements(By.CSS_SELECTOR, "p.card-text")
    
    # Ensure the number of headings and descriptions match
    if len(headings) == len(descriptions):
        for heading, description in zip(headings, descriptions):
            startups.append({
                "Startup Name": heading.text,
                "Description": description.text
            })
            # Add a separator after each startup
            startups.append({
                "Startup Name": "_______________________",
                "Description": "_______________________"
            })
    else:
        print(f"Mismatch in counts: {len(headings)} headings and {len(descriptions)} descriptions.")

    # Save to CSV
    if startups:
        df = pd.DataFrame(startups)
        df.to_csv("incubated_startups.csv", index=False)
        print("Data saved to incubated_startups.csv")
    else:
        print("No data found.")

finally:
    # Close the WebDriver
    driver.quit()
