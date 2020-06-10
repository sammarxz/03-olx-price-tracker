import json
import time
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from config import (
    get_web_driver_options,
    get_firefox_web_driver,
    set_ignore_certificate_error,
    set_browser_as_incognito,
    set_automation_as_head_less,
    NAME,
    REGION,
    CATEGORY,
    BASE_URL,
    DIRECTORY
)
from selenium.common.exceptions import NoSuchElementException


class GenerateReport:
    def __init__(self, filename, region, category, base_link, data):
        self.data = data
        self.filename = filename
        self.region = region
        self.category = category
        self.base_link = base_link
        report = {
            'title': self.filename,
            'category': self.category,
            'region': self.region,
            'date': self.get_now(),
            'best_item': self.get_best_item(),
            'base_link': self.base_link,
            'products': self.data
        }
        print('Creating the report...')
        with open(f'{DIRECTORY}/{filename}.json', 'w') as f:
            json.dump(report, f)
        print("Done...")

    @staticmethod
    def get_now():
        now = datetime.now()
        return now.strftime('%d/%m/%Y %H:%M')

    def get_best_item(self):
        try:
            return sorted(self.data, key=lambda k: k['price'])[0]
        except Exception as e:
            print(e)
            print('Problem with sorting items')
            return None


class OLXApi:
    def __init__(self, search_term, region, category, base_url):
        self.base_url = base_url
        self.search_term = search_term
        self.region = region
        self.category = category
        options = get_web_driver_options()
        set_automation_as_head_less(options)
        set_ignore_certificate_error(options)
        set_browser_as_incognito(options)
        self.driver = get_firefox_web_driver(options)

    def run(self):
        print('Starting Script...')
        print(f'Looking for {self.search_term} products')

        products_list = self.get_products()

        if not products_list:
            print('Stopped script.')
            return

        print('Getting info about produts...')

        products = self.get_products_info(products_list)

        print(f'Got info about {len(products)} products...')

        self.driver.quit()
        return products

    def get_products(self):
        full_url = self.base_url + self.region + '/' + self.category + '?q=' + self.search_term

        print(f'Getting products at: {full_url}')

        self.driver.get(full_url)

        time.sleep(2) # wait to load page

        products = []

        try:
            products = self.driver.find_elements_by_xpath('/html/body/div[1]/div[2]/div[1]/div[4]/div/div[2]/div[9]/ul/li')
            return products
        except Exception as e:
            print('Didn\'t get any products...')
            print(e)
            return products

    def get_products_info(self, products):
        products_with_info = []

        for item in products:
            product = self.get_single_product_info(item)
            if product:
                products_with_info.append(product)
        return products_with_info

    def get_single_product_info(self, product):
        url = self.get_url(product)
        title = self.get_title(product)
        price = self.get_price(product)
        location = self.get_location(product)

        if title and price and location:
            product_info = {
                'url': url,
                'title': title,
                'location': location,
                'price': price,
            }
            return product_info
        return None

    def get_url(self, product):
        try:
            link = product.find_element_by_class_name('fnmrjs-0')
            return link.get_attribute('href')
        except Exception as e:
            return None

    def get_title(self, product):
        try:
            return product.find_element_by_class_name('fnmrjs-10').text
        except Exception as e:
            return None

    def get_price(self, product):
        price = None
        try:
            price = product.find_element_by_class_name('fnmrjs-16').text
            return price
        except Exception as e:
            return None

    def get_location(self, product):
        try:
            return product.find_element_by_class_name('fnmrjs-13').text
        except Exception as e:
            return None


if __name__ == '__main__':
    ox = OLXApi(NAME, REGION, CATEGORY, BASE_URL)
    data = ox.run()
    GenerateReport(NAME, REGION, CATEGORY, BASE_URL, data)
