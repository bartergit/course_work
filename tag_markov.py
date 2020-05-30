from _word_declaration import Word
import re
import random
from pickle_manip import load_pickle_obj, save_pickle_obj


def create_markov_dictionary(sentences):
    dict = {}
    worder = {}
    for sentence in sentences:
        sentence = sentence.lower()
        sentence = re.sub(r'\s+', ' ', sentence)
        sentence = re.split(' ', sentence)
        new_sentence = []
        for s in sentence:
            if s != "":
                new_sentence.append(s)
        sentence = new_sentence
        for ind, word in enumerate(sentence):
            word = Word(word).tag if "PNCT" not in Word(word).tag else word
            try:
                if sentence[ind] not in worder[word]:
                    worder[word].append(sentence[ind])
            except:
                worder[word] = [sentence[ind]]
            try:
                next_sentence = Word(sentence[ind + 1]).tag if "PNCT" not in Word(sentence[ind + 1]).tag else sentence[ind+1]
            except:
                next_sentence = "."
            if word not in dict:
                dict[word] = {}
            if next_sentence in dict[word]:
                dict[word][next_sentence] += 1
            else:
                dict[word][next_sentence] = 1
    worder[Word(".").tag] = ["."]
    return dict, worder


def generate(final_dict):
    current_word = random.choice(list(final_dict.keys()))
    output = ""
    while str(current_word) != ".":
        try:
            current_word = random.choices(population=list(final_dict[current_word].keys()),
                                          weights=list(final_dict[current_word].values()))[0]
        except:
            current_word = random.choices(population=list(dict[current_word].keys()),
                                          weights=list(dict[current_word].values()))[0]
        # print(worder[current_word])
        if str(current_word) == ".":
            break
        output += " " + random.choice(worder[current_word])
    output = output.replace(" ,", ",")
    output = output.replace(" .", ".")
    output = output[1:]
    output = output[:1].upper() + output[1:] + "."
    return output


if __name__ == "__main__":
    # print(str(Word("человек").tag) == str(Word("мужчина").tag))
    d = load_pickle_obj("corpus/ru_books")
    d1 = d[:100]
    d2 = d[:10000]
    dict1, worder = create_markov_dictionary(d1)
    dict2, worder2 = create_markov_dictionary(d2)
    print(len(dict1),len(dict2))
    for i in range(7):
        sentence = generate(dict1)
        if sentence != ".":
            print(sentence)

