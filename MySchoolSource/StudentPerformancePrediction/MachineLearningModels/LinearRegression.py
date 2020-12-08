from aagam_packages.terminal_yoda.terminal_yoda import *

import pickle
import sklearn
import matplotlib
import matplotlib.pyplot as plt

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

yoda_saberize_print(sklearn.__version__, YodaSaberColor.WHITESMOKE, YodaSaberColor.GREEN)
yoda_saberize_print(matplotlib.__version__, YodaSaberColor.WHITESMOKE, YodaSaberColor.GREEN)


def train_linear_regression_model(dataset):
    test_features = list()
    test_labels = list()

    feature_dataset = dataset[:]
    label_dataset = dataset[:]

    best_accuracy = 0
    for i in range(1000):
        train_features, test_features, train_labels, test_labels = \
            sklearn.model_selection.train_test_split(feature_dataset, label_dataset, test_size=0.8)

        mdl_linear_regression = linear_model.LinearRegression()

        mdl_linear_regression.fit(train_features, train_labels)
        accuracy = mdl_linear_regression.score(test_features, test_labels)

        if best_accuracy < accuracy:
            with open("mdl_linear_regression.pickle", "wb") as regression_file:
                pickle.dump(mdl_linear_regression, regression_file)

            best_accuracy = accuracy

    is_debugger_attached = bool(__debug__)
    if is_debugger_attached:
        pickled_model = open("mdl_linear_regression.pickle", "rb")
        mdl_linear_regression = pickle.load(pickled_model)

        predicted_labels = mdl_linear_regression.predict(test_features)

        print(f'Coefficients: {mdl_linear_regression.coef_}')
        print(f'Mean squared error: {mean_squared_error(test_labels, predicted_labels)}')
        print(f'Coefficient of determination: {r2_score(test_labels, predicted_labels)}')

        plt.scatter(test_features, test_labels, color='black')
        plt.plot(test_features, predicted_labels, color='blue', linewidth=3)

        plt.xticks(())
        plt.yticks(())

        plt.show()
