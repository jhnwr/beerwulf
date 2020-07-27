from requests_html import HTMLSession
import pandas as pd
import time

s = HTMLSession()
drinklist = []

def request(url):
    r = s.get(url)
    r.html.render(sleep=1)
    return r.html.xpath('//*[@id="product-items-container"]', first=True).absolute_links

def parse(products):
    for item in products:
        r = s.get(item)
        name = r.html.find('div.product-detail-info-title', first=True).text
        subtext = r.html.find('div.product-subtext', first=True).text
        price = r.html.find('span.price', first=True).text
        try:
            rating = r.html.find('span.label-stars', first=True).text
        except:
            rating = 'none'   
        if r.html.find('div.add-to-cart-container'):
            stock = 'in stock'
        else:
            stock = 'out of stock'

        drink = {
            'name': name,
            'subtext': subtext,
            'price': price,
            'rating': rating,
            'stock': stock
        }
        drinklist.append(drink)

def output():
    df = pd.DataFrame(drinklist)
    df.to_csv('drinklist.csv', index=False)
    print('Saved to CSV.')

x=1

while True:
    try:
        products = request(f'https://www.beerwulf.com/en-gb/c/beers?segment=Beers&page={x}&catalogCode=Beer_1')
        print(f'Getting items from page {x}..')
        parse(products)
        print('Total Items = ', len(drinklist))
        x = x+1
        time.sleep(2)
    except:
        print('No more items!')
        break

output()
print(len(drinklist))
