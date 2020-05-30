import urllib.request

import bs4 as bs

from pickle_manip import *

from dictionary import format_sentence


def wiki_parse(flag = False):
    a = urllib.request.urlopen("https://ru.wikipedia.org/wiki/%D0%92%D0%B8%D0%BA%D0%B8%D0%BF%D0%B5%D0%B4%D0%B8%D1%8F:%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81%D1%82%D0%B0%D1%82%D0%B5%D0%B9,_%D0%BA%D0%BE%D1%82%D0%BE%D1%80%D1%8B%D0%B5_%D0%B4%D0%BE%D0%BB%D0%B6%D0%BD%D1%8B_%D0%B1%D1%8B%D1%82%D1%8C_%D0%B2%D0%BE_%D0%B2%D1%81%D0%B5%D1%85_%D1%8F%D0%B7%D1%8B%D0%BA%D0%BE%D0%B2%D1%8B%D1%85_%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1%8F%D1%85")
    a = a.read()
    a = bs.BeautifulSoup(a,'lxml')
    a = a.find_all('a')
    urls = []
    for i in a:
        if i.text != "":
            urls += [(i.text,i.get('href'))]
    urls = urls[73:-245]
    output = []
    for i in range(0,998):
        scrapped_data = urllib.request.urlopen('https://ru.wikipedia.org/'+urls[i][1])
        article = scrapped_data.read()
        parsed_article = bs.BeautifulSoup(article,'lxml')

        paragraphs = parsed_article.find_all('p')
        print(i,end=" ")

        article_text = ""

        for p in paragraphs:
            article_text += p.text

        processed_article = article_text
        processed_article = format_sentence(processed_article)
        output.append(processed_article)
        if flag:
            try:
                f = open("corpus/wikis/wiki" + str(i) + ".txt", "w+", encoding='utf-8')
                f.write(urls[i][0]+'\n'+processed_article)
                f.close()
            except:
                pass
    return output

if __name__ ==  "__main__":
    save_pickle_obj(wiki_parse(True),"corpus/wiki")