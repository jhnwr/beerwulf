import requests
from requests_html import HTMLSession
import pandas as pd

url = 'https://www.beerwulf.com/en-gb/c/subkegs?container=SUB%20Kegs%20-%202L%20keg&catalogCode=Beer_1'

#Use requests_HTML to create a session, then use render() to load the dynamic content
print('Rendering Page.')
s = HTMLSession()
r = s.get(url)
r.html.render(sleep=1) # sleep=1 is important - sleeps for x seconds after the render

#I used the xpath function to find the main product container. could have used a css selector
products = r.html.xpath('//*[@id="product-items-container"]/a')

beerlist = []

# Print statement so we can see it working
print('Getting beerwulf info..')

#loop through each element within the products xpath
for item in products:
    name  = item.find('h4', first=True).text # return the first item from the list, without this we would get all the H4 tags as a list
    price = item.find('span', first=True).text
    beer_type = item.find('p', first=True).text
    links = item.absolute_links # Pulls in the full urls
    
    # because the button has unique text we can search the item html for that string and if it returns, it is out of stock, if it isnt found, the item is in stock
    # IF statement for the above
    if item.search('Temporarily sold out'):
        stock = 'out of stock'
    else:
        stock = 'in stock'
        
    
    #print(dict(name=name,stock=stock)) # test string to get stock working

    product_info = {
    'Name': name,
    'Price': price,
    'Beer Type': beer_type,
    'Stock': stock,
    'URL': links
    }
    beerlist.append(product_info)

    print(f'Found {len(beerlist)} item(s)')

df = pd.DataFrame(beerlist)
df.to_excel('beer-list.xls', index=False)
