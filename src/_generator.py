import random

import re

from pickle_manip import load_pickle_obj, save_pickle_obj

from _word_declaration import Word

group_names = ["Pltm", "Fixd",
               "neut", "masc", "ms-f", "femn",  # ms-f is not usable i believe
               "ADJF", "PRTF"]


def is_acceptable_pos(word):
    acceptable_pos = ["NOUN", "ADJF", "PRTF"]
    for pos in acceptable_pos:
        if pos in word.tag and "Apro" not in word.tag:
            return True
    return False


def determine_group(word):
    group_name = word.tag.gender if "NOUN" in word.tag else word.tag.POS
    if "Pltm" in word.tag:
        group_name = "Pltm"
    if "Fixd" in word.tag:
        group_name = "Fixd"
    return group_name


class Smart_Word():
    def __init__(self, word):
        self.itself = Word(word).first_form
        self.usages = {}
        for name in group_names:
            self.usages[name] = {}

    def add_next(self, next_word):
        next_word = Word(next_word)
        if is_acceptable_pos(next_word):
            group_name = determine_group(next_word)
            next_word = next_word.first_form
            try:
                self.usages[group_name][next_word] += 1
            except:
                self.usages[group_name][next_word] = 1

    def predict_next(self, group_name):
        return random.choices(population=list(self.usages[group_name].keys()),
                              weights=list(self.usages[group_name].values()))[0]

    def __eq__(self, other):
        if self.itself == other.itself:
            return True
        else:
            return False

    def __str__(self):
        return_string = str(self.itself) + ":\n"
        for usage in self.usages:
            return_string += usage + " : " + str(self.usages[usage]) + ", "
        return return_string


def find_sentences(corpus, percent):
    acceptable_pos = ["NOUN", "ADJF", "PRTF"]
    while True:
        sentence = random.choice(corpus)
        s = sentence
        sentence = re.split('; | |!|\.|\?', sentence)
        new_sentence = []
        for i in sentence:
            if i != '':
                new_sentence.append(i)
        sentence  = new_sentence
        useful_content = 0
        if len(sentence) < 4:
            continue
        for word in sentence:
            useful_content += is_acceptable_pos(Word(word))
        coefficient = useful_content / len(sentence)
        if coefficient > percent:
            print(s)
            return sentence


#  i

def generate(sentence, dict):
    #add punctuation
    ' '.join(sentence)
    try:
        group_name = str(determine_group(Word(sentence[0])))
        if group_name == 'PRTF':
            group_name = 'ADJF'
        current = random.sample(pos_dict[group_name], 1)[0]
        current = Word(current).inflect(Word(sentence[0]).tag)
    except:
        current = sentence[0]
    output = current[0].upper() + current[1:] + " "
    prev_word = current
    for ind, word in enumerate(sentence[1:]):
        # print(is_acceptable_pos(Word(word)),word)
        if is_acceptable_pos(Word(word)):
            try:
                current = dict[Word(prev_word).first_form].predict_next(
                    determine_group(Word(word)))
                current = Word(current).inflect(Word(word).tag) #.upper()
            except:
                group_name = str(determine_group(Word(word)))
                if group_name == 'PRTF':
                    group_name = 'ADJF'
                current = random.sample(pos_dict[group_name],1)[0]
                current = Word(current).inflect(Word(word).tag) #.upper()
                # print(current, end="|")
        else:
            current = word
        if current in "; ,!.?":
            output = output[:-1] + current + " "
        else:
            output += current + " "
        prev_word = current
    output = output[:-1] + "."
    return output

def create_dictionary(corpus):
    list = {}
    for sentence in corpus:
        sentence = re.sub(r'\s+', ' ', sentence)
        sentence = re.split('[, \-()]', sentence)
        new_sentence = []
        for s in sentence:
            if s != "":
                new_sentence.append(s)
        sentence = new_sentence
        for ind, word in enumerate(sentence[:-1]):
            word_markov = Smart_Word(word)
            if Word(word).first_form in list:
                list[Word(word).first_form].add_next(sentence[ind + 1])
            else:
                word_markov.add_next(sentence[ind + 1])
                list[Word(word).first_form] = word_markov
    return list

def create_POS_dict(corpus):
    return_d = {}
    for sentence in corpus:
        sentence = re.sub(r'\s+', ' ', sentence)
        sentence = re.split('[, \-()]', sentence)
        for w in sentence:
            if is_acceptable_pos(Word(w)):
                try:
                    name = str(determine_group(Word(w)))
                    w = Word(w).first_form
                    return_d[name].add(w)
                except:
                    name = str(determine_group(Word(w)))
                    w = Word(w).first_form
                    return_d[name] = {w}
    return return_d

