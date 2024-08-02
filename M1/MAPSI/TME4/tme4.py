#AZMOUDEH
#ZEDIRA

import numpy as np
import matplotlib.pyplot as plt
import pickle as pkl

#plt.rcParams['animation.writer'] = 'ffmpeg'#forcer matplotlib à utilser matplotlib

def normale_bidim(x, mu, Sig):
    N=len(Sig)
    prodscalaire=(x-mu).T.dot(np.linalg.inv(Sig)).dot(x-mu)
    
    a= ((2*np.pi)**(N/2))*((np.linalg.det(Sig))**(1/2))
    res= (1/a)*(np.exp((-1/2)*prodscalaire))
    
    return res

def estimation_nuage_haut_gauche():
    mu4  = np.array([4.25,80.0])
    sig4 = np.array([[2.25,0],[0,400.]])
    return mu4,sig4

def init(X):
    pi = np.array([0.5, 0.5]) # le plus raisonnable dans l'absolu et cohérent avec les observations
    

    moymu1p=np.mean(X[:,0]+1)
    moymu1m=np.mean(X[:,0]-1)
    moymu2m=np.mean(X[:,1]-1)
    moymu2p=np.mean(X[:,1]+1)
    mu=np.array([[moymu1p,moymu2p],[moymu1m,moymu2m]])
    
   
    
    Sig=np.array([np.cov(X.T),np.cov(X.T)])
    
                  
        
    return pi, mu, Sig

def Q_i(X, pi, mu, Sig):
    # votre code
    q=np.zeros((len(pi),len(X))) #tableau Q nb de colonne Xi des données, nb de lignes --> nombre de classes pi
    #il faut utiliser la fonction normale_bidim(X, mu, Sig)
    for k in range(X.shape[0]):
        denom=0
        
        for j in range(len(pi)) :
            denom +=(normale_bidim(X[k], mu[j], Sig[j]))*pi[j]

        for i in range(pi.shape[0]):
        
            p1=normale_bidim(X[k], mu[i], Sig[i])
            num=p1*pi[i]
           
            q[i][k]=num/denom
      
    return q

def update_param(X, q, pi, mu, Sig):
    pi_u=np.zeros(pi.shape)
    mu_u=np.zeros(mu.shape)
    Sig_u=np.zeros(Sig.shape)
    
    
    #les sommes de Q sont les memes donc on les garde dans des variables
    sum_yi = np.zeros(len(pi))
    for i in range(len(pi)):
        sum_yi[i] = np.sum(q[i,:])
    
    #calcul de mu
    prod=np.matmul(q,X)
    for i in range(len(pi)):
        mu_u[i,:]= prod[i,:]/sum_yi[i]

    #calcul de sig
    for i in range(len(pi)):
        Sig_u[i] = np.matmul(q[i]*np.transpose(X-mu_u[i]),(X-mu_u[i]))/sum_yi[i]
    
    #calcul de pi
    total_sum_yi = np.sum(sum_yi)
    for i in range(len(pi)):
        pi_u[i] = sum_yi[i] / total_sum_yi

    return pi_u,mu_u,Sig_u


import os


def EM(X,initFunc=None,nIterMax=None,saveParam=None):
    if(initFunc==None):
        initFunc=init
    if nIterMax==None:    
        nIterMax=100
    
    pi, mu, Sig = initFunc(X)
    
    for i in range(nIterMax):
        
        q = Q_i(X, pi, mu, Sig)
        pi_up, mu_up, Sig_up = update_param(X, q, pi, mu, Sig)
        
        
        #pour sauvegarder
        if saveParam != None:                                            # détection de la sauvergarde
            if not os.path.exists(saveParam[:saveParam.rfind('/')]):     # création du sous-répertoire
                 os.makedirs(saveParam[:saveParam.rfind('/')])
            pkl.dump({'pi':pi, 'mu':mu, 'Sig': Sig},\
                     open(saveParam+str(i)+".pkl",'wb'))                 # sérialisation
        
        
        #on compare le nouveau mu avec le precedent
        #si les deux mu sont assez proche, on arrete d'iterer (np.sum(abs((mu_up)-(mu)))<=1e-3)
       
        if np.abs(mu-mu_up).sum()<1e-3 :
            
            break
        nIterMax=i+1
        pi=pi_up
        mu=mu_up
        Sig=Sig_up
        
    #dans le cas ou les mu ne converge pas apres nIterMax
    #print("Apres ",nIterMax, " pas de convergence pour un critere à 1e-3")
    return nIterMax, pi, mu, Sig

def init_4(X): 
    
    #Affectation des valeurs pour mu
    mu_4 = np.array(([1,1], [-1,1], [1,-1], [-1,-1]))
    
    
    #Nombre de classes : mu_f.shape[0]
    nbcl = mu_4.shape[0]
    
    #Création de pi, mu et Sig
    pi_4 = np.zeros((nbcl))
    Sig_4 = np.zeros((nbcl,2,2))
    

    #Parcours sur le nombre de classes voulu
    for cl in range(nbcl):
        
        # Equiprobabilité de pi
        pi_4[cl] = 1/nbcl
        
        #mu_4[cl] = np.mean(X, axis=0)

        mean_x = np.mean(X, axis=0)
        mu_4 = np.array([mean_x + [1, 1], mean_x + [-1, 1], mean_x + [1, -1], mean_x + [-1, -1]])
        
        #Calcul de la matrice de variances
        Sig_4[cl] = np.cov(X.T)
    
    return pi_4, mu_4, Sig_4


