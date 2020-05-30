import random

from word_declaration import Word

from pickle_manip import *


class Word_usage():
    def __init__(self, word, next_word):
        self.itself = Word(word).first_form
        self.usages = {}
        self.add_next(next_word)

    def add_next(self, next_word):  # распихать все по частям речи
        next_word = Word(next_word).first_form
        try:
            self.usages[next_word] += 1
        except:
            self.usages[next_word] = 1

    def __str__(self):
        return_string = str(self.itself) + ":\n"
        for usage in self.usages:
            return_string += usage + " : " + str(self.usages[usage]) + ", "
        return return_string


class Dictionary():  # должен содержать все слова как ключи, но только нужные части речи как значения
    def __init__(self):
        self.acceptable_pos = ["Pltm", "Fixd", "Femn", "ADJF", "PRTF"]  # to work on
        self.content = {}
        for pos in self.acceptable_pos:
            self.content[pos] = []

    def add(self, word, next_word):
        group_name = word.tag.gender if "NOUN" in word.tag else word.tag.POS
        if "Pltm" in word.tag:
            group_name = "Pltm"
        if "Fixd" in word.tag:
            group_name = "Fixd"
        for word in dict[group_name]:
            if word.itself == Word(word):
                word.add_next(next_word)
                return 0
        dict[group_name].append(Word_usage(word, next_word))


def find_sentences(corpus, percent):
    acceptable_pos = ["NOUN", "ADJF", "PRTF"]
    for i in "?!":
        corpus = corpus.replace(i, ".")
    for i in ".,:?!()":
        corpus = corpus.replace(i, " " + i)
    sentences = corpus.split(".")
    while True:
        sentence = random.choice(sentences)
        useful_content = 0
        if len(sentence) < 10:
            continue
        for word in sentence.split():
            useful_content += condition(Word(word))
        coefficient = useful_content / len(sentence.split())
        if coefficient > percent and len(sentence.split()) > 3:
            return sentence


def condition(word):
    acceptable_pos = ["NOUN", "ADJF", "PRTF"]
    for pos in acceptable_pos:
        if pos in word.tag and "Apro" not in word.tag:
            return True
    return False


def generate(string, dict):
    string = string.replace(".", "")
    words = string.split()
    output = ""
    for word in words:
        word = Word(word)
        # print(i)
        if condition(word):
            group_name = word.tag.gender if "NOUN" in word.tag else word.tag.POS
            if "Pltm" in word.tag:
                group_name = "Pltm"
            if "Fixd" in word.tag:
                group_name = "Fixd"
            random_word = random.choice(dict[group_name]).get
            output += Word(random_word).inflect(word.tag) + " "
        else:
            output += word.get + " "
    return output


def create_dictionary(corpus):
    for i in ".,:?!-—()":
        corpus = corpus.replace(i, "")
    corpus = corpus.split()
    dict = {}
    for word in corpus:
        word = Word(word)
        if condition(word) and \
                "Sgtm" not in word.tag:
            group_name = word.tag.gender if "NOUN" in word.tag else word.tag.POS
            if "Pltm" in word.tag:
                group_name = "Pltm"
            if "Fixd" in word.tag:
                group_name = "Fixd"
            try:
                dict[group_name].append(word)
            except:
                dict[group_name] = [word]
    return dict


if __name__ == "__main__":
    f = open("corpus/lord_of_the_flies.txt", encoding="utf-8")
    corpus = f.read()
    f.close()
    dict = create_dictionary(corpus)

    for i in range(0, 10):
        s = find_sentences(corpus, 0.6)
        # s = "Человеческой глупости нет предела."
        # s = "Три человека и я с давних времен вся история, которая в драматическом рассказе обязательно красива и безучастна - начало, середина и завершение"
        # print(s)
        print(generate(s, dict))
