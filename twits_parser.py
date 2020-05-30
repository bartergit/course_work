import re
from pickle_manip import *
from dictionary import format_sentence


def skip_comma(string, n=1):
    for i in range(n):
        ind = str.find(string, ",") + 1
        string = string[ind:]
    return string[1:]


def twits_parse():
    f = open("corpus/positive.sql", encoding="utf-8")
    output = []
    for i in range(47):  # 47
        f.readline()
    for i in range(48, 72):  # 48,72
        line = f.readline()
        while True:
            line = line[str.find(line, "(") + 1:]
            line = skip_comma(line, 3)
            index = str.find(line, "'")
            twit = line[:index]
            twit = format_sentence(twit)
            if twit == "" or str.find(twit, ", ) ;") != -1:
                break
            output.append(twit)
    f.close()
    return output


if __name__ == "__main__":
    save_pickle_obj(twits_parse(), "corpus/twits")
