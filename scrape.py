import bs4
import requests
import sys
from time import sleep
from random import randint
import pandas

url="https://store.steampowered.com/search/?category1=998&os=win&filter=globaltopsellers"

res=[]

max_page=input("Enter page number to search until: ")
try:
    max_page=int(max_page)
except:
    print("Invalid input. Run the program again.")
    sys.exit()

if max_page>50:
    sys.exit("Please enter a smaller number and run the program again.")

target=input("Enter target price: ")
try:
    target=float(target)
except:
    print("Invalid input")
    sys.exit()

for page in range(1,max_page+1):
    if page==1:
        url_attach=""
    else:
        url_attach="&page="+str(page)

    url+=url_attach

    response=requests.get(url)
    html_soup=bs4.BeautifulSoup(response.text, 'html.parser')
    container=html_soup.find_all('div', class_="responsive_search_name_combined")

    for i in range(len(container)):

        game=container[i]
        name=game.find('span', class_='title', recursive=True).text
        price_combined=game.find('div', class_="col search_price_discount_combined responsive_secondrow")

        if price_combined.find('span', recursive=True) is None:
            raw_price=price_combined.text.strip().replace("S$","")
            if raw_price.lower()=="free to play" or raw_price.lower()=="" or raw_price.lower()=="free":
                price=9999
            else:
                price=float(raw_price)

        else:
            for span in price_combined("span"):
                price_combined.span.decompose()

            raw_price=price_combined.text.strip().replace("S$","")
            if raw_price.lower()=="free to play":
                price=9999
            else:
                price=float(raw_price)
        if price<=target:
            res.append((name,price))


name=[]
price=[]
for i in range(len(res)):
    name.append(res[i][0])
    price.append(res[i][1])

test_df=pandas.DataFrame({"Name":name, "Price":price})
print(test_df.to_string())
