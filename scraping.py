from bs4 import BeautifulSoup
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Setup Selenium WebDriver
options = Options()
#options.add_argument("--headless")
options.add_argument('--enable-gpu')
#options.add_argument("--disable-gpu")
options.add_argument('--no-sandbox')
options.add_argument("--enable-unsafe-swiftshader")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress logs

driver = webdriver.Chrome(options=options)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept-Language': 'en-US,en;q=0.5'
}
base_url = "https://www.amazon.in/s?k=mobile+phone+under+20000&ref=nb_sb_noss"

# Fetch search results page using requests
def fetch_page(URL):
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {URL}")
        return None
    return BeautifulSoup(response.content, 'html.parser')

# Extract functions
def get_product_name(product):
    name = product.find('h2')
    return name.get_text(strip=True) if name else 'Name Not Found'

def get_discount_price(product):
    disc = product.find('span', class_='a-price-whole')
    return disc.get_text(strip=True).replace(',', '') if disc else 'Price Not Found'

def get_original_price(product):
    orig = product.find('span', class_='a-price a-text-price')
    if orig:
        offscreen = orig.find('span', class_='a-offscreen')
        if offscreen:
          return offscreen.get_text(strip=True).replace(',', '').replace('₹', '')
    return 'Original Price Not Found'

def get_review_count(product):
    # Try common review count classes
    review =product.find('span', class_='a-size-base s-underline-text') or \
            product.find('span', class_='a-size-small puis-normal-weight-text s-underline-text')  
    if review:
        text = review.get_text(strip=True)
        # Filter out unwanted cases like "Let us know" or "M.R.P"
        if "let us know" in text.lower() or "m.r.p" in text.lower():
            return "No Reviews"
        return text.replace('(', '').replace(')', '')
    
    return 'No Reviews'


def get_product_rating(product):
    rating_tag = product.find('span', class_='a-icon-alt')
    return rating_tag.get_text(strip=True) if rating_tag else 'Rating Not Found'

def get_product_link(product):
    link = product.find('a', class_='a-link-normal s-no-outline', href=True)
    return 'https://www.amazon.in' + link['href'] if link else 'Link Not Found'

# Check if product is a smartphone
def is_product(link):
    try:
        driver.get(link)
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, 'table'))
            )
        except TimeoutException:
            print(f"[Timeout] Table not loaded for {link}")
            return False
        # Expanding "Item details"
        try:
            expand_btn = driver.find_element(By.XPATH, "//span[contains(text(),'Item details')]")
            driver.execute_script("arguments[0].click();", expand_btn)
            time.sleep(1)
        except:
            pass
        #valid and invalid keywords
        valid_types = ['smartphone', 'smart phone', 'mobile phone', 'cellular phone', 'android phone', 'mobile', 'smart handset', 'cell phone']
        invalid_types = ['holder', 'stand', 'cover', 'case']

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        tables = soup.find_all('table')

        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                th = row.find('th')
                td = row.find('td')
                if th and td:
                    label = th.text.strip().lower()
                    value = td.text.strip().lower()

                    if 'item type' in label or 'generic name' in label:
                        # Split by '||' and check each item
                        types = [v.strip() for v in value.split('||')]

                        for t in types:
                            if any(valid in t for valid in valid_types) and not any(invalid in t for invalid in invalid_types):
                                return True
    except Exception as e:
        print(f"[Error checking {link}]: {e}")
    return False


# Parse all product listings on a page
def get_product(soup):
    product_data = []
    product_block = soup.find_all('div', {'data-component-type': 's-search-result'})
    for product in product_block:
        name = get_product_name(product)
        discount = get_discount_price(product)
        mrp = get_original_price(product)
        reviews = get_review_count(product)
        rating = get_product_rating(product)
        link = get_product_link(product)

        try:
            discount_val = int(discount.replace(',', '').replace('₹', ''))
            if discount_val >= 20000:
                continue
        except:
            continue

        if link != 'Link Not Found':
            print(f"Checking: {name}")
            if is_product(link):
                product_data.append({
                    'Name': name,
                    'Price': discount,
                    'Mrp': mrp,
                    'Reviews': reviews,
                    'Rating': rating,
                    'Link': link
                })
            else:
                print("Not a smartphone")
    return product_data

# Main scraping loop
def scrape(URL, pages):
    all_products = []
    for page in range(1, pages + 1):
        print(f"\nScraping Page {page}")
        soup = fetch_page(f"{URL}&page={page}")
        if soup:
            products = get_product(soup)
            all_products.extend(products)
        time.sleep(1)
    return all_products

# Start scraping
results = scrape(base_url, pages=2)
driver.quit()

# Save results
df = pd.DataFrame(results)
df.to_csv('smartphones_under_20k.csv', index=False, encoding='utf-8')
print('File created and dataset is saved.')
