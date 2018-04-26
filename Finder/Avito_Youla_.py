from bs4 import BeautifulSoup
import urllib.request, socket
import requests
import sys
import smtplib
import time
from time import sleep

sender = 'maximiliannikiforov@mail.ru'
destination = 'maximiliannikiforov@gmail.com'
#destination = 'Zenonius@gmail.com'

try:
    file = open('hrefs.txt', 'r')
    file.close
except:
    print('The reference database was not created / was deleted, I create a new one...')
    file = open('hrefs.txt', 'w')
    file.close
try:
    f_tags = open('tags.txt', 'r')
    tags = f_tags.read().split('\n')
except:
    print('Please, create file "tags.txt" and fill it with tags;\n'
          '!!!! Every tag must be splitted by "\\n"\n'
          'Example: IPhone 6S\n'
          'Intel Core I7\n'
          'Mercedes benz C 300 4MATIC')
    sys.exit()
if tags != ['']:
    for finder in tags:
        part1 = 'https://www.avito.ru'
        if finder.find('@') != -1:
            semn = finder.find('@')
            if finder[semn+1] == '1':
                region = 'moskva'
            elif finder[semn+1] == '2':
                region = 'moskovskaya_oblast'
            finder = finder.replace(finder[semn]+finder[semn+1], '')
        else:
            region = 'rossiya'
        if finder.find('$') != -1:
            if finder.find(':') != -1:
                price_min = int(finder[finder.find('$')+1 : finder.find(':')])
                price_max = int(finder[finder.find(':')+1 : ])
            else:
                price_max = int(finder[finder.find('$')+1 : ])
                price_min = 0
            finder = finder[:-finder.find('$')]
        else:
            price_min = 0
            price_max = 0
        #print(price_min, ' ', price_max)
        #print(finder)
        lenta = 'https://www.avito.ru/'+region+'?q='+finder
        page = urllib.request.urlopen(lenta)
        soup = BeautifulSoup(page.read(), "html.parser")
        etc = soup.find_all("a", class_="item-description-title-link")
        for hrefs in etc:
            url = part1 + hrefs.get('href')
            if price_max != 0:
                if price_min != 0:
                    price_txt = hrefs.findNext("div", class_="about ").get_text().replace('руб.', '').replace('Цена не указана', '0').replace('\n', '').replace(' ', '')
                    if price_min >= int(price_txt) or price_max <= int(price_txt):
                        continue
                else:
                    if price_max <= int(price_txt):
                        continue
            print(url)
            '''
            f_r = open('hrefs.txt', 'r')
            f_cont = f_r.read()
            f_r.close()
            if f_cont.find(url) == -1:
                smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
                smtpObj.ehlo()
                smtpObj.starttls()
                smtpObj.login(sender,'nelyublyuparoli')
                msg = "\r\n".join([
                  "From: "+sender,
                  "To: "+destination,
                  "Subject: URL",
                  "",
                  url
                  ])
                smtpObj.sendmail(sender,destination,msg)
                smtpObj.quit()
                f_w = open('hrefs.txt', 'a')
                f_w.write(url+'\n')
                f_w.close()
                print("Sended: "+url)
                time.sleep(30)
    for finder in tags:
        part1 = 'https://youla.ru'
        if finder.find('@') != -1:
            finder = finder.replace(finder[finder.find('@')]+finder[finder.find('@')+1], '')
        if finder.find('$') == -1:
            lenta = 'https://youla.ru/?q='+finder
        else:
            lenta='https://youla.ru/?attributes[price][to]='+finder[finder.find('$')+1 : ]+'00&q='+finder[:finder.find('$')]
            finder = finder[:-finder.find('$')]
        page = urllib.request.urlopen(lenta)
        soup = BeautifulSoup(page.read(), "html.parser")
        f_li = soup.find_all("li", class_="product_item")
        for hrefs in f_li:
            etc = hrefs.find_next("a")
            url = part1 + etc.get('href')
            f_r = open('hrefs.txt', 'r')
            f_cont = f_r.read()
            f_r.close()
            if f_cont.find(url) == -1:
                smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
                smtpObj.ehlo()
                smtpObj.starttls()
                smtpObj.login(sender,'nelyublyuparoli')
                msg = "\r\n".join([
                  "From: "+sender,
                  "To: "+destination,
                  "Subject: URL",
                  "",
                  url
                  ])
                smtpObj.sendmail(sender,destination,msg)
                smtpObj.quit()
                f_w = open('hrefs.txt', 'a')
                f_w.write(url+'\n')
                f_w.close()
                print("Sended: "+url)
                time.sleep(30)'''
