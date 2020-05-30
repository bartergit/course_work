import pymorphy2
import re

morph = pymorphy2.MorphAnalyzer()


class Word:
    def __init__(self, word):
        self.objs = morph.parse(word)
        self.obj = self.objs[0]
        self.get = self.obj[0]
        self.tag = self.obj.tag
        self.first_form = self.obj[2]

    def inflect(self, tag):
        tags = set()
        # if tag.aspect is not None:
        #     print(tag.aspect)
        #     tags.add(tag.aspect)
        if tag.number is not None\
                and "Sgtm" not in self.tag and "Pltm" not in self.tag and "Fixd" not in self.tag:
            # print(tag.number)
            tags.add(tag.number)
        # if tag.tense is not None:
        #     # print(tag.tense)
        #     tags.add(tag.tense)
        if tag.case is not None:
            # print(tag.case)
            tags.add(tag.case)
        if "pres" in tag and tag.person is not None:
            # print(tag.person)
            tags.add(tag.person)
        if "past" in tag or "ADJF" in tag and "plur" not in tag and tag.gender is not None:
            # print(tag.gender)
            tags.add(tag.gender)
        if len(tags) == 0 or None in tags:
            return self.get
        if self.obj.inflect(tags) is None:
            return self.get
        else:
            return self.obj.inflect(tags)[0]


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
                              weights=list(self.usages[group_name].values()))

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
