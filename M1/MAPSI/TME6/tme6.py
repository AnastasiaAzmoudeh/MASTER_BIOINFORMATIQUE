import numpy as np
import matplotlib.pyplot as plt
import string
import utils

#AZMOUDEH
#ZEDIRA



def discretise(x, d):
    intervalle = 360 / d
    disc = []
    for i in range(len(x)) :
        intt = np.array(np.floor(x[i] / intervalle))
        disc.append(intt)
    
    return np.array(disc)

def groupByLabel(y):
    index = []
    for i in np.unique(y): # pour toutes les classes
        ind, = np.where(y == i)
        index.append(ind)
    
    dicoindex={}
    l="a"
    for i,e in enumerate(index):
        
        

        cle=chr(ord(l)+i)
        dicoindex[cle]=e
        
    return dicoindex

def learnMarkovModel(Xc, d):
    Xcd=discretise(Xc, d) 
    A = np.zeros((d, d))
    Pi = np.zeros(d)
    
    for i in range(len(Xcd)):
        
        
        Pi[int(Xcd[i][0])]+=1
    
        for j in range(len(Xcd[i])-1) :

            A[int(Xcd[i][j])][int(Xcd[i][j+1])]+=1
        
    A = A / np.maximum(A.sum(1).reshape(d, 1), 1) # normalisation
    Pi = Pi / Pi.sum()
    return Pi, A

def learn_all_MarkovModels(X,Y,d):
    
    #Xd = discretise(X, d)    # application de la discrétisation
    dicoindex = groupByLabel(Y)  # groupement des signaux par classe
    #ll=[]
    models = {}
    #for cl in range(len(np.unique(Y))): # parcours de toutes les classes et optimisation des modèles
    #for key,val in dicoindex.items():
       # models[key]= learnMarkovModel(Xd[val], d)
    l="a"
    for cl in range(len(np.unique(Y))):  # parcours de toutes les classes et optimisation des modèles
        
        cle=chr(ord(l)+cl)
        
        #if cle not in models:
        models[cle] = learnMarkovModel([X[i] for i in dicoindex[cle]], d)
           
    return models

def stationary_distribution_freq(Xc,d):
    mu1=np.zeros(d)
    for i in range(len(Xc)):
        for j in range(len(Xc[i])):
            mu1[int(Xc[i][j])]+=1
    mu1=mu1/mu1.sum()
    return mu1

#NE MARCHE PAS 
'''def stationary_distribution_sampling(models,N):
    result = []
    for i in range(len(models)) :
        ite = 0
        mu = models[i][0] #matrice Pi #initialisation
        
        while ite <N  :
            mu_u = np.matmul(mu,models[i][1]) #matrice de transition
            if (mu - mu_u).sum() < 10^-3 :
                break
            else :
                mu = mu_u
                ite +=1
        
        result.append(mu_u)
        
    return result'''

def stationary_distribution_sampling(models,N):
    pass

def stationary_distribution_fixed_point(models,epsilon):
    pass



# print(tme6.stationary_distribution_fixed_point_VP(models['a'][1])) REMPLACER PAR
#print(tme6.stationary_distribution_fixed_point_VP(models['a'])) DE CETTE MANIERE NOUS ARRIVONS A OBTENIR LE BON RESULTAT

def stationary_distribution_fixed_point_VP(models):
    result = []
   
    ite = 0
    mu = models[0] #matrice Pi #initialisation
        
    while ite <100  :
        mu_u = np.matmul(mu,models[1]) #matrice de transition
            #mu_u = np.matmul(mu,models) #matrice de transition
        if (mu - mu_u).sum() < 10^-3 :
            break
        else :
            mu = mu_u
            ite +=1
        
    result.append(mu_u)
        
    return result


#Inférence : classificartion de séquences (affectation dans les classes sur critère MV)

def logL_Sequence2(s,Pi,A):
    tmp = 0
    
    for j in range(len(s)-1) :
        tmp+= np.log(A[s[j]][s[j+1]])
    tmp += np.log(Pi[s[0]])
    
    return tmp

def logL_Sequence(s, Pi, A):
    logproba=Pi[int(s[0])]
    pos=int(s[0]) #position precedente
    for i in s[1:]:
        logproba=logproba*A[pos][int(i)]
        pos=int(i)
    if logproba!=0:
        logproba=np.log(logproba)
    else:
        logproba=-np.inf
    return logproba


#FONCTION MODIFIEE AJOUT DE Y DANS LA FONCTION. NOUS N'AVONS PAS REUSSI SANS AJOUTER Y 

def compute_all_ll(Xd,models,Y): #sans Y je ne sais pas honnetement 
    l="a"
    ll = np.array([[logL_Sequence(Xd[i], models[chr(ord(l)+cl)][0], models[chr(ord(l)+cl)][1]) for i in range(len(Xd))]
                  for cl in range(len(np.unique(Y)))])
    return ll

def compute_all_ll_bis(Xd,models): #sans Y je ne sais pas honnetement 
    
    ll = np.array([logL_Sequence(Xd[i], models[key][0], models[key][1]) for i in range(len(Xd))]
                  for key in models.keys())
    return ll

def accuracy(ll,Y):
    # calcul d'une version numérique des Y :
    Ynum = np.zeros(Y.shape)
    for num, char in enumerate(np.unique(Y)):
        Ynum[Y == char] = num
        
    # Calcul de la classe la plus probable :
    pred = ll.argmax(0) # max colonne par colonne
    

    # Calcul d'un pourcentage de bonne classification :
    return np.where(pred != Ynum, 0.,1.).mean()