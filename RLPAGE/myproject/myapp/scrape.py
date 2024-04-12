import requests
from bs4 import BeautifulSoup
import time
import random

def scrape_amazon_product(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data from Amazon. Status code: {response.status_code}")

        time.sleep(random.uniform(1, 5))  # Introduce random delay

        soup = BeautifulSoup(response.content, 'html.parser')

        price_element = soup.find('span', {'class': 'a-price-whole'})
        if not price_element:
            return None  # Return None if price element is not found

        price = price_element.text.strip()

        rating_element = soup.find('span', {'class': 'a-icon-alt'})
        if not rating_element:
            return None  # Return None if price element is not found

        rating = rating_element.text.strip()

        
        stack_element = soup.find('span', {'class': 'a-size-medium a-color-success'})
        if not stack_element:
            return None  # Return None if price element is not found

        stack = stack_element.text.strip()


        # image_element = soup.find('div', {'id': 'imgTagWrapperId'})
        # if not image_element or not image_element.img:
        #     raise ValueError("Image element not found on the page")
        # image_url = image_element.img['src']

        # product_element = soup.find('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
        # if not image_element or not image_element.img:
        #     raise ValueError("Image element not found on the page")
        # product_url = product_element.url['href']

        brand_element = soup.find('td', {'class': 'a-span3'})
        if not brand_element:
            return None  # Return None if price element is not found

        brand = brand_element.text.strip()

        value_element = soup.find('td', {'class': 'a-span9'})
        if not value_element:
            return None  # Return None if price element is not found
        value = value_element.text.strip()

        model_element = soup.find('tr', {'class': 'a-spacing-small po-model_name'})
        if not model_element:
            return None  # Return None if price element is not found

        model = model_element.text.strip()

        value2_element = soup.find('tr', {'class': 'a-spacing-small po-model_name'})
        if not value2_element:
            return None  # Return None if price element is not found

        value2 = value2_element.text.strip()

        network_element = soup.find('tr', {'class': 'a-spacing-small po-wireless_provider'})
        if not network_element:
            return None  # Return None if price element is not found

        network = network_element.text.strip()

        value3_element = soup.find('td', {'class': 'a-span9'})
        if not value3_element:
            return None  # Return None if price element is not found

        value3 = value3_element.text.strip()

        operating_element = soup.find('tr', {'class': 'a-spacing-small po-operating_system'})
        if not operating_element:
            return None  # Return None if price element is not found

        operating = operating_element.text.strip()

        value4_element = soup.find('tr', {'class': 'a-spacing-small po-operating_system'})
        if not value4_element:
            return None  # Return None if price element is not found

        value4 = value4_element.text.strip()

        cellular_element = soup.find('tr', {'class': 'a-spacing-small po-cellular_technology'})
        if not cellular_element:
            return None  # Return None if price element is not found

        cellular = cellular_element.text.strip()

        value5_element = soup.find('tr', {'class': 'a-spacing-small po-cellular_technology'})
        if not value5_element:
            return None  # Return None if price element is not found

        value5 = value5_element.text.strip()



        
        return { 'price': price, 'rating':rating, 'stack':stack, 'brand':brand, 'value':value, 'model':model, 'value1':value2, 'network':network, 'value3':value3, 'operating':operating, 'value4':value4, 'cellular':cellular, 'value5':value5, }
    except Exception as e:
        print("Error occurred while scraping Amazon:", e)
        return None

def scrape_flipkart_product(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322) Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch data from Flipkart. Status code: {response.status_code}")

        soup = BeautifulSoup(response.content, 'html.parser')

       

        price_element = soup.find('div', {'class': '_30jeq3 _16Jk6d'})
        if not price_element:
            raise ValueError("Price element not found on the page")
        price = price_element.text.strip()

        
        return { 'price': price, }
    except requests.RequestException as e:
        print("Request Error occurred while scraping:", e)
        return None
    except Exception as e:
        print("Error occurred while scraping:", e)
        return None