import numpy as np
from sklearn.model_selection import train_test_split
import random
import importlib
import functions
importlib.reload(functions)
from functions import *
"""
Exercise 3:
Running OLS on the Franke Function as a function of the complexity of the model and using k-fold as a resampling technique
-->Plotting mean MSE as a function of complexity
"""
np.random.seed(2405)

#Same as ex1 and ex2
N = 500
x = np.random.uniform(0, 1, N)
y = np.random.uniform(0, 1, N)

z = FrankeFunction(x, y)
complex = 13 #complexity of model
X = create_X(x,y,complex)
noise = np.random.normal(0, 1, size=(z.shape))
z_noisy = FrankeFunction(x, y) + noise*0.2

tts = train_test_split(X,z_noisy,test_size=0.2) #Train test split

k = np.arange(5,11)
mse_train_kfold = np.zeros((complex, len(k))) #Arrays for storing the evaluation values
mse_test_kfold = np.zeros((complex, len(k)))
r2_train_kfold = np.zeros((complex, len(k)))
r2_test_kfold = np.zeros((complex, len(k)))

for i in range(len(k)): #Loops through the different number of k folds
    mse_train_kfold[:,i], r2_train_kfold[:,i], mse_test_kfold[:,i], r2_test_kfold[:,i] = kfold(X, z_noisy, k[i], complex)

plot_mse(mse_train_kfold, mse_test_kfold, method_header = "Kfold", complexities = k)
