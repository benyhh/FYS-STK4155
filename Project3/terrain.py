import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import importlib
import functions
import NNReg
importlib.reload(functions); importlib.reload(NNReg)
from NNReg import NeuralNetwork
from functions import *
from sklearn.exceptions import ConvergenceWarning, DataConversionWarning

warnings.filterwarnings(action='ignore', category=DataConversionWarning)
warnings.filterwarnings(action='ignore', category=ConvergenceWarning)
data = imread('SRTM_data_Norway_1.tif') #All data
terrain = data[:50,-50:] #Subset
Y = terrain.ravel() #1d array of subset
np.random.seed(42)
dim = terrain.shape
x1,x2 = np.meshgrid(range(dim[0]), range(dim[1]))
X1 = x1.ravel().astype(np.float)
X2 = x2.ravel().astype(np.float)

#Scale variables
#X1_scaled, X2_scaled = scale_data(X1,X2)

#Set up design matrix
#X1, X2 = scale_data(X1, X2)

X = create_X(X1, X2, 50)



X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.2)

X_train, X_test = scale_data(X_train, X_test)
Y_train, Y_test = scale_data(Y_train, Y_test)


def BVT_OLS(X_train, X_test, y_train, y_test, nb = 100, plot = False):
    complexity = X_train.shape[1]
    degree = int((-3+np.sqrt(9-8*(1-complexity)))/2)
    Loss = np.zeros(degree)
    Variance = np.zeros(degree)
    Bias = np.zeros(degree)
    
    for d in tqdm(range(1, degree + 1)):

        c = int((d+1)*(d+2)/2)
        regr = LinearRegression()
        avg_expected_loss, avg_bias, avg_var = bias_variance_decomp(
            regr, X_train[:,:c], y_train, X_test[:,:c], y_test, loss='mse', num_rounds = nb)

        Loss[d-1] = avg_expected_loss
        Variance[d-1] = avg_var
        Bias[d-1] = avg_bias
    
    if plot:
        plt.plot(range(1,degree+1), Bias, 'o-', label = "Bias$^2$")
        plt.plot(range(1,degree+1), Variance, 'o-', label = "Variance")
        plt.plot(range(1,degree+1), Loss, 'o-', label = "Loss")
        plt.xlabel("Polynomial Degree")
        plt.ylabel("Error")
        plt.title("OLS Bias-Variance Trade Off")
        plt.ylim(0,0.2)
        #plt.xlim(0,40)
        plt.legend()
        plt.savefig('bv_tradeoff_ols.pdf', dpi = 400, bbox_inches = 'tight')
        plt.show()

        plt.plot(range(1,degree+1), Bias, 'o-', label = "Bias$^2$")
        plt.plot(range(1,degree+1), Variance, 'o-', label = "Variance")
        plt.plot(range(1,degree+1), Loss, 'o-', label = "Loss")
        plt.xlabel("Polynomial Degree")
        plt.ylabel("Error")
        plt.title("OLS Bias-Variance Trade Off")
        plt.ylim(0,0.05)
        #plt.xlim(0,40)
        plt.legend()
        plt.savefig('bv_tradeoff_ols_close.pdf', dpi = 400, bbox_inches = 'tight')
        plt.show()

def BVT_Ridge(X_train, X_test, y_train, y_test, nb = 100, plot = False):
    complexity = X_train.shape[1]
    degree = int((-3+np.sqrt(9-8*(1-complexity)))/2)
    Loss = np.zeros(degree)
    Variance = np.zeros(degree)
    Bias = np.zeros(degree)
    
    for d in tqdm(range(1, degree + 1)):

        c = int((d+1)*(d+2)/2)
        regr = Ridge(alpha = 0.0005)
        avg_expected_loss, avg_bias, avg_var = bias_variance_decomp(
            regr, X_train[:,1:c], y_train, X_test[:,1:c], y_test, loss='mse', num_rounds = nb)

        Loss[d-1] = avg_expected_loss
        Variance[d-1] = avg_var
        Bias[d-1] = avg_bias
    
    if plot:
        plt.plot(range(1,degree+1), Bias, 'o-', label = "Bias$^2$")
        plt.plot(range(1,degree+1), Variance, 'o-', label = "Variance")
        plt.plot(range(1,degree+1), Loss, 'o-', label = "Loss")
        plt.xlabel("Polynomial Degree")
        plt.ylabel("Error")
        plt.title("Ridge Bias-Variance Trade Off")
        plt.ylim(0,0.02)
        #plt.xlim(0,40)
        plt.legend()
        plt.savefig('bv_tradeoff_ridge.pdf', dpi = 400, bbox_inches = 'tight')
        plt.show()
        
        plt.plot(range(1,degree+1), Bias, 'o-', label = "Bias$^2$")
        plt.plot(range(1,degree+1), Variance, 'o-', label = "Variance")
        plt.plot(range(1,degree+1), Loss, 'o-', label = "Loss")
        plt.xlabel("Polynomial Degree")
        plt.ylabel("Error")
        plt.title("Ridge Bias-Variance Trade Off")
        plt.ylim(0,0.01)
        #plt.xlim(0,40)
        plt.legend()
        plt.savefig('bv_tradeoff_ridge_close.pdf', dpi = 400, bbox_inches = 'tight')
        plt.show() 

