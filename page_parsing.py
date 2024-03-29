# -*-coding:utf-8-*-
#@Author: Songzq
#@Time: 2019年06月10日08时
#说明:
#总结:
import requests
from bs4 import BeautifulSoup
import time
import pymongo

client = pymongo.MongoClient('localhost', 27017)
ceshi = client['ceshi']
url_list = ceshi['url_list3']
item_info = ceshi['item_info3']

#spider 1

def get_links_from(channel, pages, who_sells=0):
    #https://bj.58.com/diannao/0/pn2
    list_view = '{}{}/pn{}/'.format(channel,str(who_sells),str(pages))
    wb_data = requests.get(list_view)
    time.sleep(1)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find('td','t'):
        for link in soup.select('td.t a.t'):
            item_link = link.get('href').split('?')[0]
            url_list.insert_one({'url':item_link})
            print(item_link)
            get_item_info(item_link)
    else:
        pass
        #Nothing!

#spider 2
def get_item_info(url):
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    #print(soup.prettify())
    title = soup.title.text
    #print(title)
    price = soup.select('div.infocard__container__item__main > span')[0].text.strip()
    date = soup.select('div.detail-title__info > div.detail-title__info__text')[0].text
    area = list(soup.select('div.infocard__container__item__main > a')[0].stripped_strings)
    item_info.insert_one({'title':title, 'price':price, 'date':date, 'area': area })
    print({'title':title, 'price':price, 'date':date, 'area': area })
get_links_from('https://bj.58.com/pbdn/',2)
