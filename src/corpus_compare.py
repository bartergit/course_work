from pickle_manip import load_pickle_obj
import random
from dictionary import create_dictionary, format_word
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import numpy as np
from _word_declaration import Word
from pure_markov import create_markov_dictionary


def graph(path,color):
    arr = load_pickle_obj(path)
    symbols = 0
    for sentence in arr:
        symbols += len(sentence)
    y1 = [0]
    y2 = [0]
    y3 = [0]
    q1 = 0
    q2 = 0
    q3 = 0
    x = np.linspace(0, len(arr), num=4, endpoint=True)
    dict = create_dictionary(arr)
    dict_markov = create_markov_dictionary(arr)
    for ind in range(len(x) - 1):
        for word in list(dict.keys())[ind*int(len(dict)/4):(ind+1)*int(len(dict)/4)]:
            if dict[word] > 2:
                q1 += 1
            if dict[word] > 5:
                q2 += 1
        for word in list(dict_markov.keys())[ind*int(len(dict_markov)/4):(ind+1)*int(len(dict_markov)/4)]:
            sum = 0
            if len(dict_markov[word]) > 10:
                q3 += 1
        y1.append(q1)
        y2.append(q2)
        y3.append(q3)
    print("Количество предложений: {:,}".format(len(arr)))
    print("Количество символов: {:,}".format(symbols))
    print("Количество форм слов: {:,}".format(len(dict)))
    print("Количество слов, у которых больше одного повторения {:,}".format(q1))
    print("Количество слов, у которых больше одного повторения {:,}".format(q2))
    print("Количество слов, у которых больше четырёх вариантов выбора {:,}".format(q3))
    print("Качество словаря (1 и 2)",
          int(q1 / len(dict) *1000)/10,
          int(q2 / len(dict)*1000)/10)
    print("Пример предложения: ", arr[random.randint(0, len(arr) - 1)])
    f1 = interp1d(x, y1, kind='cubic')
    f2 = interp1d(x, y2, kind='cubic')
    f3 = interp1d(x, y3, kind='cubic')
    xnew = np.linspace(0, len(arr), num=40, endpoint=True)
    plt.plot(x, y1, 'o', x, y2, 'o',
             xnew, f1(xnew), '-',
             xnew, f2(xnew), '--',
             xnew, f3(xnew), '+', color=color)
    print("-------------")


if __name__ == "__main__":
    colors = [(0, 0, 0), (0.5, 0.5, 0.5), (1, 0.3, 0.3), (0,0,1)]
    graph("corpus/twits", colors[0])
    graph("corpus/xml", colors[1])
    graph("corpus/ru_books", colors[2])
    # graph("corpus/eng_books", colors[3])
    # graph("corpus/xml")
    plt.show()