def BVT_Lasso(X_train, X_test, y_train, y_test, nb = 100, plot = False):
    complexity = X_train.shape[1]
    degree = int((-3+np.sqrt(9-8*(1-complexity)))/2)
    Loss = np.zeros(degree)
    Variance = np.zeros(degree)
    Bias = np.zeros(degree)
    
    for d in tqdm(range(1, degree + 1)):

        c = int((d+1)*(d+2)/2)
        regr = Lasso(alpha = 0.000005, max_iter=1000, tol = 1e-3, fit_intercept=False)
        avg_expected_loss, avg_bias, avg_var = bias_variance_decomp(
            regr, X_train[:,1:c], y_train, X_test[:,1:c], y_test, loss='mse', num_rounds = nb)

        Loss[d-1] = avg_expected_loss
        Variance[d-1] = avg_var
        Bias[d-1] = avg_bias
    
    if plot:
        plt.plot(range(1,degree+1), Bias, 'o-', label = "Bias$^2$")
        plt.plot(range(1,degree+1), Variance, 'o-', label = "Variance")
        plt.plot(range(1,degree+1), Loss, 'o-', label = "Loss")
        plt.xlabel("Polynomial Degree")
        plt.ylabel("Error")
        plt.title("Lasso Bias-Variance Trade Off")
        #plt.ylim(0,0.4)
        #plt.xlim(0,40)
        plt.legend()
        plt.savefig('bv_tradeoff_lasso.pdf', dpi = 400, bbox_inches = 'tight')
        plt.show() 

        plt.plot(range(1,degree+1), Bias, 'o-', label = "Bias$^2$")
        plt.plot(range(1,degree+1), Variance, 'o-', label = "Variance")
        plt.plot(range(1,degree+1), Loss, 'o-', label = "Loss")
        plt.xlabel("Polynomial Degree")
        plt.ylabel("Error")
        plt.title("Lasso Bias-Variance Trade Off")
        plt.ylim(0,0.02)
        #plt.xlim(0,40)
        plt.legend()
        plt.savefig('bv_tradeoff_lasso_close.pdf', dpi = 400, bbox_inches = 'tight')
        plt.show() 

def BVT_DT(X_train, X_test, y_train, y_test, nb = 100, plot = False):
    complexity = 15
    Loss = np.zeros(complexity)
    Variance = np.zeros(complexity)
    Bias = np.zeros(complexity)
    leaf = np.logspace(1,complexity,complexity,base=2).astype(int)
    print(leaf)
    for c in tqdm(range(complexity)):
        regr = DecisionTreeRegressor(max_leaf_nodes=leaf[c])
        avg_expected_loss, avg_bias, avg_var = bias_variance_decomp(
            regr, X_train, y_train, X_test, y_test, loss='mse', num_rounds = nb)

        Loss[c] = avg_expected_loss
        Variance[c] = avg_var
        Bias[c] = avg_bias
    
    if plot:
        plt.plot(np.log2(leaf), Bias, 'o-', label = "Bias$^2$")
        plt.plot(np.log2(leaf), Variance, 'o-', label = "Variance")
        plt.plot(np.log2(leaf), Loss, 'o-', label = "Loss")
        plt.xlabel("log2(Leaves)")
        plt.ylabel("Error")
        plt.title("Decision Tree Bias-Variance Trade Off")
        plt.ylim(0,0.05)
        #plt.xlim(0,40)
        plt.legend()
        plt.savefig('bv_tradeoff_dt.pdf', dpi = 400, bbox_inches = 'tight')
        plt.show() 

