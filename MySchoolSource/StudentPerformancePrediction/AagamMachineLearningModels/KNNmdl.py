# import pickle
# import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
# import sklearn
# from django.forms import model_to_dict
# from sklearn.neighbors import KNeighborsClassifier
#
# from MySchoolHome import models as msh
# from StudentPerformancePrediction import models
# from aagam_packages.terminal_yoda.terminal_yoda import *
#
#
# yoda_saberize_print(sklearn.__version__, YodaSaberColor.WHITESMOKE, YodaSaberColor.GREEN)
# yoda_saberize_print(matplotlib.__version__, YodaSaberColor.WHITESMOKE, YodaSaberColor.GREEN)
#
#
# def get_dataset_for_knn():
#     efficacy_data = models.StudentEfficacy.objects.all()
#     features = efficacy_data.values_list('father_education', 'internet_facility', 'study_time',
#                                          'paid_tuition', 'past_failures', 'free_time', 'extra_curricular_activities',
#                                          'absences', 'past_marks', 'past_marks1', 'class_engagement', 'health')
#     labels = efficacy_data.values_list('group')
#     np_features = np.array(features)
#     np_labels = np.array(labels)
#     return np_features, np_labels
#
#
# def train_k_nearest_neighbor_model():
#     feature_dataset, label_dataset = get_dataset_for_knn()
#
#     train_features, test_features, train_labels, test_labels = \
#         sklearn.model_selection.train_test_split(feature_dataset, label_dataset, test_size=0.9, shuffle=True)
#
#     best_accuracy = 0
#     error_rate = []
#     for i in range(1, 40):
#         train_features, test_features, train_labels, test_labels = \
#             sklearn.model_selection.train_test_split(feature_dataset, label_dataset, test_size=0.9, shuffle=True)
#
#         mdl_k_nearest_neighbor = KNeighborsClassifier(n_neighbors=i)
#
#         mdl_k_nearest_neighbor.fit(train_features, train_labels.ravel())
#         accuracy = mdl_k_nearest_neighbor.score(test_features, test_labels)
#
#         predicted = mdl_k_nearest_neighbor.predict(test_features)
#         error_rate.append(np.mean(predicted != test_labels))
#
#         if best_accuracy < accuracy:
#             with open("StudentPerformancePrediction/AagamMachineLearningModels/mdl_k_nearest_neighbor.pickle", "wb") as knn_file:
#                 pickle.dump(mdl_k_nearest_neighbor, knn_file)
#             best_accuracy = accuracy
#
#     plt.figure(figsize=(10, 6))
#     plt.plot(range(1, 40), error_rate, color='blue', linestyle='dashed',
#              marker='o', markerfacecolor='red', markersize=10)
#     plt.title('Error Rate vs. K Value')
#     plt.xlabel('K')
#     plt.ylabel('Error Rate')
#     print("Minimum error:-", min(error_rate), "at K =", error_rate.index(min(error_rate)))
#
#     yoda_saberize_print(best_accuracy, YodaSaberColor.WHITESMOKE, YodaSaberColor.BLUEVIOLET)
#
#     is_debugger_attached = bool(__debug__)
#     if is_debugger_attached:
#         pickled_model = open("StudentPerformancePrediction/AagamMachineLearningModels/mdl_k_nearest_neighbor.pickle", "rb")
#         mdl_k_nearest_neighbor = pickle.load(pickled_model)
#
#         predicted = mdl_k_nearest_neighbor.predict(test_features)
#         yoda_saberize_print(predicted, YodaSaberColor.WHITESMOKE, YodaSaberColor.HOTPINK)
#         names = ["Top", "Average"]
#
#         count = 0
#         for x in range(len(predicted)):
#             if names[predicted[x]] == names[test_labels.ravel()[x]]:
#                 count += 1
#
#         print(f'{count}/{len(predicted)}')
#
#
# def fetch_prediction_data(user):
#     efficacy_data = models.StudentEfficacy.objects.get(student=user.pk)
#
#     features = list(model_to_dict(efficacy_data, exclude=["group", "predictions", "student_efficacy_id", "student"])
#                     .values())
#     labels = list(model_to_dict(efficacy_data, fields=["group"]).values())
#
#     feature_dataset = np.array(features)
#     label_dataset = np.array(labels)
#     feature_dataset = feature_dataset.reshape(1, -1)
#     label_dataset = label_dataset.reshape(1, -1)
#
#     pickled_model = open("StudentPerformancePrediction/AagamMachineLearningModels/mdl_k_nearest_neighbor.pickle", "rb")
#     mdl_k_nearest_neighbor = pickle.load(pickled_model)
#
#     names = ["Top", "Average"]
#
#     predicted = mdl_k_nearest_neighbor.predict(feature_dataset)
#
#     return names[predicted[0]], names[label_dataset[0][0]]
