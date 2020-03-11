from sklearn.model_selection import train_test_split
from sklearn.preprocessing import normalize


def predict(model, data):
    return model.predict(data)


def fit(model, a, b):
    model.fit(a, b)


def divide_data(x, y):
    # Train and test data
    return train_test_split(x, y, test_size=0.3)


def normalize_trial(x, xt):
    n = []
    for each in [x, xt]:
        n.append(normalize(each.as_matrix()))
    return n[0], n[1]
