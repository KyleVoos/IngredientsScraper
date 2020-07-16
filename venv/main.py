import requests
from bs4 import BeautifulSoup
import csv
import time
import random

# content = requests.get("https://www.ewg.org/skindeep/search/?search_type=ingredients&per_page=8921")
# # content = requests.get("https://www.ewg.org/skindeep/search/?search_type=ingredients&per_page=10")
# soup = BeautifulSoup(content.text, 'html.parser')
# allHrefs = []
# elements = soup.find_all('p', {'class' : 'product-name'})
# for ele in elements:
#     a = ele.find('a');
#     if a.text:
#         allHrefs.append('https://www.ewg.org' + a['href'])
        
id = 1

#proxies = ["189.129.170.65:999"]
# proxies = ["35.230.21.108:80","206.127.88.18:80","64.227.2.152:8080"]
# proxies = ["64.62.166.73:3838"]
# proxies = ["184.149.34.86:51529"'69.162.66.52:5836']
# value = random.choice(proxies)
# proxy = {'https':value}

with open('ing_ewg.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    fieldname = ['Rating', 'id', 'Short-Info', 'Purpose', 'More-Info']
    writer = csv.DictWriter(csv_file, fieldname, delimiter='|')
    writer.writeheader()
    with open('ing_names.csv', mode='w', newline='', encoding='utf-8') as csv_file2:
        fieldname2 = ['Name', 'id']
        writer2 = csv.DictWriter(csv_file2, fieldname2, delimiter='|')
        writer2.writeheader()
        page = 1;
        pageSize = 50
        url = ""
        while page * pageSize < 9000:
            if page == 1:
                url = "https://www.ewg.org/skindeep/search/?search_type=ingredients&per_page=50"
            else:
                url = "https://www.ewg.org/skindeep/search/?page={0}&per_page={1}&search_type=ingredients".format(page, pageSize)
            # content = requests.get("https://www.ewg.org/skindeep/search/?search_type=ingredients&per_page=8921")
            try:
                # content = requests.get(url, proxies=proxy)
                content = requests.get(url)
                print(content.status_code)
            except:
                # proxies.remove(value)
                # value = random.choice(proxies)
                # proxy = {'https': value}
                print(content.status_code)
            while content.status_code == 429:
                print("content:{0} | id:{1}".format(content, id))
                time.sleep(25)
                # value = random.choice(proxies)
                # proxy = {'https': value}
                # print(proxy)
                # content = requests.get("https://httpbin.org/ip", proxies=proxy)
                content = requests.get(url)
                # print(content.text)
                # content = requests.get(url, proxies=proxy)
            soup = BeautifulSoup(content.text, 'html.parser')
            allHrefs = []
            elements = soup.find_all('p', {'class': 'product-name'})
            for ele in elements:
                a = ele.find('a');
                if a.text:
                    allHrefs.append('https://www.ewg.org' + a['href'])
            for href in allHrefs:
                try:
                    # content = requests.get(href, proxies=proxy)
                    content = requests.get(href)
                except:
                    # proxies.remove(value)
                    # value = random.choice(proxies)
                    # proxy = {'https': value}
                    print(content.status_code)
                finally:
                    # content = requests.get(href, proxies=proxy)
                    # content = requests.get(href)
                    while content.status_code == 429:
                        print("content:{0} | id:{1}".format(content, id))
                        time.sleep(25)
                        # value = random.choice(proxies)
                        # proxy = {'https': value}
                        # print(proxy)
                        # content = requests.get("https://httpbin.org/ip", proxies=proxy)
                        # print(content.text)
                        # content = requests.get(href, proxies=proxy)
                        content = requests.get(href)
                print("content:{0} | id:{1}".format(content.status_code, id))
                soup = BeautifulSoup(content.text, 'html.parser')
                try :
                    name = soup.find('h2', {'class' : 'chemical-name text-block'}).string
                    if name.find('/') != -1:
                        name = name.replace("/ ", "/")
                    end = name.find(')')
                    if end != -1:
                        start = name.find('(')
                        if start != -1:
                            commonName = name[start + 1:end] if end == len(name) else name[start + 1:end] + name[end + 1:]
                            name = name[:start - 1] if end == len(name) else name[:start - 1] + name[end + 1:]
                            # print("name : " + name + " | commonName : " + commonName)
                            writer2.writerow({'Name':name, 'id':id})
                            writer2.writerow({'Name':commonName, 'id':id})
                        else:
                            print("ERROR: OPEN PAREN NOT FOUND - id = {0}".format(id))
                    else:
                        writer2.writerow({'Name': name, 'id': id})
                    purpose = soup.find('p', {'class' : 'chemical-info chemical-functions-text hidden'}).string
                    short_info = soup.find('p', {'class': 'chemical-info chemical-about-text hidden'}).string
                    rate = soup.find('img', {'class' : 'squircle'})['src'].split("score=")[1]
                    min = rate.split("min=")[1][0]
                    rating = ord(rate[0]) - 48 if rate[0] == min else ((ord(rate[0]) - 48) + (ord(min) - 48)) * 0.5
                    writer.writerow({"Rating":rating, 'id':id, 'Short-Info':short_info, 'Purpose':purpose, 'More-Info':href})
                    print("name : " + name + "| id: {0}".format(id))
                    id += 1
                except:
                    print("ERROR: id = {0}".format(id))
                time.sleep(.85)
            page += 1


i = 0;
with open('ing_ewg.csv', mode='r', newline='', encoding='utf-8') as csv_file:
    with open('ing_ewgFixed.csv', mode='w',newline='',encoding='utf-8') as out_file:
        fieldname = ['Rating', 'id', 'Short-Info', 'Purpose', 'More-Info']
        reader = csv.DictReader(csv_file, fieldname, delimiter='|')
        writer = csv.DictWriter(out_file, fieldname, delimiter='|')
        writer.writeheader()
        for row in reader:
            if i == 0:
                i += 1
                continue
            rating = row['Rating']
            if rating.find(".0") != -1:
                rating = rating[0]
            more_Info = row['More-Info'].split("https://www.ewg.org/skindeep/ingredients/")[1]
            writer.writerow({"Rating":rating, 'id':row['id'], 'Short-Info':row['Short-Info'], 'Purpose':row['Purpose'], 'More-Info':more_Info})

