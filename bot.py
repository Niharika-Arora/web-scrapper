import xlrd
import os
import re
import requests
import pandas
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request


headers = {"Accept-Language": "en-US, en;q=0.5"}

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def find_link(url):
    r = requests.get(url, headers = headers)
    txt = BeautifulSoup(r.text, 'html.parser')
    links = []
    for link in txt.findAll('a'):
        links.append(link.get('href'))
    return r, links

def contact_check(links):
    url1 = ''
    for link in links:
        if str(link).casefold() == '/contact'.casefold() or str(link).casefold() == '/contact-us'.casefold() or str(link).casefold() == '/contactus'.casefold():
            url1 = url + link
    return url1

def save_file(r, url):
    body = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(body, 'html.parser')
    txt = soup.findALL(text=True)
    visible_texts = filter(tag_visible, txt) 
    mail_list = re.findall('[a-z0-9_\-\.]+@[a-z\.]+\.[a-z]{2,3}', str(visible_texts))
    phone = re.findall('(\+(\d\-\ )?\d{2,3}[\s\-]?)?(\d{10}|(\(\d{3}\)([\s\-]?)\d{3}\5\d{4})|(\d{3}([\s\-]?)\d{3}\7\d{4}))', str(visible_texts))
    dicn = {'link': url, 'email': mail_list, 'phone number': phone}
    for i in dicn.keys():
        print(dicn[i])
    df = pandas.DataFrame.from_dict(dicn, orient= 'index')
    df.transpose()
    df.to_csv('contact_info.csv')
    print("File Saved!!")

if __name__ == "__main__":
    loc = os.path.abspath('websites.xlsx')
    wb = xlrd.open_workbook(loc)
    st = wb.sheet_by_index(0)
    st.cell_value(0, 0)

    site = input("Enter name: ")
    url = ''

    for i in range(st.nrows):
        if site.casefold() == str(st.cell_value(i, 0)).casefold():
            url = str(st.cell_value(i, 1))
    if url == '':
        print("URL Not Found!")
        exit(0)
    print(url)
    lin = []
    ln = []
    url2 = ''
    url1 = ''
    flag = True
    response, lin = find_link(url)
    url1 = contact_check(lin)
    print(url1)
    if url1 != '':
        save_file(response, url1)
    else:
        while flag == True:
            for l in ln:
                url2 = url + l
                print(url2)
                if res.status_code == 404:
                    print("continue")
                    continue
                else:
                    res, ln = find_link(url2)
                    url2 = contact_check(ln)
                    if url2 == '':
                        continue
                    else:
                        save_file(res, url2)
                        print("broken")
                        break
            flag = False
    exit(0)