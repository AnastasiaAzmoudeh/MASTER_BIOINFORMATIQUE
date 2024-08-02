import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pickle as pkl

#AZMOUDEH 
#ZEDIRA

def labels_tobinary(Y, cl):
    return np.where(Y > cl, 0., 1.)

#def pred_lr(X, A ,i):
    #pass

def pred_lr(X, w, b):

    #if w.shape[0] != X.shape[1]:
    #    w = w.T
    # Calcul de la combinaison linéaire
    z = np.dot(X, w) + b
    
    # Application de la fonction sigmoïde
    proba = 1 / (1 + np.exp(-z))
    
    # Prédiction de classe (0 ou 1)
    #prediction = np.where(probability > 0.5, 1, 0)
    
    
    return proba

def classify_binary(Y_pred):
    predictions = np.where(Y_pred> 0.5, 1., 0.)
    
    return predictions

def accuracy(predictions, labels):
    # Comparaison des prédictions avec les vraies étiquettes
    correct_predictions = np.equal(predictions, labels)
    # Calcul du taux de bonne classification
    accuracy = np.mean(correct_predictions)
    return accuracy



def rl_gradient_ascent(X,Y,eta, niter_max):
    w=np.zeros(X.shape[1])
    b=0
    accs=[]

    for it in range(niter_max):
        z=np.dot(X,w)+b
        p=(1/(1+np.exp(-z)))

        grad_w=np.dot(X.T, Y - p)
        grad_b=np.sum(Y-p)

        w+=eta*grad_w

        b+=eta*grad_b

        

        predictions = classify_binary((p))
        #accs=accuracy(predictions, Y)
        accs.append(accuracy(predictions, Y))

        if np.linalg.norm(eta * grad_w) < 1e-6:
            print(f"Convergence atteinte à l'itération {it + 1}")
            break
    
    #print("liste accs = ",accs)

    return w,b,accs,it+1


def visualization(w):
    # Visualisation du vecteur de poids sans le biais
    plt.figure()
    plt.imshow(w.reshape(16, 16), cmap='gray')
    plt.colorbar()  # Ajoute une barre de couleur pour indiquer les valeurs
    plt.savefig("wrla.png")




def rl_gradient_ascent_one_against_all(X,Y,epsilon, niter_max):
    
    N,d = X.shape
    classes = np.unique(Y)
    # Initialiser les poids & lancer un modèle par classe
    w = np.zeros((len(classes), d))
    # dans la boucle for, vous pouvez utiliser : Y_tmp = np.where(Y == c, 1., 0.)
    for i in classes : 
        w[int(i)], b ,accs,it = rl_gradient_ascent(X, Y==i,epsilon,niter_max)
        print("classe %d : acc train %.2f %%" %(i,accs[it-1]*100))
    
    
    w=w.T
    return w,b

def classif_multi_class(Y_pred):
    predicted_classes = np.argmax(Y_pred, axis=1)
    
    return predicted_classes


#Quelle limitation sur l'encodage des pixels noirs (à 0) cette visualisation met-elle en évidence ? Expliquer.
#La limitation est que qu'il se peut que le modèle ne pas être suffisamment robuste 
#pour prendre en compte les informations importantes qui pourraient être codées dans des pixels noirs.
#(par exemple la pertinence des pixels,le manque d'informations, la dépendance aux couleurs des pixels)
#Il faudrait explorer de manière plus approfondie les caractéristiques de l'image et les stratégies pour capturer les informations #manquantes. 
#Cela permetterait d'améliorer les performances du modèle, en particulier pour les images mal classées.


def normalize(X):
    return X - 1


def pred_lr_multi_class(X, W, b):
    # Calcul de la combinaison linéaire
    s = np.dot(X, W) + b
    
    # Application de la fonction softmax
    exp_s = np.exp(s)
    Y_pred = exp_s / np.sum(exp_s, axis=1, keepdims=True)
    
    return Y_pred

def to_categorical(Y, K):
    # Initialisation d'une matrice de zéros avec le nombre de lignes égal à la taille de Y
    Yc = np.zeros((len(Y), K), dtype=int)
    
    # Remplissage de la matrice avec des 1 selon l'indice de la classe dans Y
    for i in range(len(Y)):
        Yc[i, Y[i]] = 1
    
    return Yc


def rl_gradient_ascent_multi_class(X, Y, eta, numEp, verbose=0):
    N, d = X.shape
    K = len(np.unique(Y))  # Nombre de classes
    Yc = to_categorical(Y, K)  # Encodage one-hot des classes

    W = np.zeros((d, K))
    b = np.zeros(K)

    for epoch in range(numEp):
        # Calcul de la prédiction du modèle
        Y_pred = pred_lr_multi_class(X, W, b)
        # Calcul du gradient
        grad_W = (1/N) * np.dot(X.T, Yc - Y_pred)
        grad_b = (1/N) * np.sum(Yc - Y_pred, axis=0)
        # Mise à jour des paramètres
        W += eta * grad_W
        b += eta * grad_b

        # Calcul de l'accuracy
        accuracy_train = accuracy(classif_multi_class(Y_pred), Y)
        
        if verbose and epoch % 100 == 0:
            print("epoch {} accuracy train={:.2f} %".format(epoch, accuracy_train * 100))

    return W, b


def rl_gradient_ascent_multi_class_batch(X, Y, tbatch, eta, numEp, verbose=0):

    num_samples = len(Y)
    Y_hot = np.zeros((num_samples, 10))
    Y_hot[np.arange(num_samples), Y] = 1
    N, d = X.shape
    K = Y_hot.shape[1]
    W = np.zeros((d, K))
    b = np.zeros(K)

    for epoch in range(numEp):
        for start in range(0, N, tbatch):
            end = start + tbatch
            if end > N:
                end = N

            X_batch = X[start:end, :]
            Y_batch = Y_hot[start:end, :]

            Y_pred = pred_lr_multi_class(X_batch, W, b)
            Yc = to_categorical(Y_batch.argmax(axis=1), K)
            #Yc = Y_batch

            grad_w = np.dot(X_batch.T, Yc - Y_pred)
            grad_b = np.sum(Yc - Y_pred, axis=0)

            W += eta * grad_w / tbatch
            b += eta * grad_b / tbatch

        if verbose:
            predictions_one_hot = classif_multi_class(pred_lr_multi_class(X, W, b))
            predictions = np.argmax(predictions_one_hot, axis=0)
            acc_train = accuracy(predictions, Y)
            #acc_train = accuracy(classif_multi_class(pred_lr_multi_class(X, W, b)), Y_hot)
            print(f"epoch {epoch} accuracy train={acc_train*100:.2f} %")

    return W, b


