import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MaxAbsScaler
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import Lasso
from sklearn import linear_model
import random
import importlib
import functions
importlib.reload(functions)
from functions import mse, r2, create_X, ols, ridge, lasso, kfold, var_beta, predict, FrankeFunction, evaluate_method, bootstrap, plot_mse, ci
plt.rcParams['figure.figsize'] = (10.,10.)
np.random.seed(2405)

N = 500
x = np.random.uniform(0, 1, N)
y = np.random.uniform(0, 1, N)
# Make data.
#x = np.arange(0, 1, 0.001)
#y = np.arange(0, 1, 0.001)

#x1, y1 = np(x,y)
z = FrankeFunction(x, y)
#z = FrankeFunction(x, y)
complex = 13 #complexity of model
X = create_X(x,y,complex)

test_train_l = train_test_split(X,z,test_size=0.2)
#Exercise 1
print(f"OLS: {evaluate_method(ols, test_train_l, scale = False, d = 5)}")

noise = np.random.normal(0, 1, size=(z.shape))
z_noisy = FrankeFunction(x, y) + noise*0.2
test_train_l_noise = train_test_split(X,z_noisy,test_size=0.2)
print(f"OLS with noise: {evaluate_method(ols, test_train_l_noise, scale = False, d = 5)}")
variance_beta = var_beta(test_train_l_noise[0])
beta_l = ols(test_train_l_noise[0], test_train_l_noise[2])
confidence_interval = ci(beta_l, variance_beta, N)




#Exercise 2
n_bs = 100 #number of bootstrap cycles
mse_test = np.zeros((complex, n_bs)) #for storing bootstrap samples' MSE for varying complexity (rows:complexity, columns:bootstrap sample)
mse_train = np.zeros((complex, n_bs))
r2_test = np.zeros((complex, n_bs))
r2_train = np.zeros((complex, n_bs))

#Bootstrap and plotting MSE vs complexity

tts = train_test_split(X,z_noisy,test_size=0.2)
beta_l = np.zeros(X.shape[1])

for j in range(n_bs): #looping through bootstrap samples
    X_sample, z_sample = bootstrap(tts[0],tts[2])
    tts2 = [X_sample, tts[1], z_sample, tts[3]]
    for i in range(complex): #looping through complexity of model
        mse_train[i,j], r2_train[i,j], mse_test[i,j], r2_test[i,j] = evaluate_method(ols, tts2, scale = True, d = i+1)

mean_mse_train = np.mean(mse_train, axis = 1) #calculating mean of MSE of all bootstrap samples
mean_mse_test = np.mean(mse_test, axis = 1)
mean_r2_train = np.mean(r2_train, axis = 1)
mean_r2_test = np.mean(r2_test, axis = 1)

plot_mse(mean_mse_train, mean_mse_test, method_header = "bootstrap")


#Bootstrap and plot MSE vs # datapoints
n_points = np.arange(100,10001,100)

mse_test_n = np.zeros((len(n_points), n_bs)) #for storing bootstrap samples' MSE for varying sample size (rows:sample size, columns:bootstrap sample)
mse_train_n = np.zeros((len(n_points), n_bs))
r2_test_n = np.zeros((len(n_points), n_bs))
r2_train_n = np.zeros((len(n_points), n_bs))


for i in range(len(n_points)): #looping through different sample sizes
    X_data = X[:n_points[i]]
    z_data = z_noisy[:n_points[i]]
    X_sample, z_sample = bootstrap(X_data,z_data)
    tts = train_test_split(X_sample,z_sample,test_size=0.2)
    for j in range(n_bs): #looping through different bootstrap cycles
        mse_train_n[i,j], r2_train_n[i,j], mse_test_n[i,j], r2_test_n[i,j] = evaluate_method(ols, tts, scale = True, d = 4)


mean_mse_train_n = np.mean(mse_train_n, axis = 1) #calculating mean of MSE of all bootstrap samples
mean_mse_test_n = np.mean(mse_test_n, axis = 1)
mean_r2_train_n = np.mean(r2_train_n, axis = 1)
mean_r2_test_n = np.mean(r2_test_n, axis = 1)

