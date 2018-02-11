import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def get_one(name):
    url = "http://gallantryawards.gov.in"+name
    page = requests.get(url)


    soup = BeautifulSoup(page.content, 'html.parser')

    parent = soup.find_all('div',class_='reportarea')
    parent = parent[0]

    rows = parent.find_all('div',class_='newrow')

    data = {}
    for ele in rows:
        data[ele.select('div')[0].text.strip()] = ele.select('div')[1].text.strip()
    data['Name'] = soup.find_all('div',class_='profilename')[0].text.strip()
    print(data['Name'])
    return data

def get_name_urls(chakra):
        name_urls = []
        page = requests.get('http://gallantryawards.gov.in/awardees/'+chakra)
        soup = BeautifulSoup(page.content, 'html.parser')
        parent = soup.find_all('div',class_='awardpersonpic')

        for pic in parent:
            links = pic.select('a')[0]['href']
            links = links.split('\n')
            name_urls += links
        return name_urls
def get_all_data_from_chakra(chakra):
    print(chakra)
    name_urls = get_name_urls(chakra)
    print("Got name urls")
    data = []
    for url in name_urls:
        row = get_one(url)
        data.append(row)
    return data


link = 'shaurya-chakra'
data = []
for i in range(60,69):
    print(i)
    if i == 0:
        x = get_all_data_from_chakra(link)
    else:
        x = get_all_data_from_chakra(link+"?page="+str(i))
    data.extend(x)
data = pd.DataFrame(data)
data.to_csv(link+'2.csv',index=None)
