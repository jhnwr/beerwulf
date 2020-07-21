from requests_html import HTMLSession
import pandas as pd

url = 'https://www.beerwulf.com/en-gb/c/subkegs?container=SUB%20Kegs%20-%202L%20keg&catalogCode=Beer_1'
beerlist = []

def render_page(url):
    print('Rendering Page.')
    s = HTMLSession()
    r = s.get(url)
    r.html.render(sleep=1) # sleep=1 is important - sleeps for x seconds after the render
    products = r.html.xpath('//*[@id="product-items-container"]/a')
    return products

def parse(products):
    print('Getting beerwulf info..')
    for item in products:
        name  = item.find('h4', first=True).text
        beer_type = item.find('p', first=True).text
        price = item.find('span', first=True).text
        links = item.absolute_links

        if item.search('Temporarily sold out'):
            stock = 'out of stock'
        else:
            stock = 'in stock'

        product_info = {
        'Name': name,
        'Price': price,
        'Beer Type': beer_type,
        'Stock': stock,
        'URL': links
        }
        beerlist.append(product_info)

        print(f'Found {len(beerlist)} item(s)')

def output():
    df = pd.DataFrame(beerlist)
    print('Saved to .xls')
    df.to_excel('beer-list.xls', index=False)


html = render_page(url)
parse(html)
output()
