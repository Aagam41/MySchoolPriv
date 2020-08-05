import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import sklearn.metrics
from MySchool.StudentPerformance import models
import matplotlib.pyplot as plt
import os,csv
import zipfile
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
import glob, keras
from keras.utils import np_utils
from keras import regularizers
from keras.models import Sequential,load_model
from keras.utils.np_utils import to_categorical
from sklearn import preprocessing
from keras.layers import Dense, Dropout


xTrain, xTest, yTrain, yTest = train_test_split(X, Y, test_size=0.15)
#Perform one hot encoding
x_train = pd.get_dummies(xTrain)
x_test = pd.get_dummies(xTest)
y_train  = pd.get_dummies(yTrain)
y_test  = pd.get_dummies(yTest)

model = Sequential()
model.add(Dense(64, activation='relu',  kernel_regularizer=regularizers.l2(0.001),input_shape = (58,)))
model.add(Dense(64, kernel_regularizer=regularizers.l2(0.001), activation='relu'))
model.add(Dense(32, kernel_regularizer=regularizers.l2(0.001), activation='relu'))
model.add(Dense(5,  kernel_regularizer=regularizers.l2(0.001),activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
knnFittedModel  = model.fit(x_train,y_train, epochs = 200, batch_size = 5, validation_data = (x_test,y_test))

knnFittedModel.summary()
results = knnFittedModel.evaluate(x_test,y_test)
print("Accuracy of the Model %.2f%%" % ( results[1]*100))