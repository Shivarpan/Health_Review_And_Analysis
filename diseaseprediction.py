from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
import numpy as np,pandas as pd
import os

data = pd.read_csv("/home/axcel/Desktop/final_proj/flask-pixel-bootstrap-uikit/app/templates/Training.csv")
df = pd.DataFrame(data)
cols = df.columns
cols = cols[:-1]
x = df[cols]
y = df['prognosis']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

print ("DecisionTree")
dt = DecisionTreeClassifier()
clf_dt=dt.fit(x_train,y_train)

gnb = GaussianNB()
gnb = gnb.fit(x_train, y_train)

clf4 = RandomForestClassifier()
clf4 = clf4.fit(x_train, y_train)

log = LogisticRegression()
log = log.fit(x_train,y_train)

model = SVC()
model = model.fit(x_train,y_train)

indices = [i for i in range(132)]
symptoms = df.columns.values[:-1]

dictionary = dict(zip(symptoms,indices))

def decision_tree(symptom):
    user_input_symptoms = symptom
    user_input_label = [0 for i in range(132)]
    for i in user_input_symptoms:
        idx = dictionary[i]
        user_input_label[idx] = 1

    user_input_label = np.array(user_input_label)
    user_input_label = user_input_label.reshape((-1,1)).transpose()
    return(dt.predict(user_input_label))

def NaiveBayes(symptom):
    
    user_input_symptoms = symptom
    user_input_label = [0 for i in range(132)]
    for i in user_input_symptoms:
        idx = dictionary[i]
        user_input_label[idx] = 1

    user_input_label = np.array(user_input_label)
    user_input_label = user_input_label.reshape((-1,1)).transpose()
    return(gnb.predict(user_input_label))

def randomforest(symptom):
   user_input_symptoms = symptom
   user_input_label = [0 for i in range(132)]
   for i in user_input_symptoms:
    	idx = dictionary[i]
    	user_input_label[idx] = 1

   user_input_label = np.array(user_input_label)
   user_input_label = user_input_label.reshape((-1,1)).transpose()
   return(clf4.predict(user_input_label))

def logistic_reg(symptom):
    user_input_symptoms = symptom
    user_input_label = [0 for i in range(132)]
    for i in user_input_symptoms:
    	idx = dictionary[i]
    	user_input_label[idx] = 1

    user_input_label = np.array(user_input_label)
    user_input_label = user_input_label.reshape((-1,1)).transpose()
    return(log.predict(user_input_label))

def svm_(symptom):
    user_input_symptoms = symptom
    user_input_label = [0 for i in range(132)]
    for i in user_input_symptoms:
    	idx = dictionary[i]
    	user_input_label[idx] = 1

    user_input_label = np.array(user_input_label)
    user_input_label = user_input_label.reshape((-1,1)).transpose()
    return(model.predict(user_input_label))