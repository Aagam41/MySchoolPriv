import tensorflow
import keras
import numpy as np
import pandas as pd
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

style.use("ggplot")

data = pd.read_csv("student-mat.csv", sep=";")

predict = "G3"

data = data[["G1","G2","G3","studytime","failures","absences","sex", "age", "Medu", "Fedu", "schoolsup", "famsup", "paid", "activities", "nursery", "higher", "internet","famrel", "freetime", "goout", "health"]]

data = data.replace(['yes'],'1')
data = data.replace(['no'],'0')
data = data.replace(['F'],'0')
data = data.replace(['M'],'1')

names = []
for i in range(len(data.index)):
    names = np.append(names,[str(i) + ' Aagam'], axis=0)

data['Names'] = names

x = np.array(data.drop([predict], 1))
y = np.array(data[predict])


pickle_in = open("studentmodel.pickle", "rb")
linear = pickle.load(pickle_in)

print('Coefficient: \n', linear.coef_)
print('Intercept: \n', linear.intercept_)

for x1 in x:
    x2 = x1[20]
    x1 = np.delete(x1,20)
    x1 = x1.reshape(1,-1)
    predicted = linear.predict(x1)
    x1 = np.append(x1,x2)
    print(predicted, x1)

plot = "G1"
plt.scatter(data[plot], data["G3"])
plt.xlabel(plot)
plt.ylabel("Final Grade")
plt.show()