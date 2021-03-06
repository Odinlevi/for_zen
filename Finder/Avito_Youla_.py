from bs4 import BeautifulSoup
import urllib
import urllib.request, socket
from urllib.parse import quote
import requests
import sys
import smtplib
import time
from time import sleep
from transliterate import translit, get_available_language_codes

# Here are emails, which are need for script's work
sender = 'maximiliannikiforov@mail.ru'
#destination = 'maximiliannikiforov@gmail.com'
destination = 'Zenonius@gmail.com'

# Here is beginnig of work with files and all the instructions
try:
    file = open('hrefs.txt', 'r', encoding="utf-8")
    file.close
except:
    print('The reference database was not created / was deleted, I create a new one...')
    file = open('hrefs.txt', 'w', encoding="utf-8")
    file.close
try:
    f_tags = open('tags.txt', 'r', encoding="utf-8")
    tags = f_tags.read().replace('\n\n\n', '').replace('\n\n', '').split('\n')
except:
    print('Please, create file "tags.txt" and fill it with tags;\n'
          '!!!! Every tag must be splitted by "\\n"\n'
          'Example: IPhone 6S\n'
          'Intel Core I7\n'
          'Mercedes benz C 300 4MATIC\n'
          'You can also use such signs like @ and $\n'
          'First is used for region\'s denomination: 1 or 2 (Moscow or Moscow Region)\n'
          'Second is used for definition of price limits in rubles\n'
          'You can type 1000 (max price) or 500:1000 (min and max prices)')
    sys.exit()
global_count = 0
# I found the file tags.txt, so shall we begin
if tags != ['']:
    # Avito.ru
    for finder in tags:
        part1 = 'https://www.avito.ru'
        # If you typed the sign @, I'll change the region
        if finder.find('@') != -1:
            semn = finder.find('@')
            if finder[semn+1] == '1':
                region = 'moskva'
            elif finder[semn+1] == '2':
                region = 'moskovskaya_oblast'
            finder = finder.replace(finder[semn]+finder[semn+1], '')
        else:
            region = 'rossiya'
        # If you typed the sign $, I'll change the price limits
        if finder.find('$') == -1:
            lenta = 'https://www.avito.ru/'+region+'?q={0}&i=1'.format(quote(finder.replace('\ufeff', '')))
        else:
            if finder.find(':') != -1:
                lenta='https://www.avito.ru/'+region+'?pmin='+finder[finder.find('$')+1 : finder.find(':')]+'&pmax='+finder[finder.find(':')+1 : ]+'&q={0}&i=1'.format(quote(finder[:finder.find('$')].replace('\ufeff', '')))
            else:
                lenta='https://www.avito.ru/'+region+'?pmax='+finder[finder.find('$')+1 : ]+'&q={0}&i=1'.format(quote(finder[:finder.find('$')].replace('\ufeff', '')))
            finder = finder[:finder.find('$')]
        # Beginning of work with the site www.Avito.ru
        url_list = 'Avito.ru, item - '+finder+':\n'
        try:
            page = urllib.request.urlopen(lenta)
        except:
            url_list = url_list+'There is no such item on Avito.ru now - '+finder+'\n'
            #print('There is no such item on Avito.ru now - '+finder)
            continue
        soup = BeautifulSoup(page.read(), "html.parser")
        etc = soup.find_all("a", class_="item-description-title-link")
        count = 0
        # Here I got all the links, and I just try to use them right
        for hrefs in etc:
            # Link is ready!
            if count >= 10:
                break
            url = part1 + hrefs.get('href')
            f_r = open('hrefs.txt', 'r', encoding="utf-8")
            f_cont = f_r.read()
            f_r.close()
            if f_cont.find(url) == -1:
                url_list = url_list+url+'\n'
                f_w = open('hrefs.txt', 'a', encoding="utf-8")
                f_w.write(url+'\n')
                f_w.close()
                count += 1
                global_count += 1
        if count == 0:
            url_list = url_list+'There is no such item on Avito.ru now - '+finder+'\n'
            #print('There is no such item on Avito.ru now - '+finder)
    # Youla.ru
    for finder in tags:
        part1 = 'https://youla.ru'
        # If you typed the sign @, I'll change the region
        region = ''
        if finder.find('@') != -1:
            finder = finder.replace(finder[finder.find('@')]+finder[finder.find('@')+1], '')
            region = 'moskva'
        # If you typed the sign $, I'll change the price limits
        if finder.find('$') == -1:
            lenta = 'https://youla.ru/?q={0}'.format(quote(finder.replace('\ufeff', '')))
        else:
            if finder.find(':') != -1:
                lenta='https://youla.ru/'+region+'?attributes[price][from]='+finder[finder.find('$')+1 : finder.find(':')]+'00&attributes[price][to]='+finder[finder.find(':')+1 : ]+'00&q={0}'.format(quote(finder[:finder.find('$')].replace('\ufeff', '')))
            else:
                lenta='https://youla.ru/'+region+'?attributes[price][to]='+finder[finder.find('$')+1 : ]+'00&q={0}'.format(quote(finder[:finder.find('$')].replace('\ufeff', '')))
            finder = finder[:finder.find('$')]
        # Beginning of work with the site www.Youla.ru
        url_list = url_list+'Youla.ru, item - '+finder+':\n'
        page = urllib.request.urlopen(lenta)
        soup = BeautifulSoup(page.read(), "html.parser")
        f_li = soup.find_all("li", class_="product_item")
        count = 0
        # Here I got all the links, and I just try to use them right
        for hrefs in f_li:
            if count >= 10:
                break
            etc = hrefs.find_next("a")
            # Link is ready!
            url = part1 + etc.get('href')
            f_r = open('hrefs.txt', 'r', encoding="utf-8")
            f_cont = f_r.read()
            f_r.close()
            if f_cont.find(url) == -1:
                url_list = url_list+url+'\n'
                f_w = open('hrefs.txt', 'a', encoding="utf-8")
                f_w.write(url+'\n')
                f_w.close()
                count += 1
                global_count += 1
        if count == 0:
            url_list = url_list+'There is no such item on Youla.ru now - '+finder+'\n'
            #print('There is no such item on Youla.ru now - '+finder)
    sng = translit(url_list, 'ru', reversed=True)
    if global_count != 0:
        # Email sending
        smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
        smtpObj.ehlo()
        smtpObj.starttls()
        # Yeah, it is my password... Or not?
        smtpObj.login(sender,'nelyublyuparoli')
        msg = "\r\n".join([
            "From: "+sender,
            "To: "+destination,
            "Subject: URL",
            "",
            sng
            ])
        smtpObj.sendmail(sender,destination,msg.replace('\ufeff', ''))
        smtpObj.quit()
    print("Sended: "+sng)
