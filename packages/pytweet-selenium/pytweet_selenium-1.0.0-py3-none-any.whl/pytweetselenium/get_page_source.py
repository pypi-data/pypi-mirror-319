from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time



def get_tweet_html(tweet_url, Debug):
    # Set up Chrome options
    options = Options()
    if not Debug:
        options.add_argument("--headless=new")  
        options.add_argument("--disable-gpu")

    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent detection as a bot

    # Add a modern User-Agent
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.204 Safari/537.36"
    )

    driver_path = "/opt/homebrew/bin/chromedriver"
    # Use your ChromeDriver path
    driver_service = Service(driver_path)

    # Start Chrome
    driver = webdriver.Chrome(service=driver_service, options=options)
    driver.get(tweet_url)
    time.sleep(2)  # Wait for the page to load
    try:
        # Output the entire page source
        page_source = driver.page_source
        # Save it as source.html
        if Debug:
            # Create a file with the page source
            with open("source.html", "w") as f:
                f.write(page_source)
            
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
    return page_source

