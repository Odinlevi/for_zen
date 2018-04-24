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
        lenta = 'https://www.avito.ru/rossiya?q='+finder
        page = urllib.request.urlopen(lenta)
        soup = BeautifulSoup(page.read(), "html.parser")
        etc = soup.find_all("a", class_="item-description-title-link")
        for hrefs in etc:
            url = part1 + hrefs.get('href')
            if finder.find('$') != -1:
                price_txt = hrefs.findNext("div", class_="about ").get_text().replace('руб.', '').replace('Цена не указана', '0').replace('\n', '').replace(' ', '')
                
                #print('{} : {}'.format(int(finder[finder.find('$')+1 : ]),int(price_txt)))
                if int(finder[finder.find('$')+1 : ]) < int(price_txt):
                    continue
                print(int(price_txt))
            #print(url)
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
        if finder.find('$') == -1:
            lenta = 'https://youla.ru/?q='+finder
        else:
            lenta='https://youla.ru/?attributes[price][to]='+finder[finder.find('$')+1 : ]+'00&q='+finder[:finder.find('$')]
            print(lenta)
        page = urllib.request.urlopen(lenta)
        soup = BeautifulSoup(page.read(), "html.parser")
        f_li = soup.find_all("li", class_="product_item")
        for hrefs in f_li:
            etc = hrefs.find_next("a")
            url = part1 + etc.get('href')
            #print(url)
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
