import pickle

def save_pickle_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, 0)


def load_pickle_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
