import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# List of brands for accessories and cables
brands = [
    '2B', 'Acefast', 'Adam Elements', 'Anker', 'Apple', 'Aspor', 'Aukey', 'Baseus', 'Blitz', 
    'Borofone', 'Buddy', 'Cable', 'Celebrat', 'Choetech', 'Corn', 'Coteetci', 'Dadu', 'Dausen', 'Devia', 
    'Earldom', 'Eloroby', 'EMB', 'Energiemax', 'Energizer', 'Eugizmo', 'Genai', 'General', 'Generic', 
    'Gerlax', 'GFUZ', 'GravaStar', 'Havit', 'Hoco', 'HP', 'Iconix', 'Iconz', 'Infinix', 'Inkax', 'Jellico', 
    'JOYROOM', 'JSAUX', 'K3', 'Kingleen', 'Konfulon', "L'Avvento", 'Lanex', 'Ldino', 'Ldnio', 'Lightning', 
    'Linein', 'Majentik', 'Manhattan', 'Mcdodo', 'Mcgear', 'Mi', 'Momax', 'MOMO', 'Moxom', 'Nillkin', 'Nubia', 
    'Odoyo', 'Onten', 'Oraimo', 'Orimo', 'Over', 'Pavareal', 'Powerline', 'Proda', 'Promate', 'Ravpower', 
    'realme', 'Recci', 'Remax', 'RockRose', 'Romoss', 'Samsung', 'Sanyon', 'Sendem', 'Shark', 'Sikenai', 
    'Smart Gate', 'Soda', 'Strong', 'super touch', 'Tronsmart', 'Ugreen', 'Vidivi', 'Vidvie', 'WiWU', 'WK Design', 
    'wopow', 'WUW', 'X-Plus', 'X-Scoot', 'XIAOMI', 'XO', 'Yesido'
]

# Base URL for accessories and cables with page placeholder
base_url = 'https://www.jumia.com.eg/mobile-phone-accessories-cables/?page={}'

# Function to get product data from each product div
def get_product_data(product):
    name = product.find('h3', {'class': 'name'}).get_text(strip=True)
    
    # Extracting product price
    price = product.find('div', {'class': 'prc'}).get_text(strip=True)
    
    # Extract image link (adjusted to get data-src)
    img_tag = product.find('img')
    image_url = img_tag['data-src'] if img_tag and 'data-src' in img_tag.attrs else None
    
    # Extract product link (adjusted to get correct href)
    link_tag = product.find('a', {'class': 'core'})
    product_link = 'https://www.jumia.com.eg' + link_tag['href'] if link_tag else None
    
    # Determine the category (brand) based on product name
    category = None
    for brand in brands:
        if brand.lower() in name.lower():
            category = brand
            break
    if not category:
        category = 'Other'  # For all other brands

    return {
        'Product Name': name,
        'Price': price,
        'Category': category,
        'Image URL': image_url,  # Added image URL
        'Product Link': product_link  # Added product link
    }

# Function to scrape products from a given page
def scrape_page(page_num):
    url = base_url.format(page_num)  # Format the base URL with the current page number
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all product entries on the page (use 'prd _fb' class for product)
        products = soup.find_all('article', {'class': 'prd _fb col c-prd'})  # Adjust to find 'article' tags
        
        if not products:
            return None

        page_data = []
        for product in products:
            product_data = get_product_data(product)
            page_data.append(product_data)
        return page_data
    else:
        print(f"Failed to retrieve page {page_num}.")
        return None

# Function to scrape all pages
def scrape_all_pages():
    all_product_data = []
    page_num = 1

    while True:
        print(f"Scraping page {page_num}...")
        page_data = scrape_page(page_num)
        
        if not page_data:
            print(f"No products found on page {page_num}. Stopping scraping.")
            break
        
        all_product_data.extend(page_data)
        page_num += 1
        time.sleep(2)  # Add a delay to avoid overloading the server
    
    return all_product_data

# Function to save data to an Excel file
def save_to_excel(data):
    df = pd.DataFrame(data)
    file_path = 'C:/Users/dell/Desktop/accessories_and_cables_jumia_products.xlsx'  # Adjust the path
    df.to_excel(file_path, index=False, engine='openpyxl')
    print(f"Data saved to {file_path}")

# Main function to start the scraping process
def main():
    all_product_data = scrape_all_pages()  # Scrape all pages
    if all_product_data:
        save_to_excel(all_product_data)  # Save data to an Excel file

if __name__ == '__main__':
    main()
