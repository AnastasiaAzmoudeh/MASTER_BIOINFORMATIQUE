import random
import numpy as np
import matplotlib.pyplot as plt
import math

# Zedira
# Azmoudeh


# I.1
def bernoulli(p):
    """bernoulli: float ->int"""
    if 0 <= p <= 1:
        r = random.random()
        return int(r < p)


# I.2
def binomiale(n, p):
    """binomiale: int , float -> int"""
    s = 0
    for i in range(n):
        s = s + bernoulli(p)
    return s


# I.3
def galton(l, n, p):
    """galton: int,int,float -> int np.array"""
    res = []
    for i in range(l):
        res.append(binomiale(n, p))
    return np.array(res)


def histo_galton(l, n, p):
    """histo_galton: int,int,float -> void"""
    r = galton(l, n, p)
    bins = len(np.unique(r))
    data, bins, patchs = plt.hist(r, bins=bins)  # bins = nombre colonne.
    plt.show()


# II.1
def normale(k, s):
    """normale : int,float -> float np.array
    Renvoie un tableau numpy de floats représentant une probabilité affine.
    - k doit être impair"""
    liste = []
    if k % 2 == 0:  # Si k pair
        raise ZeroDivisionError("Division par zero, k pair")
    else:
        X = np.linspace(-2 * s, 2 * s, k)
        for i in X:
            liste.append(
                1 / (s * np.sqrt(2 * np.pi)) * np.exp(-0.5 * ((i) / s) ** 2)
            )  # Fonction densité loi Normale
    return np.array(liste)


# II.2
def proba_affine(k, slope):
    """proba_affine : int , float -> float np.array
    Renvoie un tableau numpy de floats représentant une probabilité affine.
    - k doit être impair"""
    tab = []
    if k % 2 == 0:
        raise ValueError("le nombre k doit etre impair")
    if abs(slope) > 2.0 / (k * k):
        raise ValueError("la pente est trop raide : pente max = " + str(2.0 / (k * k)))
    else:
        for i in range(0, k, 1):
            tab.append(1 / k + (i - (k - 1 / 2)) * slope)
    return tab


# II.3
def Pxy(x, y):
    """Pxy : float np.array , float np.array -> float np.2D-array"""
    array = np.zeros((len(x), len(y)))
    for i in range(len(x)):
        for j in range(len(y)):
            array[i, j] = x[i] * y[j]

    return array


# III.1
def calcYZ(P_XYZT):
    P_YZ = np.zeros((2, 2))  # matrice de 0
    for x in range(
        P_XYZT.shape[0]
    ):  # numpy.ndarray.shape attribute ndarray.shape Tuple of array dimensions
        # longueur de chaque ligne
        for y in range(P_XYZT.shape[1]):
            for z in range(P_XYZT.shape[2]):
                for t in range(P_XYZT.shape[3]):
                    P_YZ[y][z] += P_XYZT[x][y][z][t]
    return P_YZ


# III.1
def calcXTcondYZ(P_XYZT):
    P_YZ = calcYZ(P_XYZT)
    P_XTcondYZ = np.zeros((2, 2, 2, 2))
    for x in range(P_XYZT.shape[0]):
        for y in range(P_XYZT.shape[1]):
            for z in range(P_XYZT.shape[2]):
                for t in range(P_XYZT.shape[3]):
                    P_XTcondYZ[x][y][z][t] += P_XYZT[x][y][z][t] / P_YZ[y][z]

    return P_XTcondYZ


# III.1
def calcX_etTcondYZ(P_XYZT):
    P_XTcondYZ = calcXTcondYZ(P_XYZT)
    P_XcondYZ = np.zeros((2, 2, 2))
    P_TcondYZ = np.zeros((2, 2, 2))
    for x in range(P_XYZT.shape[0]):
        for y in range(P_XYZT.shape[1]):
            for z in range(P_XYZT.shape[2]):
                for t in range(P_XYZT.shape[3]):
                    P_XcondYZ[x][y][z] += P_XTcondYZ[x][y][z][t]
                    P_TcondYZ[y][z][t] += P_XTcondYZ[x][y][z][t]
    return P_XcondYZ, P_TcondYZ


