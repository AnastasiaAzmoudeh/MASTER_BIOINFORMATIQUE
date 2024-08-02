import numpy as np
import pickle as pkl
import matplotlib.pyplot as plt
import math

#AZMOUDEH
#ZEDIRA


    
def learnHMM(allX, allS, N, K):
    """ apprend un modèle à partir 
    d'un ensemble de couples (seq. d'observations, seq. d'états) 
    retourne les matrices A  B """
    
    #Création de la matrice de transition A et de la matrice de probabilité des émissions B.
    A = np.zeros((N, N)) 
    B = np.zeros((N, K)) 
    
    #Parcours sur le nombre d'états
    for i in range (len(allS)-1):
        
        #Calcul de la matrice de transition
        A[int(allS[i])][int(allS[i+1])]+=1
        
        #Calcul de la matrice de probabilité des émissions
        B[int(allS[i])][int(allX[i])]+=1
    
    #Calcul pour la dernière case
    B[int(allS[i+1])][int(allX[i+1])]+=1
    
    #Normalisation des lignes sur les deux matrices
    A = A/np.maximum(A.sum(1).reshape(N,1),1)
    B = B/np.maximum(B.sum(1).reshape(N,1),1)


    return A,B


def viterbi(allx,Pi,A,B):
    """
    Parameters
    ----------
    allx : array (T,)
        Sequence d'observations.
    Pi: array, (K,)
        Distribution de probabilite initiale
    A : array (K, K)
        Matrice de transition
    B : array (K, M)
        Matrice d'emission matrix

    """
    ## Initialisation
    psi = np.zeros((len(A), len(allx))) # A = N
    psi[:,0]= -1
    delta = np.zeros((len(A), len(allx)))  # initialisation en dimension mais pas en contenu !
    
    
    ## Recursion
    #on parcourt la sequence avec les colonnes de delta avec t
    for t in range(1,len(allx)) :
        #on parcourt les lignes de delta avec j
        for j in range(len(A)) :
            
            #boucle pour calculer max𝑖𝛿𝑡−1(𝑖)+log𝑎𝑖𝑗
            liste = np.zeros(len(A))
            for i in range(len(A)) :
                if A[i,j] != 0 :
                    liste[i]= delta[i,t-1]  + np.log(A[i,j])
                else :
                    liste[i]= delta[i,t-1] + np.log(1e-10)
            if B[j,int(allx[t])] != 0 :
                delta[j,t] = np.max(liste) + np.log(B[j,int(allx[t])])
            else :
                delta[j,t] = np.max(liste) + np.log(1e-10)
            psi[j,t] = np.argmax(liste)
            
    ## Terminaison
    S = np.zeros(len(allx))
    S[len(allx)-1] = np.argmax(delta[:,(len(allx)-1)])

    ## chemin    
    for i in range(len(allx)-2,-1,-1):
        S[i] =psi[int(S[i+1]),i]
    
    
    return  S

def get_and_show_coding(etat_predits,annotation_test):
    codants_predits=[]
    codants_test=[]

    etat_predits[etat_predits!=0]=1 
  

    annotation_test[annotation_test!=0]=1

    for e in etat_predits:
        codants_predits.append(e)

    for t in annotation_test:
        codants_test.append(t)

   

    fig, ax = plt.subplots(figsize=(15,2))
    ax.plot(annotation_test[100000:200000], label="annotation", lw=3, color="black", alpha=.4)
    ax.plot(etat_predits[100000:200000], label="prediction", ls="--")
    plt.legend(loc="best")
    plt.show()
    return codants_predits,codants_test
    

def create_confusion_matrix(true_sequence, predicted_sequence):
    true_seq = np.copy(true_sequence)
    predicted_seq = np.copy(predicted_sequence)
    true_seq[true_seq!=0]=1 
    predicted_seq[predicted_seq!=0]=1
    
    resultat = np.zeros((2,2))
    for i,j in zip(true_seq,predicted_seq):
        if i == 0 :
            true = 1 
        else :
            true = 0
        if j == 0 :
            predicted = 1 
        else :
            predicted = 0
        resultat[predicted,true]+=1
        
    return resultat


def get_annotation2(annotation_train):

    #on trouve tout les un qui ont un zero avant 

    indices_1_apres_0 = []
    precedent_est_zero = False

    for i, element in enumerate(annotation_train):
        if element == 1 and precedent_est_zero:
            indices_1_apres_0.append(i)
        precedent_est_zero = (element == 0)

    #on creer un array annotation_train2 de la même taille 
    annotation_train2=np.zeros((annotation_train.shape))



    for elt in indices_1_apres_0:    
        #on commence par le debut 
        i=elt
        while annotation_train[i]==0:
            annotation_train2[i]=0
            i+=1
            
        ind=i+3  

        #codon start

        annotation_train2[i]=1
        annotation_train2[i+1]=2
        annotation_train2[i+2]=3
        
        #codon intergenique 

        while annotation_train[ind]!=0:
            
            annotation_train2[ind]=4
            annotation_train2[ind+1]=5
            annotation_train2[ind+2]=6
            ind+=3
            
        #codon stop

        indback=ind
        annotation_train2[indback-1]=9
        annotation_train2[indback-2]=8
        annotation_train2[indback-3]=7
    
    return annotation_train2