def bad_init_4(X): #FAUX 
    #Affectation des valeurs pour mu
    mu_4 = np.array(([4,2], [3,4], [0,0], [-5,0]))
    
    
    #Nombre de classes : mu_f.shape[0]
    nbcl = mu_4.shape[0]
    
    #Création de pi, mu et Sig
    pi_4 = np.zeros((nbcl))
    Sig_4 = np.zeros((nbcl,2,2))
    

    #Parcours sur le nombre de classes voulu
    for cl in range(nbcl):
        
        # Equiprobabilité de pi
        pi_4[cl] = 1/nbcl

        mean_x = np.mean(X, axis=0)
        mu_4 = np.array([mean_x + [4, 2], mean_x + [3, 4], mean_x + [0, 0], mean_x + [-5, 0]])
        
        #Calcul de la matrice de variances
        Sig_4[cl] = np.cov(X.T)
    
    return pi_4, mu_4, Sig_4
def init_B(X):
    pi = np.zeros(10)+0.1
    theta = np.zeros((10,256))
    for i in range(10):
        theta[i] = np.sum(X[i*3:(i+1)*3],axis=0)/3
    return pi, theta

def logpobsBernoulli(X, theta): 
    seuil = 1e-5
    theta = np.maximum(np.minimum(1-seuil, theta),seuil)
    logp = (X*np.log(theta)+(1-X)*np.log(1-theta)).sum()
    return np.array(logp)

def Q_i_B(X, pi, theta):
    q = np.zeros((10, 6229))
    log_p_theta_x = np.zeros((10, 6229))
    theta = np.maximum(np.minimum(1-(1e-5), theta),(1e-5))
    for i in range(10):
        for j in range(6229):            
            log_p_x_theta = logpobsBernoulli(X[j], theta[i])
            val = np.exp(log_p_x_theta) * theta[i]
            s_star = np.max(val)
            log_neg = s_star + np.log(np.exp(val-s_star))
            for k in range(256):
                log_p_theta_x[i][j] = log_p_x_theta + np.log(theta[i][k]) - log_neg[k]
                q[i][j] = pi[i] * np.exp(log_p_theta_x[i][j])
    q_sum = np.sum(q, axis=0)
    for i in range(10):
        q[i] /= q_sum
    return q

def update_param_B(X, q, pi, theta):
    pi_u=np.zeros(pi.shape)
    theta_u=np.zeros(theta.shape)
    
    #les sommes de Q sont les memes donc on les garde dans des variables
    sum_yi = np.zeros(len(pi))
    for i in range(len(pi)):
        sum_yi[i] = np.sum(q[i,:])
    
    #calcul de theta
    prod=np.matmul(q,X)
    for i in range(len(pi)):
        theta_u[i,:]= prod[i,:]/sum_yi[i]

    
    #calcul de pi
    total_sum_yi = np.sum(sum_yi)
    for i in range(len(pi)):
        pi_u[i] = sum_yi[i] / total_sum_yi
    return pi_u, theta_u


def EM_B_bis(X):
    
    nIterMax=100 
    saveParam=None
    pi, theta = init_B(X)
    for i in range(nIterMax):
        q = Q_i_B(X, pi, theta)
        pi_u, theta_u = update_param_B(X, q, pi, theta)
        
           
    
       
        err = np.abs(theta-theta_u).max()   
        if(err < 1e-3):
            break
        pi = pi_u
        theta = theta_u
        
    return pi, theta

def EM_B(X,initFunc=None,nIterMax=None,saveParam=None):
    if(initFunc==None):
        initFunc=init_B
    if nIterMax==None:    
        nIterMax=100
    
    pi,theta = initFunc(X)
    
    for i in range(nIterMax):
        
        q = Q_i_B(X, pi, theta)
        pi_up, theta_up = update_param_B(X, q, pi,theta)
        
        
        
        
        #on compare le nouveau mu avec le precedent
        #si les deux mu sont assez proche, on arrete d'iterer
        err = np.abs(theta-theta_up).max()   
        if(err < 1e-3):
            break
        nIterMax=i+1
        pi=pi_up
        theta=theta_up
        
    #dans le cas ou les mu ne converge pas apres nIterMax
    #print("Apres ",nIterMax, " pas de convergence pour un critere à 1e-3")
    return nIterMax, pi, theta


def calcul_purete(X, Y, pi, theta):
    
    #initialisation 
    Y_hat = Q_i_B(X,pi,theta).argmax(0)
    
    
    purete = np.zeros(10)
    poids = np.zeros(10)
    
    
    for i in range(10):
        
       
        Y_hat_i = Y[Y_hat == i]
        
       
        val, count = np.unique(Y_hat_i, return_counts=True)
        
        
        purete[i] = np.max(count)/ np.sum(count)
        poids[i] = np.sum(count)

    return purete,poids