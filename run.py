import requests
from bs4 import BeautifulSoup
import json
import glob
import pandas as pd
session = requests.Session()

def login():
    print("Login...")
    loginUser = {
        'username': 'vellie',
        'password': 'Vellie99sk'
    }
    res = session.post("http://localhost:5000/login", data=loginUser)
    soup = BeautifulSoup(res.text, 'html.parser')
    page_item = soup.findAll('li', attrs={'class': 'page-item'})
    total_pages = len(page_item) - 2
    print(total_pages)
    return total_pages

def get_urls(hal):
    print(f"get urls...Page : {hal}")
    paraMeter = {'page': hal}
    res = session.get("http://localhost:5000", params=paraMeter)
    soup = BeautifulSoup(res.text, 'html.parser')
    urlTitle = soup.findAll('h4', attrs={'class': 'card-title'})
    kumpUrl = []
    for url in urlTitle:
        txtUrl = url.find('a')['href']
        kumpUrl.append(txtUrl)
        print(txtUrl)
    return kumpUrl

def get_details(url):
    print(f"Details...{url}")
    res = session.get("http://localhost:5000"+url)
    soup = BeautifulSoup(res.text, 'html.parser')
    title = soup.find('h3', attrs={'class': 'card-title'})
    price = soup.find('h4', attrs={'class': 'card-price'})
    stock = soup.find('span', attrs={'class': 'card-stock'})
    category = soup.find('span', attrs={'class': 'card-category'})
    description = soup.find('p', attrs={'class': 'card-text'})
    detail_prod = {
        'title': title.text.strip(),
        'price': price.text.strip(),
        'stock': stock.text.strip().replace('stock: ', ''),
        'category': category.text.strip().replace('category: ', ''),
        'description': description.text.strip().replace('Description: ', '')
    }
    return detail_prod

def create_csv():
    print("Create csv...")
    files = sorted(glob.glob('./results/*.json'))
    datas = []
    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)
    df = pd.DataFrame(datas)
    df.to_csv("results.csv")
    print("CSV generated...")

def run():
    totalPages = login()

    pageUrl = []
    for i in range(totalPages):
        pageUrl = pageUrl + (get_urls(i+1))

    data_product = []
    for url in pageUrl:
        data_product.append(get_details(url))
        with open('./results/{}.json'.format(url.replace('/', '')), 'w') as outfile:
            json.dump(get_details(url), outfile)

    create_csv()

if __name__ == "__main__":
    run()