# использует местоимения - не стоит
# исключить слова, у которых нет каких-либо форм, а также неизменяемых и т д
# add ADJS - кр прил   https://pymorphy2.readthedocs.io/en/latest/user/grammemes.html
#    comp - сравнение
# имена собственные
# Знаки препинания
# корпус
# причастия неправильно склоняются!!
# если корпус большой - удалять очень редкие слова
# числительные

if __name__ == "__main__":
    random.seed(10)
    corpus = load_pickle_obj("corpus/ru_books")
    # pos_dict = create_POS_dict(corpus)
    # save_pickle_obj(pos_dict, "corpus/ru_books_pos")
    pos_dict = load_pickle_obj("corpus/ru_books_pos")
    # dict = create_dictionary(corpus)
    # save_pickle_obj(dict, "corpus/ru_books_dict")
    dict = load_pickle_obj("corpus/ru_books_dict")
    print(dict["турнир"])
    # d = [' Государство кривых зеркал ',
    #      'Доказательная овощебаза',
    #      'Зомби — наше будущее',
    #      'Налоговый плюс на валовый минус',
    #      'Нашла касса на камень',
    #      "Кругом были жилые дома , и в одном из них , возможно , проживала чья - то зазноба",
    #      'Согласно определению , повествовательное предложение рассказывает о каких-то фактах и явлениях , а также чувствах и мыслях говорящего , то есть цель этого высказывания заключается в том , чтобы о чем-то рассказать.' ]
    d = ['Без русского языка не сколотишь и сапога .', 'Без языка и колокол нем .', 'Блюди хлеб на обед , а слово - на ответ .' ,
     'Будь своему слову господин .' , 'Где слова редки , там они вес имеют .' , 'Глупые речи - что пыль на ветру .' ,
     'Говори по делу , живи по совести .' , 'Говорит про тебя , забыв себя .' , 'Доброе молчанье лучше худого ворчанья .' ,
     'Доброе слово человеку - что дождь в засуху .' , 'Долго не говорит - ум копит , а вымолвит - слушать нечего .' ,
     'Думай дважды , говори раз .' , 'Жало остро , а язык — острей того .' , 'Каков ум , такова и речь .' ,
     'Какова речь , таков и склад .' , 'Колокольный звон не молитва , крик не беседа .' ,
     'Коня на вожжах удержишь , а слова с языка не воротишь .' , 'Красно поле пшеном , а беседа умом .' ,
     'Кто говорит , тот сеет; кто слушает — собирает ( пожинает ) .' , 'Кто ясно мыслит , тот ясно излагает .' ,
     'Лучше недосказать , чем пересказать .' , 'Лучше скажи мало , но хорошо .' , 'Лучше споткнуться ногою , нежели словом .' ,
     'Мал язык , да всем телом владеет .' , 'Молва без крыльев , а летает .' , 'Не всякая пословица при всяком молвится .' ,
     'Не пройми копьем , пройми языком!' , 'Невысказанное слово порой гремит , как гром .',
     'Недолгая речь хороша , а долгая – поволока .' ,
     'Неискренние слова , как спутанные волосы на голове: распутать их – трудное дело .' ,
     'Острый язык — дарование , а длинный — наказание .' , 'Острый язык змею из гнезда выманит .' ,
     'Перо всегда смелее языка .' , 'Песнь не околица , глупая речь не пословица .' ,
     'Правдивое слово - как лекарство: горько , зато излечивает .' , 'Проврался , что прокрался .' ,
     'Сердце громче стонет , когда молчишь .' , 'Сказанное слово - потерянное , не сказанное - свое .' ,
     'Слово - олово ( т .е . тяжело , веско )' , 'Слово держать - не по ветру бежать .' , 'Слово не стрела , а сердце язвит .' ,
     'Сперва подумай , а там и нам скажи .' , 'Старинная пословица не мимо молвится .' , 'У дурака язык опаснее кинжала .',
     'Что написано пером , не вырубишь топором .' , 'Что сказано , то свято .' ,
     'Язык — стяг , дружину водит . Язык царствами ворочает .' , 'Язык поит и кормит , и спину порет .' ,
     'Язык разум открывает .' , 'Язык языку ответ даёт, а голова смекает .', 'Язык – телу якорь . ']
    for i in d:
        print(generate(i.split(),dict))
    for i in d:
        print(generate(i.split(),dict))
    # for i in range(0, 5):
    #     s = find_sentences(corpus, 0.7)
    #     print(generate(s, dict))