def BVT_NN(X_train, X_test, y_train, y_test, nb = 100, plot = False):
    complexity = 9
    n = 20
    Loss = np.zeros(n)
    Variance = np.zeros(n)
    Bias = np.zeros(n)
    nodes = np.logspace(0,complexity-1, n, base = 2).astype(int)
    for c in tqdm(range(n)):

        regr = MLPRegressor(learning_rate_init=0.1,hidden_layer_sizes=(nodes[c],nodes[c]) , max_iter=10000)
        avg_expected_loss, avg_bias, avg_var = bias_variance_decomp(
            regr, X_train, y_train, X_test, y_test, loss='mse', num_rounds = nb)

        Loss[c] = avg_expected_loss
        Variance[c] = avg_var
        Bias[c] = avg_bias
    
    if plot:
        plt.plot(np.log2(nodes), Bias, 'o-', label = "Bias$^2$")
        plt.plot(np.log2(nodes), Variance, 'o-', label = "Variance")
        plt.plot(np.log2(nodes), Loss, 'o-', label = "Loss")
        plt.xlabel("log2(Nodes)")
        plt.ylabel("Error")
        plt.title("Neural Network Bias-Variance Trade Off")
        plt.ylim(0,0.2)
        #plt.xlim(0,40)
        plt.legend()
        plt.savefig('bv_tradeoff_nn.pdf', dpi = 400, bbox_inches = 'tight')
        plt.show()
        
        plt.plot(np.log2(nodes), Bias, 'o-', label = "Bias$^2$")
        plt.plot(np.log2(nodes), Variance, 'o-', label = "Variance")
        plt.plot(np.log2(nodes), Loss, 'o-', label = "Loss")
        plt.xlabel("log2(Nodes)")
        plt.ylabel("Error")
        plt.title("Neural Network Bias-Variance Trade Off")
        plt.ylim(0,0.025)
        #plt.xlim(0,40)
        plt.legend()
        plt.savefig('bv_tradeoff_nn_close.pdf', dpi = 400, bbox_inches = 'tight')
        plt.show() 


def BVT_SVM(X_train, X_test, y_train, y_test, nb = 100, plot = False):
    complexity = X_train.shape[1]
    degree = int((-3+np.sqrt(9-8*(1-complexity)))/2)
    degree = 10
    Loss = np.zeros(degree)
    Variance = np.zeros(degree)
    Bias = np.zeros(degree)
    gamma = np.logspace(-3,3,degree)

    for d in tqdm(range(1, degree + 1)):
        regr = SVR(gamma = gamma[d-1])
        avg_expected_loss, avg_bias, avg_var = bias_variance_decomp(
            regr, X_train, y_train, X_test, y_test, loss='mse', num_rounds = nb)
        #c = int((d+1)*(d+2)/2)
        #regr = SVR(C = 5)
        #avg_expected_loss, avg_bias, avg_var = bias_variance_decomp(
        #    regr, X_train[:,1:c], y_train, X_test[:,1:c], y_test, loss='mse', num_rounds = nb)

        Loss[d-1] = avg_expected_loss
        Variance[d-1] = avg_var
        Bias[d-1] = avg_bias
    
    if plot:
        plt.plot(np.log(gamma), Bias, label = "Bias$^2$")
        plt.plot(np.log(gamma), Variance, label = "Variance")
        plt.plot(np.log(gamma), Loss, label = "Loss")
        plt.xlabel("log($\gamma$)")
        plt.ylabel("Error")
        plt.title("Support Vector Machine Bias-Variance Trade Off")
        #plt.ylim(0,0.2)
        #plt.xlim(0,40)
        plt.legend()
        plt.show() 





if __name__ == '__main__':
    #BVT_OLS(X_train[:,:int(21*22/2)], X_test[:,:int(21*22/2)], Y_train, Y_test, nb=300, plot=True)
    #BVT_Ridge(X_train, X_test, Y_train, Y_test, nb=300, plot=True)   
    #BVT_NN(X_train[:,1:3], X_test[:,1:3], Y_train, Y_test, nb=100, plot=True)
    BVT_Lasso(X_train[:,:int(41*42/2)], X_test[:,:int(41*42/2)], Y_train, Y_test, nb=100, plot=True)
    #BVT_SVM(X_train[:,1:3], X_test[:,1:3], Y_train, Y_test, nb=5, plot=True)
    #BVT_DT(X_train[:,1:3], X_test[:,1:3], Y_train, Y_test, nb=10, plot=True)
    

#fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
#ax.plot_surface(x1,x2,terrain)
#ax.view_init(20,-20)
#plt.show()



