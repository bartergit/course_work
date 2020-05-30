from pickle_manip import load_pickle_obj
import re
from dictionary import format_word
import random


def create_markov_dictionary(sentences):
    dict = {}
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
            try:
                if word not in dict:
                    dict[word] = {}
                if sentence[ind + 1] in dict[word]:
                    dict[word][sentence[ind + 1]] += 1
                else:
                    dict[word][sentence[ind + 1]] = 1
            except:
                if word not in dict:
                    dict[word] = {}
                if "." in dict[word]:
                    dict[word]["."] += 1
                else:
                    dict[word]["."] = 1
    return dict


def generate(final_dict):
    current_word = random.choice(list(final_dict.keys()))
    output = current_word
    while current_word != ".":
        try:
            current_word = random.choices(population=list(final_dict[current_word].keys()),
                                          weights=list(final_dict[current_word].values()))[0]
        except:
            current_word = random.choices(population=list(dict[current_word].keys()),
                                          weights=list(dict[current_word].values()))[0]
        output += " " + current_word
    output = output.replace(" ,", ",")
    output = output.replace(" .", ".")
    output = output[:1].upper() + output[1:]
    return output


if __name__ == "__main__":
    sentences = load_pickle_obj("corpus/ru_books")
    dict = create_markov_dictionary(sentences)
    final_dict = {}
    for word in list(dict):
        sum = 0
        for d in dict[word]:
            sum += dict[word][d]
        if sum > 10:
            final_dict[word] = dict[word]
    # print(dict)
    for i in range(10):
        print(generate(final_dict))
