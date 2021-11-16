import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
import random
import importlib
import functions
import NeuralNetworkClas
importlib.reload(functions); importlib.reload(NeuralNetworkClas)
from functions import *
from NeuralNetworkClas import *


data = load_breast_cancer()
x = data['data']
y = data['target']

#Select features relevant to classification (texture,perimeter,compactness and symmetery)
#and add to input matrix

temp1=np.reshape(x[:,1],(len(x[:,1]),1))
temp2=np.reshape(x[:,2],(len(x[:,2]),1))
X=np.hstack((temp1,temp2))
temp=np.reshape(x[:,5],(len(x[:,5]),1))
X=np.hstack((X,temp))
temp=np.reshape(x[:,8],(len(x[:,8]),1))
X=np.hstack((X,temp))

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2) #Split the data into training and test sets
y_trainhot = to_categorical_numpy(y_train)

eta = np.logspace(-4,-3,2)
n_neurons = np.logspace(0,2,3)
n_neurons = np.array([10,25,50,75,100,125])
lmb = 0.001
n_hl = 2
actfunc = {
"sigmoid": sigmoid,
"softmax": softmax,
"relu": relu,
"leaky_relu": leaky_relu
}
af = "sigmoid"

train_accuracy = np.zeros((len(eta),len(n_neurons)))
test_accuracy = np.zeros_like(train_accuracy)
for i,eta_ in enumerate(eta):
    for j,n_  in enumerate(n_neurons):
        NN = NeuralNetwork(X_train, y_trainhot, epochs = 100, batch_size = 25,
            n_categories = 2, eta = eta_, lmbd = lmb, n_hidden_neurons = [n_]*n_hl, activation_function = actfunc[af])
        NN.train()
        y_tilde = NN.predict(X_train)
        y_predict = NN.predict(X_test)

        train_score = accuracy_score_numpy(y_tilde, y_train)
        test_score = accuracy_score_numpy(y_predict, y_test)
        train_accuracy[i,j] = train_score
        test_accuracy[i,j] = test_score

        print(f"Eta: {eta_} | # of neurons: {n_}")
        print(f"Training accuracy: {accuracy_score_numpy(y_tilde, y_train)}")
        print(f"Test accuracy: {accuracy_score_numpy(y_predict, y_test)}")
        print("------------------------")



make_heatmap(train_accuracy, n_neurons, eta, fn = f"train_{af}_{n_hl}c.pdf",
            xlabel = "Number of neurons per layer", ylabel = "Learning rate $\eta$", title = "Accuracy score training set")
make_heatmap(test_accuracy, n_neurons, eta, fn = f"test_{af}_{n_hl}c.pdf",
            xlabel = "Number of neurons per layer", ylabel = "Learning rate $\eta$", title = "Accuracy score test set")




#Sklearn implementation

eta_vals = np.logspace(-5, 1, 7)
lmbd_vals = np.logspace(-5, 1, 7)

epochs = 1000

n_hidden_neurons = 50

from sklearn.neural_network import MLPClassifier
# store models for later use
DNN_scikit = np.zeros((len(eta_vals), len(lmbd_vals)), dtype=object)

for i, eta in enumerate(eta_vals):
    for j, lmbd in enumerate(lmbd_vals):
        dnn = MLPClassifier(solver='sgd', hidden_layer_sizes=(n_hidden_neurons), activation='logistic',
                            alpha=lmbd, learning_rate_init=eta, max_iter=epochs)
        dnn.fit(X_train, y_train)

        DNN_scikit[i][j] = dnn


sns.set()

train_accuracy_sklearn = np.zeros((len(eta_vals), len(lmbd_vals)))
test_accuracy_sklearn = np.zeros((len(eta_vals), len(lmbd_vals)))

for i in range(len(eta_vals)):
    for j in range(len(lmbd_vals)):
        dnn = DNN_scikit[i][j]

        train_pred = dnn.predict(X_train)
        test_pred = dnn.predict(X_test)


        train_accuracy_sklearn[i][j] = accuracy_score_numpy(y_train, train_pred)
        test_accuracy_sklearn[i][j] = accuracy_score_numpy(y_test, test_pred)


make_heatmap(test_accuracy_sklearn, lmbd_vals, eta_vals, fn = f"sklearn_class.pdf",
            xlabel = "lambda values", ylabel = "$\eta$ values", title = "Accuracy score sklearn")