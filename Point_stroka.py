# Библотеки Питона
from bs4 import BeautifulSoup
import urllib.request, socket
import sys
import codecs
import locale
import win_unicode_console
import requests

# Требуется для работы консоли с русскими символами
win_unicode_console.enable()

my_file = open('D:/NEWS_UPDATE/news_from_point_MD/news.csv', 'w', encoding='utf-8')
my_file = open('D:/NEWS_UPDATE/news_from_point_MD/news.csv', 'a', encoding='utf-8')

lentaurlru = "https://stiri.md/"
spage = urllib.request.urlopen(lentaurlru)
fsoup = BeautifulSoup(spage.read(), "html.parser")
etc = fsoup.find_all("a", display="block,block,none")

counter_for_first_hrefs = 0
maximum = 10

for first_hrefs in etc:
    if counter_for_first_hrefs < maximum:
        # Получаем полную ссылку на новость
        url = lentaurlru + first_hrefs.get('href')
        print(url)
        counter_for_first_hrefs+=1
    else:
        break

    def valid_http(url):
        try:
            connect = urllib.request.urlopen(url)
            return 1
        except urllib.request.URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server: ', url)
                print('Reason: ', e.reason)
                return 0
            elif hasattr(e, 'code'):
                print('The server ', url, ' couldn\'t fulfill the request.')
                print('Error code: ', e.code)
                return 0

    if valid_http(url):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), "html.parser")

        # Вырезаем все видеофайлы, ибо нафиг
        joke = soup.find_all('iframe')
        for joker in joke:
            bad_tag1 = soup.find('iframe')
            if bad_tag1 != None:
                hren = bad_tag1.extract()

        title = soup.find('title', class_="next-head")
        utit = title.get_text()
        tit_for_text = utit
        bad_qoutes = ['«', '»', '"', 'ʺ', '˝', '˵', '˶', '〞', '〟']
        for all_for_change in bad_qoutes:
            utit = utit.replace(all_for_change, '"')
        utit = utit + ' ;'
        #print(utit)

        helper = soup.findAll("h2", text=tit_for_text)
        for helpr in helper:
            body = helpr.findNext("div")
        ufullit = str(body)
        sep = '\n'
        source = '   POINT.MD   *** ;' + sep
        ufullit = ufullit + source
        ufullit = ufullit.replace('. ', '. ;' + sep)

        soup2 = BeautifulSoup(ufullit, "html.parser")
        utext = soup2.get_text()
        ufullit = utext
        print(ufullit)
        #print(utit)

        print("Принято (md) - " + utit)
        my_file.write(utit)
        my_file.write(ufullit)

my_file.close()