# III.1
def testXTindepCondYZ(P_XYZT, epsilon):
    a = calcXTcondYZ(P_XYZT)
    b, c = calcX_etTcondYZ(P_XYZT)

    for x in range(P_XYZT.shape[0]):
        for y in range(P_XYZT.shape[1]):
            for z in range(P_XYZT.shape[2]):
                for t in range(P_XYZT.shape[3]):
                    if abs(a[x][y][z][t] - (b[x][y][z] * c[y][z][t])) > epsilon:
                        return False

    return True


# III.2
def testXindepYZ(P_XYZT, epsilon):
    P_XYZ = np.zeros((2, 2, 2))  # création matrice
    for x in range(P_XYZT.shape[0]):
        for y in range(P_XYZT.shape[1]):
            for z in range(P_XYZT.shape[2]):
                for t in range(P_XYZT.shape[3]):
                    P_XYZ[x][y][z] += P_XYZT[x][y][z][t]

    P_X = np.zeros((2))
    for x in range(P_XYZT.shape[0]):
        for y in range(P_XYZT.shape[1]):
            for z in range(P_XYZT.shape[2]):
                P_X[x] += P_XYZ[x][y][z]

    a = P_XYZ
    b = P_X
    c = calcYZ(P_XYZT)

    for x in range(P_XYZT.shape[0]):
        for y in range(P_XYZT.shape[1]):
            for z in range(P_XYZT.shape[2]):
                if abs(a[x][y][z] - (b[x] * c[y][z])) > epsilon:
                    return False

    return True


# IV.1
def conditional_indep(P, X, Y, Zs, epsilon):
    '''Potential,str,str,list[str]->bool'''
    # on met dans une liste toutes les variables qui nous interesse
    Liste = Zs.copy()
    Liste.append(X)
    Liste.append(Y)
    # on supprime de P les arguments qui nous interesse pas
    Pfiltre = P.margSumIn(Liste)
    pXYcondZs = Pfiltre / Pfiltre.margSumOut([X, Y])
    pXcondZs = pXYcondZs.margSumOut([Y])
    pYcondZs = pXYcondZs.margSumOut([X])
    if (pXYcondZs - (pXcondZs * pYcondZs)).abs().max() < epsilon:
        print("==> ", X, " et ", Y, " sont indépendants conditionnellement à ", Zs)
        print(
            "Variation entre les P = ", (pXYcondZs - (pXcondZs * pYcondZs)).abs().max()
        )
        return True
    else:
        print("=> pas d'indépendance trouvée")
        return False


def compact_conditional_proba(P, X):
    '''Potential,str-> Potential'''
    
    if P.domainSize() <= 2: # Lorsque le tableau est vide on retourne le tableau car on ne peut plus compacter
        return P
    
    K = P.var_names # Ensemble des variables dans P
    K.remove(X)
    for k in K:
        K_tmp = K.copy()
        K_tmp.remove(k)
        if conditional_indep(P, k, X, K,1e-5): # Check si les variables dans K sont independantes
            K.remove(k) # Supprime de la liste si independantes
    lvb = []
    lvb.append(X)
    for k in K:
        lvb.append(k)
    PX_K = P.margSumIn(lvb) / P.margSumIn(K) 
    PX_K = PX_K.putFirst(X)    
    return PX_K  

def create_bayesian_network(P,vp):
    '''Potential -> Potential list'''
    res = []
    liste_noms = P.var_names
    for X_i in reversed(liste_noms):
        
        Q = compact_conditional_proba(P, X_i)
              
        res.append(Q)
        P = P.margSumOut(X_i)
    return res

def calcNbParams(Pjointe):
    '''Potential -> int,int'''
    rb = 0
    baye = create_bayesian_network(Pjointe,0.001)
    for i in baye:
        rb += i.domainSize()
    j= Pjointe.toarray().size

    return j,rb
