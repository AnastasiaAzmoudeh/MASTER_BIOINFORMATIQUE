import numpy as np
import utils
import scipy.stats as stats
import pydot
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pyAgrum as gum
import pyAgrum.lib.ipython as gnb
#AZMOUDEH
#ZEDIRA

# fonction pour transformer les données brutes en nombres de 0 à n-1
def translate_data ( data ):
    # création des structures de données à retourner
    nb_variables = data.shape[0]
    nb_observations = data.shape[1] - 1 # - nom variable
    res_data = np.zeros ( (nb_variables, nb_observations ), int )
    res_dico = np.empty ( nb_variables, dtype=object )

    # pour chaque variable, faire la traduction
    for i in range ( nb_variables ):
        res_dico[i] = {}
        index = 0
        for j in range ( 1, nb_observations + 1 ):
            # si l'observation n'existe pas dans le dictionnaire, la rajouter
            if data[i,j] not in res_dico[i]:
                res_dico[i].update ( { data[i,j] : index } )
                index += 1
            # rajouter la traduction dans le tableau de données à retourner
            res_data[i,j-1] = res_dico[i][data[i,j]]
    return ( res_data, res_dico )


# fonction pour lire les données de la base d'apprentissage
def read_csv ( filename ):
    data = np.loadtxt ( filename, delimiter=',', dtype=np.str ).T
    names = data[:,0].copy ()
    data, dico = translate_data ( data )
    return names, data, dico

def create_contingency_table ( data, dico, x, y, z ):
    # détermination de la taille de z
    size_z = 1
    offset_z = np.zeros ( len ( z ) )
    j = 0
    for i in z:
        offset_z[j] = size_z      
        size_z *= len ( dico[i] )
        j += 1

    # création du tableau de contingence
    res = np.zeros ( size_z, dtype = object )

    # remplissage du tableau de contingence
    if size_z != 1:
        z_values = np.apply_along_axis ( lambda val_z : val_z.dot ( offset_z ),
                                         1, data[z,:].T )
        i = 0
        while i < size_z:
            indices, = np.where ( z_values == i )
            a,b,c = np.histogram2d ( data[x,indices], data[y,indices],
                                     bins = [ len ( dico[x] ), len (dico[y] ) ] )
            res[i] = ( indices.size, a )
            i += 1
    else:
        a,b,c = np.histogram2d ( data[x,:], data[y,:],
                                 bins = [ len ( dico[x] ), len (dico[y] ) ] )
        res[0] = ( data.shape[1], a )
    return res

def sufficient_statistics( data, dico, x, y, z ):
    
        # création du tableau de contingence
    table = create_contingency_table ( data, dico, x, y, z )
    nb_z = table.shape[0]
    nb_x, nb_y = table[0][1].shape

    # si l'on a trop peu de données pour le test, on arrête le test
    # et on considère qu'il y a indépendance
    if data.shape[1] < 5 * nb_z * nb_x * nb_y:
        return ( -1, 1 ) # stat = -1 => indépendance

    # calcul de la statistique
    stat = 0.0
    nb_z_positive = 0
    for z in range ( nb_z ):
        N_z = table[z][0]

        if N_z != 0:
            nb_z_positive += 1     

            N_xz = np.apply_along_axis ( lambda vx : vx.sum (),
                                         1, table[z][1] )
            N_yz = np.apply_along_axis ( lambda vx : vx.sum (),
                                         0, table[z][1] )
            N_xyz = np.outer ( N_xz, N_yz ) / N_z

            denominateur = np.where ( N_xyz == 0, 1, N_xyz )
            numerateur = table[z][1] - N_xyz
            stat += ( numerateur * numerateur / denominateur ).sum ()

    # on calcule le nombre de degrés de liberté
    ddl = (nb_x - 1) * (nb_y - 1) * nb_z_positive

    return ( stat, ddl )

def indep_score ( data, dico, x, y, z ):
    tab = create_contingency_table ( data, dico, x, y, z )
    nb_z = tab.shape[0]
    nb_x, nb_y = tab[0][1].shape
    nb_lignes=len(data[0])
    
    dmin=5*nb_x*nb_y*nb_z #𝑑𝑚𝑖𝑛=5×|𝑋|×|𝑌|×|𝐙|
    
    if dmin>nb_lignes: # si le nombre de lignes du CSV est supérieure ou égale à  𝑑𝑚𝑖𝑛=, 
                        #le test est considéré comme valide.
        return (-1, 1)  # stat = -1 => indépendance
    
    X2,dof=sufficient_statistics ( data, dico, x, y, z ) #dof = degree of freedom
    p=stats.chi2.sf(X2,dof)
    return p, dof

def best_candidate ( data, dico, x, z, risk_level ):
    resultat = []
    pmin = risk_level
    
    for y in range(x): #Y parmi toutes celles à gauche de  𝑋
        p , dof = indep_score ( data, dico, x, y, z ) 
        
        #on regarde si p-value est inferieur a risk_level et on stock cette valeur dans pmin
        #on changera pmin si on trouve un p-value encore plus petit que le precedent
        if p < risk_level and p <pmin:
            pmin = p
            resultat = [y]
            
    return resultat

def create_parents ( data, dico, x, risk_level ):
    z = []
    #si best_candidate (data, dico, x,z, risk_level  ) vous renvoie une liste non vide [y], rajoutez y à z
    y = best_candidate( data, dico, x,z, risk_level )
    z.extend(y)

    #on continu tant que best_candidate renvoie une liste non vide
    while y != [] :
        y = best_candidate( data, dico, x, z, risk_level )
        z.extend(y)
    
    
    return z
def learn_BN_structure ( data, dico, risk_level ):
    resultat =[]
    
    #pour chaque variable on cherche ses parents
    for x in range(len(data)):
        z = create_parents(data, dico, x, risk_level )
        resultat.append(z)
    
    return np.asarray(resultat, dtype=object)

style = { "bgcolor" : "#6b85d1", "fgcolor" : "#FFFFFF" }

def display_BN ( node_names, bn_struct, bn_name, style ):
    graph = pydot.Dot( bn_name, graph_type='digraph')

    # création des noeuds du réseau
    for name in node_names:
        new_node = pydot.Node( name,
                               style="filled",
                               fillcolor=style["bgcolor"],
                               fontcolor=style["fgcolor"] )
        graph.add_node( new_node )

    # création des arcs
    for node in range ( len ( node_names ) ):
        parents = bn_struct[node]
        for par in parents:
            new_edge = pydot.Edge ( node_names[par], node_names[node] )
            graph.add_edge ( new_edge )

    # sauvegarde et affaichage
    outfile = bn_name + '.png'
    graph.write_png( outfile )
    img = mpimg.imread ( outfile )
    plt.imshow( img )
    

def learn_parameters ( bn_struct, ficname ):
    # création du dag correspondant au bn_struct
    graphe = gum.DAG ()
    nodes = [ graphe.addNode () for i in range (len(bn_struct)) ]
    for i in range ( len(bn_struct) ):
        for parent in bn_struct[i]:
            graphe.addArc ( nodes[parent], nodes[i] )

    # appel au BNLearner pour apprendre les paramètres
    learner = gum.BNLearner ( ficname )
    learner.useScoreLog2Likelihood ()
    learner.useAprioriSmoothing ()
    return learner.learnParameters ( graphe )


