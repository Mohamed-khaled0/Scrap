import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# List of brands for Computing - Audio & Video Accessories
brands = [
    "2B", "A4tech", "Awei", "Axtel", "Boya", "Comica", "Corn", "Crash", "Dji", "Elgato",
    "FANTECH", "Forev", "GAMMA", "Generic", "Genius", "Gigamax", "Godox", "Golden King",
    "Goldenking", "Havit", "Hood", "HP", "HyperX", "Jabra", "Kisonili", "Kisonli", 
    "L'Avvento", "Lenovo", "Logitech", "Manhattan", "Marvo", "Maxi", "Media Tech", 
    "Meetion", "Microsoft", "Nacon", "Neutrik", "No Band", "Onikuma", "Ovleng", "P47", 
    "Philips", "Point", "Porodo", "Porsh Dob", "Powerology", "Rapoo", "Razer", "Recci", 
    "Redragon", "Rode", "Sades", "Saramonic", "Smile", "Soda", "SPEEDLINK", "Speed Link", 
    "Standard", "SUNWIND", "Techno Zone", "TERMINATOR", "UNIC", "XO", "XTRIKE ME", "ZERO"
]

# Base URL for Audio & Video Accessories with page placeholder
base_url = 'https://www.jumia.com.eg/computing-audio-video-accessories/?page={}'


# Function to extract product data
def get_product_data(product):
    # Extract product name
    name = product.find('h3', {'class': 'name'}).get_text(strip=True)

    # Extract price
    price = product.find('div', {'class': 'prc'}).get_text(strip=True)

    # Extract product link (adjusted to get correct href)
    link_tag = product.find('a', {'class': 'core'})
    link = 'https://www.jumia.com.eg' + link_tag['href'] if link_tag else None

    # Extract product image URL (adjusted to get data-src)
    img_tag = product.find('img', {'class': 'img'})
    img_url = img_tag['data-src'] if img_tag and 'data-src' in img_tag.attrs else None

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
        'Product Link': link,
        'Image URL': img_url,
        'Category': category
    }


# Function to scrape products from a given page
def scrape_page(page_num):
    url = base_url.format(page_num)
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
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
    file_path = 'C:/Users/dell/Desktop/audio_video_accessories_jumia.xlsx'  # Adjust the path
    df.to_excel(file_path, index=False, engine='openpyxl')
    print(f"Data saved to {file_path}")


# Main function to start scraping
def main():
    all_product_data = scrape_all_pages()
    if all_product_data:
        save_to_excel(all_product_data)


if __name__ == '__main__':
    main()