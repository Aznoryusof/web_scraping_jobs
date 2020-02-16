import requests
from bs4 import BeautifulSoup as BS

def main():
    url_main = "https://www.unileverfoodsolutions.co.th"
    url_products_catalog = url_main + "/en/products.html?page="

    html_products_catalog = requests.get(url_products_catalog)
    num_pages = 8

    # Loop through each page that stores information of the products
    for page_no in range(num_pages):
        url_page = url_products_catalog + str(page_no)

        # Request for html for product groups in current page and get soup
        html_page = requests.get(url_page)
        soup_page = BS(html_page.content, 'html.parser')
        
        # Get main product information
        for tile in soup_page.find_all('div', class_ = "product-tile js-product-tile col-span-4 product unavailable"):
            sku_number = tile.get('data-product-number')
            sku_name = tile.find('a').get('title')
            sku_url = url_main + str(tile.find('a').get('href')) 
            
            if None in (sku_number, sku_name, sku_url):
                continue
            
            # Go to product details page to scrape data there
            html_1Xproduct_catalog = requests.get(sku_url)
            soup_1Xproduct_catalog = BS(html_1Xproduct_catalog.content, 'html.parser')
            
            # Add full description of product if available
            product_description_full = []
            try:
                product_description_full.append(soup_1Xproduct_catalog.find('div', class_ = "pdp-section_top pdp-section_proplist clearfix").find('p').text.strip())
            except:
                product_description_full.append('')
            
            # Add short description of product from sub-header if available
            product_description_short = []
            try:
                product_description_short.append(soup_1Xproduct_catalog.find('div', class_ = "pdp-row_top").find('h3').text.strip())
            except:
                pass
            
            # Add short description of product if available
            try:
                for text in soup_1Xproduct_catalog.find('ul', class_ = 'ufs-product-usplist').find_all('li'):
                    product_description_short.append(text.text.strip())
            except:
                product_description_short.append('')
            
            # Add product detailed information if available
            product_details = {}
            for item in soup_1Xproduct_catalog.find_all('div', class_ = 'pdp-row'):
                if None in (item.find('h3'), item.find('p')):
                        continue
                
                product_details[item.find('h3').text.strip()] = item.find('p').text.strip()

            print(sku_number, end = '\n'*1)
            print(sku_name, end = '\n'*1)
            print(sku_url, end = '\n'*2)
            print(product_description_full, end = '\n'*2)
            print(product_description_short, end = '\n'*2)
            print(product_details, end = '\n'*2)
            

if __name__ == "__main__":
    main()