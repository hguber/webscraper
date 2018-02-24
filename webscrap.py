from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import datetime
import pickle
import time
import lxml
import nltk
import codecs
def simple_get(url):
    try:
        with closing(get(url, stream = True)) as resp:
            if is_good_response(resp):
                return resp.text
            else:
                return None
    except RequestException as e:
        log_error('Error during request to {0} : {1}'.format(url, str(e)))
        return None

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return(resp.status_code == 200
           and content_type is not None
           and content_type.find('html') > -1)

def log_error(e):
    print(e)

def pickle_save(list, name):
    pickle.dump(list, open(name + ".p","wb"))
def pickle_load(list, name):
    list = pickle.load(open(name + ".p", "rb"))

def scrape():
    l1 = list()
    l2 = list()
    l3 = list()
    l4 = list()
    d = {}
    global globnum
    global globcount
    global beforedate
    globcount = 0
    try:
        raw_html = simple_get('http://www.newyorksocialdiary.com/party-pictures')
        html = BeautifulSoup(raw_html, 'html.parser')
        for li in html.findAll('li', attrs={'class': 'pager__item--last'}):
            lastlink = (li.find('a')['href'])
            globnum = int(lastlink[-2:])
        for x in range(0, globnum + 1):
            if(x == 0):
                raw_html = simple_get('http://www.newyorksocialdiary.com/party-pictures')
            raw_html = simple_get('http://www.newyorksocialdiary.com/party-pictures' + '?page=' + str(x))
            html = BeautifulSoup(raw_html, 'html.parser')
            if(x == globnum):
                for li in html.findAll('div', attrs={'class': 'views-row'}):
                    globcount += 1
                for i, li in enumerate(html.select('a')):
                    if (i >= 19 and i < 19 + globcount):
                        l1.append(li.get('href'))
                for ind in range(1,globcount + 1):
                    l2.append(datetime.datetime.strptime(html.find("div", class_=("views-row" + "-" + str(ind))).find("span",
                                                                                   class_="views-field-created").text,' %A, %B %d, %Y '))

            else:
                for i, li in enumerate(html.select('a')):
                    if(i >= 19 and i <= 68):
                        l1.append(li.get('href'))
                for ind in range(1, 51):
                    l2.append(datetime.datetime.strptime(html.find("div", class_=("views-row" + "-" + str(ind))).find("span",
                                                                                   class_="views-field-created").text,' %A, %B %d, %Y '))

            pickle_save(l1, 'l1')
            pickle_save(l2, 'l2')
    except:
        pass
    pickle_load(l1, 'l1')
    pickle_load(l2, 'l2')
    for x in l2:
        if x < datetime.datetime.strptime(" Monday, December 1, 2014 ", ' %A, %B %d, %Y '):
            l3.append(x)
    for x in l2:
        if x == datetime.datetime.strptime(" Monday, December 1, 2014 ", ' %A, %B %d, %Y '):
            globaldate = l2.index(x)
    for x in range(globaldate+1, len(l1)):
        l4.append(l1[x])
    for x in range(0,len(l4)):
        d[l4[x]] = l3[x]
    pickle_save(d,'dict')
    captions = list()
    l5 = list()
    for x in l4:
        l5.append('http://www.newyorksocialdiary.com' + x)
    '''for i, x in enumerate(l5):
        try:
            raw_html = simple_get(x)
            html = BeautifulSoup(raw_html, 'html.parser')
            print(i,x)
        except:
            pass'''
    captionfile = codecs.open('captions.txt', "w+", "utf-8")

    for x in l5:
        try:
            raw_html = simple_get(x)
            html = BeautifulSoup(raw_html, 'lxml')
            print(x)
        except:
            pass
        for wrapper in html.findAll('div', class_='photocaption'):
            captionfile.write(wrapper.text + '\n')
        for caption in html.findAll('table', cellpadding = 1):
            captionfile.write(caption.text)

    captionfile.close()
def main():
    '''scrape()'''
    file_content = codecs.open('captions1.txt', encoding= 'utf-8').read()
    tokens = nltk.word_tokenize(file_content)
    print(tokens)

#2009 lectures for luncheons
   # Tuesday, March 20, 2007
if __name__ == "__main__":
    main()

#parties before December 1st, 2014
#31 pages