plot_mse(mean_mse_train_n, mean_mse_test_n, method_header = "bootstrap", plot_complexity = False, complexities = n_points)



#Exercise 3, K-fold
k = np.arange(5,11)
mse_train_kfold = np.zeros((complex, len(k)))
mse_test_kfold = np.zeros((complex, len(k)))
r2_train_kfold = np.zeros((complex, len(k)))
r2_test_kfold = np.zeros((complex, len(k)))

for i in range(len(k)):
    mse_train_kfold[:,i], r2_train_kfold[:,i], mse_test_kfold[:,i], r2_test_kfold[:,i] = kfold(X, z_noisy, k[i], complex)

plot_mse(mse_train_kfold, mse_test_kfold, method_header = "kfold", complexities = k)

#Exercise 4, Ridge
compl = [3,4,5,6]
nlambda = 15
lambda_values = np.logspace(-4,0.5,nlambda) #[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 0.75, 1]
mse_test_ridge = np.zeros((len(compl), len(lambda_values)))
mse_train_ridge = np.zeros((len(compl), len(lambda_values)))
r2_test_ridge = np.zeros((len(compl), len(lambda_values)))
r2_train_ridge = np.zeros((len(compl), len(lambda_values)))
"""
for j in range(n_bs): #looping through bootstrap samples
    X_sample, z_sample = bootstrap(tts[0],tts[2])
    tts2 = [X_sample, tts[1], z_sample, tts[3]]
    for i in range(complex): #looping through complexity of model
"""
for i in range(len(compl)):
    for j in range(len(lambda_values)):
        mse_train_ridge[i,j], r2_train_ridge[i,j], mse_test_ridge[i,j], r2_test_ridge[i,j] = evaluate_method(ridge,
        tts, lmb = lambda_values[j], d=compl[i], scale = True)

#mean_mse_train_ridge = np.mean(mse_train_ridge, axis = 1)
#mean_mse_test_ridge = np.mean(mse_test_ridge, axis = 1)
#mean_r2_train_ridge = np.mean(r2_train_ridge, axis = 1)
#mean_r2_test_ridge = np.mean(r2_test_ridge, axis = 1)

plot_mse(mse_train_ridge, mse_test_ridge, method_header = "ridge", lambdas = lambda_values, plot_complexity = True, complexities = compl)






#Exercise 5, Lasso
nlambda = 15
lambda_values = np.logspace(-2,0.5,nlambda) #[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 0.75, 1]
mse_test_lasso = np.zeros((len(compl), len(lambda_values)))
mse_train_lasso = np.zeros((len(compl), len(lambda_values)))
r2_test_lasso = np.zeros((len(compl), len(lambda_values)))
r2_train_lasso = np.zeros((len(compl), len(lambda_values)))



"""
for i in range(len(compl)):
    for j in range(len(lambda_values)):
        mse_train_lasso[i,j], r2_train_lasso[i,j], mse_test_lasso[i,j], r2_test_lasso[i,j] = evaluate_method(lasso,
        tts, lmb = lambda_values[j], d=compl[i], scale = False)

print(mse_test_lasso)
"""


#plot_mse(mse_train_lasso, mse_test_lasso, method_header = 'lasso', plot_complexity = True, lambdas = lambda_values, complexities = compl)



# Load the terrain
"""
terrain1 = imread('SRTM_data_Norway_1.tif')
x, y = np.meshgrid(range(terrain1.shape[1]), range(terrain1.shape[0]))
z_terrain = terrain1.flatten().astype(np.float)
X = create_X(x.flatten(),y.flatten(), 5)
train_test_terrain = train_test_split(X, z_terrain, test_size = 0.2)
print(f"OLS terrain: {evaluate_method(ols, train_test_terrain, scale = True, d = 5)}")


print(x.shape)
print(y.shape)
print(terrain1)
print(terrain1.shape)
# Show the terrain
plt.figure()
plt.title('Terrain over Norway 1')
plt.imshow(terrain1, cmap='gray')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
"""