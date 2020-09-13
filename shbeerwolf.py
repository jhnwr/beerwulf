import requests
from requests_html import HTMLSession
import pandas as pd

url = 'https://www.beerwulf.com/en-gb/c/subkegs?container=SUB%20Kegs%20-%202L%20keg&catalogCode=Beer_1'

#Use requests_HTML to create a session, then use render() to load the dynamic content
s = HTMLSession()
r = s.get(url)
r.html.render(sleep=1) # sleep=1 is important

beerlist = []
#I used the xpath function to find the main product container. could have used a css selector
products = r.html.xpath('//*[@id="product-items-container"]/a') #loop through each element within the products xpath

for item in products:
    name         = item.find('h4', first=True).text # return the first item from the list, without this we would get all the H4 tags as a list
    price        = item.find('span', first=True).text
    type         = item.find('p', first=True).text
    links        = item.absolute_links # Pulls in the full urls
    #stock        = item.find('#add-to-cart', first=True).text # Struggling to pull in the text from the button, to determin stock!!
    #print(dict(name = name, price = price, type = type, links = links)) # print output as a python dictionary
   
    product_info = {
    'Name': name,
    'Price': price,
    'Beer Type': type,
    'URL': links
    }
    beerlist.append(product_info)

df = pd.DataFrame(beerlist)
df.to_excel('Beer List.xls', index = False)
