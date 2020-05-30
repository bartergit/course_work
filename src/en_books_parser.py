import random
import re
import requests
from lxml import html
from dictionary import format_sentence
from pickle_manip import save_pickle_obj, load_pickle_obj

def choose(dict):
    overall = 0
    total = 0
    for i in dict:
        overall += dict[i]
    rand = random.randint(0,overall)
    for i in dict:
        total += dict[i]
        if total >= rand:
            return i

def get_books(flag = False):
    a = requests.get("http://www.gutenberg.org/browse/scores/top")
    tree = html.fromstring(a.content.decode())
    nums_for_url = tree.xpath('//li/a')
    temp = [None]*100
    for ind in range(0,100):
        temp[ind] = nums_for_url[ind].get("href")
        temp[ind] = temp[ind][temp[ind].find("/", 1) + 1:]
    nums_for_url = temp
    urls = ["http://www.gutenberg.org/cache/epub/"+str(i)+"/pg"+str(i)+".txt" for i in nums_for_url]
    n = 0
    output = []
    for url in urls:
        book = format_sentence(requests.get(url).content.decode(),"en")
        if flag:
            f = open("corpus/en_books/book" + str(n) + ".txt", 'w', encoding='utf-8')
            print(n, end=" ")
            n += 1
            f.write(book)
            output += re.split('; |!|\.|\?', book)
            f.close()
    return output

if __name__ == "__main__":
    save_pickle_obj(get_books(True),"corpus/eng_books")  #should be called once
