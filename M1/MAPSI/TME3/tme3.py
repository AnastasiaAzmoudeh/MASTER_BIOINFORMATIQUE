#AZMOUDEH
#ZEDIRA
import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl

def learnML_parameters(X,Y):
    #creation des matrices
    mu = np.zeros((10,256))
    sig = np.zeros((10,256))

    #on parcourt pour chaque classe
    for i in range(10) : 
        #tout les indices de X de la classe i
        indice = np.where(Y == i)
        
        #on calcule les mu et std
        mu[i] = np.mean(X[indice],axis =0)
        sig[i] = np.std(X[indice],axis =0)

    return mu,sig

def log_likelihood(img, mu, sig, defsig):
    resultat = 0
    
    for i in range(256) :
        #on remplace sig si il est egal a 0
        if sig[i] == 0 :
            sigma = defsig
        else : 
            sigma = sig[i]
            
        resultat += np.log(2* np.pi* sigma**2) + ((img[i]-mu[i])**2)/(sigma**2)
        
        
    return resultat * -0.5

def classify_image(img, mu, sig, defeps):
    vrai = np.zeros(10)
    
    #on regarde la vraisemblance pour tout les chiffres
    for i in range(10) :
        vrai[i] = log_likelihood(img, mu[i], sig[i],defeps)
    
    #on retourne le chiffre avec la vraisemblance la plus elevee
    return np.where(vrai == np.max(vrai))[0][0]

def classify_all_images(X, mu, sig, defeps):
    Y = np.array([])
    for i in range(len(X)) :
        Y = np.append(Y, classify_image(X[i], mu, sig, defeps))
        
        
    return Y

def matrice_confusion(Y, Y_hat):
    mat = np.zeros((len(np.unique(Y)), len(np.unique(Y_hat))))

    for i in range(len(Y)) : 
        mat[int(Y[i])][int(Y_hat[i])] += 1
        
    return mat

def classificationRate(Y_train,Y_train_hat):
    return np.where(Y_train == Y_train_hat, 1, 0).mean()

def classifTest(X_test,Y_test,mu,sig,e):
    Y_test_hat = classify_all_images(X_test, mu, sig, -1)
    Y_test_hat = Y_test_hat.astype(int)

    m2 = matrice_confusion(Y_test, Y_test_hat)

    print("Taux de bonne classification: {}".format(np.where(Y_test == Y_test_hat, 1, 0).mean()))

    plt.figure()
    plt.imshow(m2)

    
    faux = np.where(Y_test != Y_test_hat)
    plt.figure()
    plt.imshow(X_test[faux[0][0]].reshape(16,16),cmap="gray")
    return faux

def binarisation(X):
    return np.where(X>0, 1, 0)


def learnBernoulli ( X,Y ):
    matTheta = np.zeros((10,256))
    
    for i in range(10) :
        tmp = np.where(Y == i)
        matTheta[i] = np.mean(X[tmp],axis =0)
    
      
    return matTheta

def logpobsBernoulli(X, theta,epsilon):
    #on prend une valeur epsilon pour s'eloigner de la borne 0 et de la borne 1
    
    theta = np.maximum(np.minimum(1-epsilon,theta),epsilon)
    
    matLog = [(X * np.log(m) + (1-X)* np.log(1- m)).sum() for m in theta]
    
    return np.array(matLog)

def classifBernoulliTest(Xb_test,Y_test,theta):
    Y_test_hat = [np.argmax(logpobsBernoulli(Xb_test[i], theta,1e-5)) for i in range (len(Xb_test))]

    m = matrice_confusion(Y_test, Y_test_hat)

    print("Taux de bonne classification: {}".format(np.where(Y_test == Y_test_hat, 1, 0).mean()))

    plt.figure()
    plt.imshow(m)

def transfoProfil(X):
    x2 = []
    for x in X:
        ind = np.where(np.hstack((x.reshape(16, 16), np.ones((16,1))))>0.3)
        x2.append( [ind[1][np.where(ind[0] == i)][0] for i in range(16)])
    return np.array(x2)




def learnGeom(X, Y,seuil):
    geomTheta = np.zeros((10, 16))
    for i in range(10):
        ind = np.where(Y == i)
        # Calculez la moyenne de X pour la classe i
        moyenne = np.mean(X[ind], axis=0)
        
        # Calculez le paramètre de la loi géométrique
        theta = 1.0 / moyenne
        if theta.all()>seuil:
            geomTheta[i] = theta
    
    return geomTheta


    
def logpobsGeom(X, theta):
    geomLog = []
    for t in theta:
        log_likelihood = np.sum((X - 1) * np.log(1 - t) + np.log(t))
        geomLog.append(log_likelihood)
    
    result = np.array(geomLog)
    return result

def classifyGeom(X, theta):
    return np.argmax(logpobsGeom(X, theta))


