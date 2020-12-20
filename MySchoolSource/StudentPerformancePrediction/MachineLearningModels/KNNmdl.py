import pickle
import numpy as np
import matplotlib
import sklearn
from sklearn.neighbors import KNeighborsClassifier

from StudentPerformancePrediction import models
from aagam_packages.terminal_yoda.terminal_yoda import *


yoda_saberize_print(sklearn.__version__, YodaSaberColor.WHITESMOKE, YodaSaberColor.GREEN)
yoda_saberize_print(matplotlib.__version__, YodaSaberColor.WHITESMOKE, YodaSaberColor.GREEN)


def get_dataset():
    efficacy_data = models.StudentEfficacy.objects.all()
    features = efficacy_data.values_list('father_education', 'internet_facility', 'study_time',
                                         'paid_tuition', 'past_failures', 'free_time', 'extra_curricular_activities',
                                         'absences', 'past_marks', 'past_marks1', 'class_engagement', 'health')
    labels = efficacy_data.values_list('group')
    np_features = np.array(features)
    np_labels = np.array(labels)
    return np_features, np_labels


def train_k_nearest_neighbor_model():
    test_features = list()
    test_labels = list()

    feature_dataset, label_dataset = get_dataset()

    best_accuracy = 0
    for i in range(100):
        train_features, test_features, train_labels, test_labels = \
            sklearn.model_selection.train_test_split(feature_dataset, label_dataset, test_size=0.9, shuffle=True)

        mdl_k_nearest_neighbor = KNeighborsClassifier(n_neighbors=3)

        mdl_k_nearest_neighbor.fit(train_features, train_labels.ravel())
        accuracy = mdl_k_nearest_neighbor.score(test_features, test_labels)
        yoda_saberize_print(f'{i} : {accuracy}', YodaSaberColor.WHITESMOKE, YodaSaberColor.BROWN)

        is_debugger_attached = bool(__debug__)
        if not is_debugger_attached:
            if best_accuracy < accuracy:
                with open("StudentPerformancePrediction/MachineLearningModels/mdl_k_nearest_neighbor.pickle", "wb") as knn_file:
                    pickle.dump(mdl_k_nearest_neighbor, knn_file)
                best_accuracy = accuracy

    yoda_saberize_print(best_accuracy, YodaSaberColor.WHITESMOKE, YodaSaberColor.BLUEVIOLET)

    is_debugger_attached = bool(__debug__)
    if is_debugger_attached:
        pickled_model = open("StudentPerformancePrediction/MachineLearningModels/mdl_k_nearest_neighbor.pickle", "rb")
        mdl_k_nearest_neighbor = pickle.load(pickled_model)

        predicted = mdl_k_nearest_neighbor.predict(test_features)
        yoda_saberize_print(predicted, YodaSaberColor.WHITESMOKE, YodaSaberColor.HOTPINK)
        names = ["Low", "Top", "Average"]

        count = 0
        for x in range(len(predicted)):
            if names[predicted[x]] == names[test_labels.ravel()[x]]:
                count += 1

        print(f'{count}/{len(predicted)}')
