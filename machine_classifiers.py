""" Experimenting with some models, def 'run_classifier' adapted from
http://scikit-learn.org/stable/auto_examples/ensemble/plot_voting_decision_regions.html
"""
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
import pandas as pd

import regression
import utils.machine_learning_helpers as hp


def run_classifiers(x, xt, y, yt, cols):
    models = ['Tree', 'SVC', 'MPL', 'Voting']

    m1 = RandomForestClassifier(n_estimators=10000, criterion='gini', bootstrap=True, max_depth=15)
    # m3 = SVC(C=1, kernel='poly', degree=3, probability=True)
    # m4 = MLPClassifier(solver='lbfgs', early_stopping=True, activation='tanh', max_iter=2000)
    # voting = VotingClassifier(estimators=[('dt', m1), ('svc', m3), ('neural', m4)],
    #                           voting='soft')

    # Fitting models
    # cls = [m1, m3, m4, voting]
    cls = [m1]
    for each in cls:
        each.fit(x, y)

    models = dict(zip(models, cls))

    # Calculating accuracies and printing
    for key in models.keys():
        print('Score {}: {:.4f}.'.format(key, models[key].score(xt, yt)))
        # Examining confusion matrix
        y_hat = models[key].predict(xt)
        cm = confusion_matrix(yt, y_hat)
        print('Confusion Matrix {}:\n {}.'.format(key, cm))

    # Call Tree results
    feat = features(m1, cols)
    # Returns a dictionary of models' names and the model itself
    return cls, feat


def features(forest, cols):
    feature = pd.DataFrame(forest.feature_importances_,
                           index=cols,
                           columns=['importance']).sort_values('importance', ascending=False)
    print(feature.head(8))
    return feature


def basics():
    # Get data, train, test
    gen = False
    d = regression.get_data(1000, gen)
    X, Y, cols = regression.prepare_data(d)
    X_train, X_test, y_train, y_test = hp.divide_data(X, Y)
    return X_train, X_test, y_train, y_test, cols


if __name__ == '__main__':
    X_train, X_test, y_train, y_test, C = basics()
    l_models, f = run_classifiers(X_train, X_test, y_train, y_test, C)
