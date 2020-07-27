from requests_html import HTMLSession
from bs4 import BeautifulSoup

url = 'https://www.beerwulf.com/en-gb/c/subkegs?container=SUB%20Kegs%20-%202L%20keg&catalogCode=Beer_1'
url2 = 'https://www.beerwulf.com/en-gb/c/beers?segment=Beers&catalogCode=Beer_1&page=2'

s = HTMLSession()
r = s.get(url2)
r.html.render(sleep=1)

products = r.html.xpath('//*[@id="product-items-container"]', first=True)

for item in products.absolute_links:
    r = s.get(item)
    name = r.html.find('div.product-detail-info-title', first=True).text
    shortdesc = r.html.find('div.product-subtext', first=True).text
    price = r.html.find('span.price', first=True).text
    
    try:
        rating = r.html.find('span.label-stars', first=True).text
    except:
        rating = 'none'
    
    if r.html.find('div.add-to-cart-container'):
        stock = 'in stock'
    else:
        stock = 'out of stock'
    print(name, shortdesc, rating, price, stock)
