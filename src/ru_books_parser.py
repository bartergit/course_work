import codecs
import os
from pickle_manip import save_pickle_obj, load_pickle_obj
from dictionary import format_sentence
import re

def books_parse():
    filenames = os.listdir(path="corpus/ru_books")
    output = []
    for file in filenames:
        try:
            inputFile = codecs.open('corpus/ru_books/' + file, 'r', encoding='cp1251')
            book = inputFile.read()
            book = format_sentence(book)
            output += re.split('; |!|\.|\?', book)
            print(file)
        except:
            print("ERROR",file)
    return output


if __name__ == "__main__":
    save_pickle_obj(books_parse(),"corpus/ru_books")