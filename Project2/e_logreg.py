from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import confusion_matrix
import numpy as np
import math
import importlib
import functions
importlib.reload(functions)
from functions import *
from sklearn.preprocessing import StandardScaler
np.random.seed(2405) # Set a random seed



data = load_breast_cancer()
x = data['data']
y = data['target']
scaler = StandardScaler()
scaler.fit(x)
x = scaler.transform(x)


X_train, X_test, y_train, y_test = train_test_split(x,y,test_size=0.2) #Split the data into training and test sets


eta_vals = [0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 1]#
lmbd_vals = [0, 0.0001, 0.001, 0.01, 0.1, 1] #

n_epochs = 150


test_accuracy = np.zeros((len(eta_vals), len(lmbd_vals)))
test_accuracy_sklearn = np.zeros((len(eta_vals), len(lmbd_vals)))

k=0
for i in range(len(eta_vals)):
    for j in range(len(lmbd_vals)):
        print(k)
        k+=1
        test_accuracy[i][j] = kfold_logistic(x, y, 5, lmbd_vals[j], eta_vals[i], n_epochs, sklearn = False)
        test_accuracy_sklearn[i][j] = kfold_logistic(x, y, 5, lmbd_vals[j], eta_vals[i], n_epochs, sklearn = True)

make_heatmap(test_accuracy, lmbd_vals, eta_vals, fn = f"logistic_reg.pdf",
            xlabel = "$\lambda$ values", ylabel = "$\eta$ values", title = "Accuracy score logistic regression")

make_heatmap(test_accuracy_sklearn, lmbd_vals, eta_vals, fn = f"logistic_reg_sklearn.pdf",
            xlabel = "$\lambda$ values", ylabel = "$\eta$ values", title = "Accuracy score logistic regression using SKLearn")





coef = logistic_reg(X_train, y_train, 0.001, 0.0001, n_epochs, 10)
y_pred = predict_logistic(X_test, coef)

cm_own = confusion_matrix(y_test, y_pred)

clf = SGDClassifier(loss="log", penalty="l2", learning_rate = "constant", eta0 = 0.001, alpha = 0.0001, max_iter=n_epochs).fit(X_train, y_train)
pred_sklearn = clf.predict(X_test)

cm_sklearn = confusion_matrix(y_test, pred_sklearn)

print("Prediction: ", y_pred)
print("Target: ", y_test)
