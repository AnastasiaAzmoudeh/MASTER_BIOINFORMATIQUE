#AZMOUDEH
#ZEDIRA

import numpy as np
import matplotlib.pyplot as plt

import pickle as pkl

def analyse_rapide(d):
    "array -> void "

    avg=np.mean(d) # calcul de la moyenne/average
    print(" moyenne = : ",avg)
    ecrtyp=np.std(d) # calcul de l'ecart type
    print("ecart type = ",ecrtyp)
    listequantile= []
    for i in range(0,10):
        quantile=np.quantile(d,i/10)
        #print('Quantile num ',i,'=',quantile)
        listequantile.append(quantile)
    print("liste quantiles = ",listequantile)
   

def discretisation_histogramme(d,n):
    "array , int-> void "
    # n nb intervalle
    inter = (max(d)-min(d))/n
    
    bornes = np.arange(min(d),max(d),inter) 

    effectifs = []
    for i in range(n):
        long = np.where((d>=bornes[i])&(d<bornes[i]+inter),1,0).sum()   #comptage associe de tous les indices de x qui satisfont la clause
        
        effectifs.append(long)

    print("effectifs : ", effectifs)
    
    print(" bornes :", bornes)
    plt.figure()
    plt.bar(bornes,effectifs,width=75,edgecolor='k')

def discretisation_prix_au_km(data,n):
    "array , int-> void "
    # histogramme des prix au km 
    prix = data[:, 10]
    d=data[:,-1]
    
    prixaukm = [prix[i]/d[i] for i in range(len(prix))]

    #n = 40 # nb intervalle

    inter = (max(prixaukm)-min(prixaukm))/n

    bornes = np.arange(min(prixaukm),max(prixaukm),inter) 

    # calcul des effectifs avec np.where

    effectifs = []
    for i in range(n):
       
        long = np.where((prixaukm>=bornes[i])&(prixaukm<bornes[i]+inter),1,0).sum() 
        
        effectifs.append(long)

    print("effectifs : ", effectifs)

    print(" bornes :", bornes) 

    plt.figure()
    plt.hist(prixaukm,bornes,width=0.045)
    plt.title('Histogramme des prix au km')
    plt.show()

def loi_jointe_distance_marque(data,n,dico_marques):
    "array , int dict(str:int)-> void "
    #n # nb intervalle
    d=data[:,-1] #pour recuperer les distances
    inter = (max(d)-min(d))/n #pour avoir l'intervalle
    
    bornes = np.arange(min(d),max(d),inter) #pour avoir les bornes



    distdiscr = np.zeros(d.shape) # on construit l'array distances discretisees

    
    #pour discretiser les distances une methode est de faire d-minimum et division entiere par l'intervalle
    distdiscr = np.where(True, (d - min(d))//inter, 0)
    print("distances discretisees :", distdiscr)
    

    p_dm = np.zeros((len(bornes)-1, len(dico_marques)))

    # remplissage de la matrice p_dm 
    for i in range(len(bornes)-1): #une boucle qui va de 0 a 29
        valeurs = np.where(distdiscr == i) #on recupere les valeurs ou distances discretisees sont egale a i
        cpt_marque = 0 #cpt marque pour cpt les marques
        for v in dico_marques.values():
            cpt = 0
            for f in range(len(valeurs[0])):
                if (np.where((data[valeurs[0][f],-3] == v),1,0)): #- 3 indice marques
                    cpt += 1
            p_dm[i][cpt_marque] = cpt
            cpt_marque += 1    
            


    p_dm /= p_dm.sum() # normalisation

    # affichage du resultat

    fig, ax = plt.subplots(1,1)
    plt.imshow(p_dm, interpolation='nearest')
    ax.set_xticks(np.arange(len(dico_marques)))
    ax.set_xticklabels(dico_marques.keys(),rotation=90,fontsize=8)
    plt.show()
    
    return p_dm


def loi_conditionnelle(joint_dm,dico_marques,data,n):
    "array ,  dict(str:int),array,int-> void "
    #a revoir faux
    d=data[:,-1] #pour recuperer les distances
    inter = (max(d)-min(d))/n #pour avoir l'intervalle
    
    bornes = np.arange(min(d),max(d),inter)
        
    p_m = np.zeros(len(dico_marques))

    for i in range(len(p_m)):
        p_m[i] = joint_dm[:,i].sum()

    

    # calcul de la conditionnelle
    p_dsm = np.zeros((len(bornes)-1, len(dico_marques)))

    # application du Théorème de Bayes : P(A|B) = P(A,B) / P(B)
    for j in range(len(p_m)):
            p_dsm[:,j] =joint_dm[:,j] / p_m[j]

            
    

    # affichage
    fig, ax = plt.subplots(1,1)
    plt.imshow(p_dsm, interpolation='nearest')
    ax.set_xticks(np.arange(len(dico_marques)))
    ax.set_xticklabels(dico_marques.keys(),rotation=90,fontsize=8)
    plt.show()

    return p_dsm

def check_conditionnelle(loi):
    "array --> boolean"
    
    print("LOI[:,1].sum() = ",loi[:,1].sum()) #si la somme de la marginal est égale à 1 alors conditionnelle verifiee
    if round(loi[:,1].sum())==1:
        return True
    else:
        return False

def trace_trajectoires(data):
    "array --> void"

    
    x_dep = data[:,6]
    y_dep = data[:,7]
    x_arr = data[:,8]
    y_arr = data[:,9]

    delta_x = x_arr-x_dep
    delta_y = y_arr-y_dep

    plt.figure()
    plt.quiver(x_dep, y_dep, delta_x, delta_y, angles='xy', scale_units='xy', scale=1, color='purple')
    plt.title('Tous les vecteurs de data')
    plt.show()

def calcule_matrice_distance(data,coord):
    "array, array --> array"
    dist = np.zeros((7,7))

    for i in range(len(dist)):
        for j in range(len(dist)):
            dist[i][j]=np.sqrt(((coord[j][0]-coord[i][0])**2)+((coord[j][1]-coord[i][1])**2))
                
    return dist

def calcule_coord_plus_proche(matrice_dist):
    "array -> dico"
    np.fill_diagonal(matrice_dist, 999)
    
    dic_villeproche={}
    for i in range(len(matrice_dist)):
        dic_villeproche[i]=np.argmin(matrice_dist[i])

    return dic_villeproche
def trace_ville_coord_plus_proche(data,ville_c):
    pass