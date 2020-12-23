from math import floor, ceil

from django.forms import model_to_dict

from aagam_packages.terminal_yoda.terminal_yoda import *

import pickle
import sklearn
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

from StudentPerformancePrediction import models

yoda_saberize_print(sklearn.__version__, YodaSaberColor.WHITESMOKE, YodaSaberColor.GREEN)
yoda_saberize_print(matplotlib.__version__, YodaSaberColor.WHITESMOKE, YodaSaberColor.GREEN)


def get_dataset_for_linear():
    efficacy_data = models.StudentEfficacy.objects.all()

    features = efficacy_data.values_list('father_education', 'internet_facility', 'study_time',
                                                 'paid_tuition', 'past_failures', 'free_time',
                                                 'extra_curricular_activities',
                                                 'absences', 'past_marks', 'past_marks1', 'class_engagement', 'health')
    labels = efficacy_data.values_list('predictions')

    np_features_avg = np.array(features)
    np_labels_avg = np.array(labels)

    return np_features_avg, np_labels_avg


def train_linear_regression_model():
    test_features = list()
    test_labels = list()

    feature_dataset, label_dataset = get_dataset_for_linear()

    best_accuracy = 0
    for i in range(10000):
        train_features, test_features, train_labels, test_labels = \
            sklearn.model_selection.train_test_split(feature_dataset, label_dataset, test_size=0.9)

        mdl_linear_regression = linear_model.LinearRegression()

        mdl_linear_regression.fit(train_features, train_labels)
        accuracy = mdl_linear_regression.score(test_features, test_labels)

        if best_accuracy < accuracy:
            with open("StudentPerformancePrediction/MachineLearningModels/mdl_linear_regression.pickle", "wb") as regression_file:
                pickle.dump(mdl_linear_regression, regression_file)

            best_accuracy = accuracy

    print(best_accuracy)

    is_debugger_attached = bool(__debug__)
    if is_debugger_attached:
        pickled_model = open("StudentPerformancePrediction/MachineLearningModels/mdl_linear_regression.pickle", "rb")
        mdl_linear_regression = pickle.load(pickled_model)

        predicted_labels = mdl_linear_regression.predict(test_features)

        count = 0
        b = 0
        for x in predicted_labels:
            up = ceil(x) + 1
            down = floor(x) - 1
            print(f'\t\t\t test:{down} : {test_labels[b]} : {up}')
            if down <= test_labels[b] <= up:
                print(f'{x} : {floor(test_labels[b])}')
                count += 1
            b += 1
        print(f'{count}/{len(predicted_labels)}')

        print(f'Coefficients: {mdl_linear_regression.coef_}')
        print(f'Mean squared error: {mean_squared_error(test_labels, predicted_labels)}')
        print(f'Coefficient of determination: {r2_score(test_labels, predicted_labels)}')


def fetch_prediction_data(user):
    efficacy_data = models.StudentEfficacy.objects.get(student_efficacy_id=user)

    features = list(model_to_dict(efficacy_data, fields=['father_education', 'internet_facility', 'study_time',
                                                 'paid_tuition', 'past_failures', 'free_time',
                                                 'extra_curricular_activities',
                                                 'absences', 'past_marks', 'past_marks1', 'class_engagement', 'health'])
                    .values())
    labels = list(model_to_dict(efficacy_data, fields=["predictions"]).values())

    feature_dataset = np.array(features)
    label_dataset = np.array(labels)
    feature_dataset = feature_dataset.reshape(1, -1)
    label_dataset = label_dataset.reshape(1, -1)

    pickled_model = open("StudentPerformancePrediction/MachineLearningModels/mdl_linear_regression.pickle", "rb")
    mdl_linear_regression = pickle.load(pickled_model)

    predicted = mdl_linear_regression.predict(feature_dataset)

    return predicted, label_dataset, efficacy_data.student
