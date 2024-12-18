from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
            startups.append(f"Startup Name: {heading.text}\nDescription: {description.text}")
            startups.append("—------------------------------------------------------------------------------")
    else:
        print(f"Mismatch in counts: {len(headings)} headings and {len(descriptions)} descriptions.")

    # Save to txt file
    if startups:
        with open("startup.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(startups))
        print("Data saved to startup.txt")
    else:
        print("No data found.")

finally:
    # Close the WebDriver
    driver.quit()
