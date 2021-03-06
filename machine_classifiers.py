""" Experimenting with some models, def 'run_classifier' adapted from
http://scikit-learn.org/stable/auto_examples/ensemble/plot_voting_decision_regions.html
"""
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.metrics import confusion_matrix
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

import regression
import utils.machine_learning_helpers as hp


def run_classifiers(x, xt, y, yt, cols):
    models = ['Tree', 'SVC', 'MPL', 'Voting']

    m1 = RandomForestClassifier(n_estimators=10000, criterion='gini', bootstrap=True, max_depth=15)
    m3 = SVC(C=1, kernel='linear', degree=3, probability=True)
    m4 = MLPClassifier(solver='lbfgs', early_stopping=True, activation='tanh', max_iter=2000)
    voting = VotingClassifier(estimators=[('dt', m1), ('svc', m3), ('neural', m4)],
                              voting='soft')

    # Fitting models
    cls = [m1, m3, m4, voting]
    # cls = [m1]
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
    feat1 = features(m1, cols, fores=True)
    feat2 = features(m3, cols, sv=True)
    # Returns a dictionary of models' names and the model itself
    return cls, feat1, feat2


def features(forest, cols, fores=False, sv=False):
    if fores:
        feat = forest.feature_importances_
        feature = pd.DataFrame(feat,
                               index=cols,
                               columns=['importance']).sort_values('importance', ascending=False)
    # Else is SVM
    if sv:
        feat = forest.coef_
        feat = pd.DataFrame(feat.T, columns=['importance'])
        feat = (feat['importance'] + feat['importance'].min() * -1).to_frame()
        feat = (feat.importance / feat.importance.max()).to_frame()
        feature = (feat.importance/sum(feat.importance)).to_frame()
        feature.index = cols
    print(feature.head(8))
    return feature


def basics():
    # Get data, train, test
    gen = False
    d = regression.get_data(100, gen)
    X, Y, cols = regression.prepare_data(d, machine=True)
    X_train, X_test, y_train, y_test = hp.divide_data(X, Y)
    return X_train, X_test, y_train, y_test, cols


if __name__ == '__main__':
    X_train, X_test, y_train, y_test, C = basics()
    l_models, f1, f2 = run_classifiers(X_train, X_test, y_train, y_test, C)
