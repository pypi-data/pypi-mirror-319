"""

--------------------------------------------------------------------------------
from .imports import *

# Importing custom libraries hack
path = "your_path"
sys.path.insert(0, path)


--------------------------------------------------------------------------------
Linux:

du <path> -h # Find how much space is used by a file or folder
df -h # Find disk usage-overall
ls <pat> | wc -l # Count the number of files in a folder

tmux attach -t <session_name> # Attach to a session
Ctrl-b + [ # tmux copy mode, enter q to exit
Ctrl-b + d # Detach from a session
--------------------------------------------------------------------------------
Jupyter:

# matplotlib retina mode
%config InlineBackend.figure_format = 'retina'

# Capture the output of a cell
%%capture
--------------------------------------------------------------------------------
Better randomness:
from Crypto.Random import random # pip install pycryptodome

# drop in replacement for random.randint, random.random, random.randrange, etc
--------------------------------------------------------------------------------

Selenuim Web Scraping
```
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver
driver = webdriver.Chrome()  # Replace with the path to your ChromeDriver if necessary
wait = WebDriverWait(driver, 10)  # Set an explicit wait timeout

try:
    # Open the target website
    url = "https://example.com"  # Replace with the target URL
    driver.get(url)

    # Example: Locate a search bar and input text
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))  # Replace 'q' with the element's name
    search_box.send_keys("Selenium Web Scraping")
    search_box.send_keys(Keys.RETURN)

    # Example: Wait for search results and extract titles
    results = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".result-title")))  # Replace with the CSS selector for your target
    for index, result in enumerate(results):
        print(f"{index + 1}. {result.text}")

    # Example: Clicking a link
    if results:
        results[0].click()
        time.sleep(5)  # Allow time for the page to load
        print("Clicked the first result.")

finally:
    # Close the browser
    driver.quit()
```


"""

__all__ = []


