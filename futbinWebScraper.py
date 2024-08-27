import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Set up the Chrome WebDriver
options = webdriver.ChromeOptions()
options.headless = True  # Run browser in headless mode
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

domain = 'https://www.futbin.com'
version = 24
page = 'playerGraph'

player_ids = {
    'Pierre-Emerick Aubameyang': 188567,
    'Robert Lewandowski': 188545,
    'Antoine Griezmann': 194765,
    'David Alaba': 197445,
    'Paulo Dybala': 211110
}

def fetch_prices():
    ret_val = {}
    
    for name, player_id in player_ids.items():
        url = f"{domain}/{version}/{page}?type=daily_graph&year={version}&player={player_id}"
        browser.get(url)

        # Get the page source
        content = browser.page_source
        
        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')
        
        # Look for the JSON data directly in the script tags or elsewhere
        script_tag = soup.find('script', string=lambda t: 'var playerGraph' in t if t else False)
        
        if script_tag:
            # Extract the JSON part from the script tag
            json_text = script_tag.string.split('=', 1)[1].strip().strip(';')
            data = json.loads(json_text)

            # Assuming the JSON structure contains 'ps' which is a list of timestamp-price pairs
            prices = data.get('ps', [])
            parsed_prices = {pair[0]: pair[1] for pair in prices}
            ret_val[name] = parsed_prices
        else:
            ret_val[name] = 'JSON data not found'

    return ret_val

if __name__ == "__main__":
    prices = fetch_prices()
    print(prices)

# Close the browser
browser.quit()
