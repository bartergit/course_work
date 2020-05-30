import re
from _word_declaration import Word


def format_sentence(string, flag="ru"):
    if flag == "ru":
        string = re.sub(u'[^а-яА-Яё \-.,;?!)(]', '', string)
    else:
        string = re.sub(u'[^a-zA-z \-.,;?!)(]', '', string)
    for s in ".,;?!)":
        string = string.replace(s, " " + s)
    string = string.replace("(","( ")
    string = re.sub(r'\s+', ' ', string)
    return string


def format_word(string, flag="ru"):
    if flag == "ru":
        return re.sub(u'[^а-яА-Яё\- ]', '', string)
    else:
        return re.sub(u'[^a-zA-Z\- ]', '', string)


def create_dictionary(array):
    dict = {}
    for sentence in array:
        sentence = sentence.split()
        for word in sentence:
            # word = format_word(word)
            word = word.lower()
            try:
                dict[word] += 1
            except:
                dict[word] = 1
    return dict
