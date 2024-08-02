import numpy as np
import matplotlib.pyplot as plt

#AZMOUDEH 
#ZEDIRA

np.random.seed(0) # pour avoir les même résultats aléatoires à chaque run


def gen_data_lin(a, b, sig, N=500, Ntest=1000):
    X_train = np.sort(np.random.rand(N)) # sort optionnel, mais ça aide pour les plots
    X_test  = np.sort(np.random.rand(Ntest))
    sigma1 = np.random.normal(0,sig,size=(N))
    sigma2 = np.random.normal(0,sig,size=(Ntest))
    Y_train = a * X_train + b + sigma1
    Y_test  = a * X_test + b + sigma2
    
    return X_train, Y_train, X_test, Y_test

def modele_lin_analytique(X_train, Y_train):
    cov_xy = np.cov(X_train, Y_train)[0][1]
    cov_xy_sur_var = cov_xy / (X_train.std()**2)
    ahat = cov_xy_sur_var
    bhat = Y_train.mean() - cov_xy_sur_var * X_train.mean()
    
    return ahat, bhat

def calcul_prediction_lin(X,ahat,bhat):
    return ahat*X+bhat

def erreur_mc(y, yhat):
    return ((y-yhat)**2).mean()

def dessine_reg_lin(X_train, y_train, X_test, y_test,a,b):
    ahat, bhat = modele_lin_analytique(X_train, y_train)
    yhat_test  = calcul_prediction_lin(X_test,ahat,bhat)

    plt.figure()
    plt.plot(X_test, y_test, 'r.',alpha=0.2,label="test")
    
    plt.plot(X_train, y_train, 'b')
    plt.plot(X_test, yhat_test, 'g', lw=3)

def make_mat_lin_biais(X): # fonctionne pour un vecteur unidimensionel X
    N = len(X)
    return np.hstack((X.reshape(N,1),np.ones((N,1))))

def reglin_matriciel(Xe,y_train):
    A = Xe.T @ Xe #@ multiplication matrice
    B = Xe.T @ y_train
    w = np.asarray(np.linalg.solve(A,B))
    return w

def calcul_prediction_matriciel(Xe,w):
    return w @ Xe.T

def gen_data_poly2(a, b, c, sig, N=500, Ntest=1000):
    '''
    Tire N points X aléatoirement entre 0 et 1 et génère y = ax^2 + bx + c + eps
    eps ~ N(0, sig^2)
    '''
    X_train = np.sort(np.random.rand(N))
    X_test  = np.sort(np.random.rand(Ntest))
    y_train = a*X_train**2+b*X_train+c+np.random.randn(N)*sig
    y_test  = a*X_test**2 +b*X_test +c+np.random.randn(Ntest)*sig
    return X_train, y_train, X_test, y_test

def make_mat_poly_biais(X): # fonctionne pour un vecteur unidimensionel X
    N = len(X)
    val=np.hstack((X.reshape(N,1)**2,(X.reshape(N,1)))) 
    
    return np.hstack((val,np.ones((N,1))))

def reglin_matriciel(Xe,yp_train):
    A = Xe.T @ Xe
    B = Xe.T @ yp_train
    w = np.linalg.solve(A,B)
    return w

def dessine_poly_matriciel(Xp_train,yp_train,Xp_test,yp_test,w):
    Xe_test   = make_mat_poly_biais(Xp_test)
    yhat_test  = calcul_prediction_matriciel(Xe_test,w)
    plt.figure()
    
   
    plt.plot(Xp_test, yp_test, 'r.',alpha=0.2,label="test")
    plt.plot(Xp_train, yp_train, 'b-')
    plt.plot(Xp_test, yhat_test, 'g', lw=3)
    

def descente_grad_mc(X, y, eps, nIterations):
    w = np.zeros(X.shape[1]) # init à 0
    allw = [w]
    for i in range(nIterations):
        
        w = w - eps * 2 * X.T @ (X @ w - y) #cours
        allw.append(w) # stockage de toutes les valeurs intermédiaires pour analyse
    allw = np.array(allw)
    return w, allw # la dernière valeur (meilleure) + tout l'historique pour le plot
    

def application_reelle(X_train,y_train,X_test,y_test):
    #Calcul de w et w_t
    w = np.linalg.solve(X_train.T @ X_train, X_train.T @ y_train)
    w_t = np.linalg.solve(X_test.T @ X_test, X_test.T @ y_test)

    #Calcul de yhat et yhat_t
    yhat   = w[0]
    yhat_t = w_t[0]
    for i in range(1,X_train.shape[1]):
        yhat += X_train[:,i]*w[i]
        yhat_t += X_test[:,i]*w_t[i]

    print("w = ",w)
    print('Erreur moyenne au sens des moindres carrés (train):', erreur_mc(yhat, y_train))
    print('Erreur moyenne au sens des moindres carrés (test):', erreur_mc(yhat_t, y_test))

    return w,yhat,yhat_t

def normalisation(X_train, X_test):
    '''
    Fonction de normalisation des données pour rendre les colonnes comparables
    Chaque variable est assimilée à une loi normale qu'il faut centrer + réduire.
    on calcule les moyennes et écarts-types sur les données d'apprentissage seulement
    '''
    
    Xn_train = np.zeros(X_train.shape)
    Xn_test = np.zeros(X_test.shape)
    

    for i in range(X_train.shape[1]):
        Xn_train[:,i] = ( X_train[:,i] - np.mean(X_train[:,i]) ) / np.std(X_train[:,i])
        Xn_test[:,i] = ( X_test[:,i] - np.mean(X_train[:,i]) ) / np.std(X_train[:,i])

   
    

    #  biais
    Xn_train = np.hstack((Xn_train, np.ones((Xn_train.shape[0], 1))))
    Xn_test   = np.hstack((Xn_test, np.ones((X_test.shape[0], 1))))
    
    return Xn_train, Xn_test



