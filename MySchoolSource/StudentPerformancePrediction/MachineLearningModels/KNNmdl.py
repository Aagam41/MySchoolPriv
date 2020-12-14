from aagam_packages.terminal_yoda.terminal_yoda import *

import pickle
import sklearn
import matplotlib

from sklearn.neighbors import KNeighborsClassifier

yoda_saberize_print(sklearn.__version__, YodaSaberColor.WHITESMOKE, YodaSaberColor.GREEN)
yoda_saberize_print(matplotlib.__version__, YodaSaberColor.WHITESMOKE, YodaSaberColor.GREEN)


def train_k_nearest_neighbor_model(dataset):
    test_features = list()
    test_labels = list()

    feature_dataset = dataset
    label_dataset = dataset

    best_accuracy = 0
    for i in range(1000):
        train_features, test_features, train_labels, test_labels = \
            sklearn.model_selection.train_test_split(feature_dataset, label_dataset, test_size=0.8)

        mdl_k_nearest_neighbor = KNeighborsClassifier(n_neighbors=5)

        mdl_k_nearest_neighbor.fit(train_features, train_labels)
        accuracy = mdl_k_nearest_neighbor.score(test_features, test_labels)

        if best_accuracy < accuracy:
            with open("mdl_k_nearest_neighbor.pickle", "wb") as knn_file:
                pickle.dump(mdl_k_nearest_neighbor, knn_file)
            best_accuracy = accuracy

    is_debugger_attached = bool(__debug__)
    if is_debugger_attached:
        pickled_model = open("mdl_k_nearest_neighbor", "rb")
        mdl_k_nearest_neighbor = pickle.load(pickled_model)

        predicted = mdl_k_nearest_neighbor.predict(test_features)
        names = ["Low, Average, Top"]

        for x in range(len(predicted)):
            yoda_saberize_print(
                f'Predicted: {names[predicted[x]]}  Data: {test_features[x]}  Actual: {names[test_labels[x]]}',
                YodaSaberColor.BLUEVIOLET, YodaSaberColor.WHITESMOKE)
            n = mdl_k_nearest_neighbor.kneighbors([test_features[x]], 5, True)
            yoda_saberize_print(f'N: {n}', YodaSaberColor.BLUEVIOLET, YodaSaberColor.WHITESMOKE)
