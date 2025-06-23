# Amazon Smartphone Scraper

This project provides a Python script to automatically scrape details of smartphones under ₹20,000 from Amazon India. Using a combination of Selenium and BeautifulSoup, the script collects product names, prices, ratings, review counts, and links, and saves the data to a CSV file for further analysis.

---

### **Features**

- **Automated Browsing:** Uses Selenium WebDriver to navigate Amazon search result pages and individual product pages for accurate data extraction.
- **Data Extraction:** Captures key product details including:
  - Name
  - Discounted Price
  - Original Price (MRP)
  - Number of Reviews
  - Product Rating
  - Product Link
- **Smartphone Filtering:** Ensures only actual smartphones (not accessories or unrelated items) are included by checking product details on each page.
- **Price Filtering:** Only includes smartphones with a discounted price below ₹20,000.
- **Output:** Saves the scraped data into a CSV file (`smartphones_under_20k.csv`) for easy access and analysis.

---

### **How to Use**

1. **Clone the Repository**

   ```bash
   git clone 'url'
   cd 'repo-name'
   ```

2. **Install Dependencies**

   Ensure you have Python 3.x. Install required packages:

   ```bash
   pip install selenium beautifulsoup4 requests pandas
   or
   pip install -r requirements.txt
   ```

   You will also need the [Chrome WebDriver](https://chromedriver.chromium.org/) installed and available in your PATH.

3. **Run the Script**

   ```bash
   python scraping.py
   ```

   The script will:
   - Scrape the first two pages of Amazon search results for smartphones under ₹20,000.
   - Visit each product link to verify it is a smartphone.
   - Save the results to `smartphones_under_20k.csv`.

---

### **Output Example**

The output CSV will have columns:

| Name | Price | Mrp | Reviews | Rating | Link |
|------|-------|-----|---------|--------|------|

---

### **Notes & Limitations**

- The script is designed for Amazon India and may require adjustments for other regions.
- Amazon may block automated requests; use responsibly and consider adding delays or using proxies if scraping at scale.
- For best results, ensure your Chrome browser and ChromeDriver versions match.

---

**This project is ideal for anyone looking to automate the collection of smartphone data for price comparison, market analysis, or research.**

---

# You might have a question, How can I customize this scraper to target different product categories or sites? Here's how.

---

## Customizing the Scraper for Different Product Categories or Sites

To adapt your Amazon smartphone scraper for other product categories or entirely different websites, consider the following steps and best practices:

---

**1. Change the Search URL or Category**

- For a different product category on Amazon, update the search URL to target your desired category (e.g., laptops, headphones).
- Example: Replace the smartphone search URL with the category or keyword relevant to your target products.

**2. Update Element Selectors**

- Product details (name, price, rating, etc.) may use different HTML tags or classes in other categories or sites.
- Inspect the target page using browser developer tools to identify the correct selectors for each data point.
- Update your script’s BeautifulSoup or Selenium selectors accordingly[1].

**3. Handle Product Variations**

- Some categories have product variations (size, color, etc.). You may need to iterate through these options to capture all variants[2].

**4. Scraping Other Sites**

- For different e-commerce sites, you’ll need to:
  - Update the base URL and navigation logic.
  - Change all selectors to match the new site’s HTML structure.
  - Handle site-specific features like pagination, lazy loading, or login requirements[3].
- Consider modularizing your code: separate the scraping logic for each site/category into different functions or classes for easier maintenance[3].

**5. Make Your Scraper Robust**

- Websites often change their layout, which can break your scraper. To make it more resilient:
  - Store selectors in a configuration file for easy updates[4].
  - Write tests to alert you when scraping fails due to layout changes[4].
  - Use XPath or more flexible CSS selectors when possible.

**6. Respect Site Policies**

- Always check the site’s robots.txt and terms of service before scraping.
- Add delays between requests to avoid overloading servers[5].
- Consider using public APIs if available, as they are more stable and reliable than scraping HTML[5].

---

### Example: Changing Category on Amazon

```python
# Change the search URL for laptops under ₹30,000
search_url = "https://www.amazon.in/s?k=laptops+under+30000"
```
Update all selectors (e.g., for product name, price) based on the new category’s HTML structure.

---

### Example: Scraping a Different Site

- Identify the product listing and details page structure.
- Update navigation and data extraction logic to match the new site.
- Modularize your code for each site to keep it maintainable[3].

---

### Useful Tips

- Modularize scraping logic for each category/site.
- Store selectors/configurations externally for easy updates[4].
- Use proxies and delays to avoid being blocked, especially when scraping multiple sites at scale[6].
- Regularly maintain and test your scraper, as web layouts change frequently[4][3].

---

By following these steps, you can efficiently adapt your scraper to target new product categories or different e-commerce sites with minimal code changes.
