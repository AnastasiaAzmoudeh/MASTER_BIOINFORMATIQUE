import numpy as np
import pydot
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
np.random.seed(0)

#AZMOUDEH
#ZEDIRA


def exp(lamb): 
    x=np.random.rand(*lamb.shape)
    return -np.log(1.0-x)/np.where(lamb==0,1e-200,lamb)

# returns dense numpy arrays of k,r parameters for graph links fr -> to 
def get_kr_for(graph,fr,to):
    _,gk,gr=graph
    k=np.array([[gk.get((i, v),0) for v in to] for i in fr])
    r=np.array([[gr.get((i, v),0) for v in to] for i in fr])
    return k,r


def simulation(graph,sources, maxT):
   
    names,gk,gr=graph
    nbNodes=len(names)
    infectious= np.zeros(nbNodes)# maxT partout + 0 sur les sources
    infectious+=maxT
    infectious[sources]= 0
    # infectious sera le vecteur de travail dans lequel on élimine
    
    # les noeuds traités
    # => On crée aussi un vecteur times, qui sera celui contentant les
    # temps de référence à retourner
    times = np.copy(infectious) 
    while True: 
        #si il n'y a plus de contaminant on break
        if np.all(infectious == maxT) :
            break
            
        #  le noeud contaminant à cette itération = argmin dans infectious
        contaminant = np.argmin(infectious)
        #  le temps associé à la contamination: Tref
        Tref = times[contaminant]
        # ( élimination du noeud en mettant sa valeur ) maxT dans infectious => il ne sera plus sélectionné
        infectious[contaminant] = maxT
        # critère de sortie: il n'y a plus de noeuds contaminant possible
        if Tref == maxT :
            break
        # les indices des cibles (temps de contamination > Tref)
        cibles =[]
        for i in range(nbNodes) :
            #on cherche les transitions qui partent de notre noeud contaminant
            if (contaminant,i) in gk :
                cibles.append(i)
                
        # les paramètres des modèles entre le noeud source et les cibles:
        params = get_kr_for(graph,[contaminant],cibles) # récupération des paramètres vers les cibles
        
        # tirage Bernoulli selon params[0][0]
        conta = np.random.binomial(1, params[0][0])
        # tirage Exp selon params[1][0]
        delta=exp(params[1][0]) + Tref

       

        for i in range(len(conta)):
            #si =0 il est pas contamine
            if conta[i] == 0:
                continue
            if delta[i]<times[cibles[i]]:
                # mettre à jour times
                times[cibles[i]] = delta[i]
                # mettre à jour infectious
            infectious[cibles[i]] = delta[i]
            
 
    return times


def getProbaMC(graph,sources, maxT, nbsimu):
    names,gk,gr=graph # eclatement du graphe
    nbNodes=len(names)
    rInf= np.zeros(nbNodes) # nb d'infection de chaque noeud dans la simulation suivante
   
    # boucle for sur nbsimu
    for i in range(nbsimu):
        #Réalisation d'une simulation
        simul=simulation(graph,sources,maxT)
        #Incrément pour les noeuds contaminés dans la simulation
        simul[simul != maxT] = 1
        simul[simul == maxT] = 0
        rInf += simul
    # retour de rInf (normalisé en fréquence et pas en comptage)
    return rInf/nbsimu

def getProbaMC2(graph,sources, maxT, nbsimu):
    names,gk,gr=graph # eclatement du graphe
    nbNodes=len(names)
    rInf= np.zeros(nbNodes) 
    
    
    rInf=np.zeros((len(graph[0])))
    for i in range(nbsimu):
        simul=simulation(graph,sources,maxT)
        simul=np.where(simul<maxT,simul,simul-10)  #on soustrait les non-infectes=maxT
        simul=np.where(simul==0,simul,simul-simul+1) #on met des 1 la ou ya infection
        rInf+=simul
    rInf[sources]=nbsimu  #les sources sont toujours infecte
    return rInf/nbsimu

def getPredsSuccs(graph):
    names,gk,gr=graph
    nbNodes=len(names)
    preds={}
    succs={}
    for (a,b),v in gk.items():
        s=succs.get(a,[])
        s.append((b,v,gr[(a,b)]))
        succs[a]=s
        p=preds.get(b,[])
        p.append((a,v,gr[(a,b)]))
        preds[b]=p
    
    return (preds,succs)



def compute_ab(v, times, preds, maxT, eps):
    predsV=preds.get(v,[])
    t=times[v]
    if t==0:
        return (1,0)
    a=eps
    b=0
    if len(predsV)>0:
        c,k,r=map(np.array,zip(*predsV)) 
        
       
        somme_alpha_sur_beta = 0
        somme_log_beta = 0
        
        tpred = times[c]
      
        alpha = np.zeros(len(predsV))
        beta = np.zeros(len(predsV))
        for i in range(len(predsV)):
            if 0<= tpred[i] and tpred[i]< t :
                alpha[i] = k[i]*r[i]*np.exp(-r[i]*(t-tpred[i]))
                beta[i] =k[i]*np.exp(-r[i]*(t-tpred[i]))+1-k[i]
                
        for i in range(len(predsV)):
            if beta[i] != 0 :
                somme_alpha_sur_beta += alpha[i]/beta[i]
                somme_log_beta += np.log(beta[i])

       
        b=somme_log_beta
        
        if t<maxT:
      
            a=np.maximum(eps,somme_alpha_sur_beta)
       
        else:
       
            a=1.0
        
            
                
    
    return (a,b)


def compute_ll(times,preds, maxT):
    
    ll=1
    sa=np.zeros(len(times))
    sb=np.zeros(len(times))
    # = calcul de a,b pour tous les v
    for i in range(len(times)):
        a,b=compute_ab(i,times,preds,maxT,1e-20)
        sa[i]=a
        sb[i]=b
    # calcul de la log-vraisemblance
    for i in range(len(times)):
        ll *= np.exp(np.log(sa[i])+sb[i])
    ll = np.log(ll)
    
    return ll,sa,sb

def addVatT(v,times,newt,preds,succs,sa,sb, maxT):
    t=times[v]
    if t>=0:
        raise Error("v  must have been removed before")
  
 
    times[v]=newt
    sa[v],sb[v]=compute_ab(v,times,preds,maxT,1e-20)
    for i in preds:  
        sa[i],sb[i]=compute_ab(i,times,preds,maxT,1e-20)
    
    
    return

def logsumexp(x,axis=-1):
    xstar=np.amax(x) #maximum d'un array
    return xstar+np.log( np.sum(np.exp(x-xstar),axis))

def removeV(v,times,succs,sa,sb,eps=1e-20):
    succs=succs.get(v,[])
    t=times[v]
    if t<0:
        return 
    times[v]=-1
    sa[v]=1.0
    sb[v]=0.0
    if len(succs)>0:
        c,k,r=map(np.array,zip(*succs))
        tp=times[c]
        which=(tp>t)

        tp=tp[which]
        dt=tp-t
        k=k[which]
        r=r[which]
        c=c[which]
        rt = -r*dt
        b1=k*np.exp(rt)
        b=b1+1.0-k

        a=r*b1
        a=a/b
        b=np.log(b)
        #maxT=10
        sa[c]=sa[c]-np.where(tp<10,a,0.0)
        sa[c]=np.where(sa[c]>eps,sa[c],eps)
        sb[c]=sb[c]-b
        sb[c]=np.where(sb[c]>0,0,sb[c])




def getLL(v,times,nt,preds,succs,sa,sb,maxT,onUsers=None):
    sa=np.copy(sa)
    sb=np.copy(sb)
    if onUsers is None:
        onUsers=range(len(times))
    addVatT(v,times,nt,preds,succs,sa,sb,maxT)
    times[v]=-1
    ll=np.sum((np.log(sa)+sb)[onUsers])
    return (ll,sa,sb)

  
def sampleV(v,times,preds,succs,sa,sb,maxT,k,k2):

    nbCandidateT=k
    bounds=np.linspace(0,maxT,nbCandidateT)
    newt=np.random.uniform(bounds[:-1],bounds[1:])

    if times[v]<maxT:
        idx = newt.searchsorted(times[v])
        newt=np.concatenate((newt[:idx], [times[v]], newt[idx:]),axis=0)
        nbCandidateT+=1
    newt=np.append(newt,[maxT])

    if v in succs:
        c,_,_=map(list,zip(*succs.get(v,[])))
    else:
        c=[]
    c.append(v)
    c=np.array(c)
    oldll=np.sum((np.log(sa)+sb)[c])
    otime=times[v]
    nsa=np.copy(sa)
    nsb=np.copy(sb)
    removeV(v,times,succs,nsa,nsb)
    lls=[getLL(v,times,nt,preds,succs,nsa,nsb,maxT,onUsers=c) for nt in newt]
    ll,la,lb=zip(*lls)
    ll=list(ll)
    ll=np.array(ll)

    diffsx=(newt[1:]-newt[:-1])/2.0
    diffsx[1:]=diffsx[1:]+diffsx[:-1]
    diffsx[0]+=newt[0]
    diffsx[-1]+=(maxT-newt[nbCandidateT-1])/2.0
    areas=np.log(diffsx)+ll[:-1]
    lln=np.append(areas,ll[-1])


    p=np.exp(lln-tme10.logsumexp(lln))


    i=np.random.choice(range(len(p)),1,p=p).sum()
    if i==(len(p)-1):
        times[v]=maxT
        np.copyto(sa,np.array(la[-1]))
        np.copyto(sb,np.array(lb[-1]))
    else: 
        if i>0: 
            bi=(newt[i]+newt[i-1])/2.0
        else:
            bi=0
        if i<(len(p)-2): 
            bs=(newt[i]+newt[i+1])/2.0
        else:
            bs=maxT
        bounds=np.linspace(bi,bs,k2)
        newt=np.concatenate(([newt[i]],np.random.uniform(bounds[:-1],bounds[1:])))
        lls=[getLL(v,times,nt,preds,succs,nsa,nsb,maxT,onUsers=c) for nt in newt]
        ll,la,lb=zip(*lls)
        ll=np.array(ll)
        p=np.exp(ll-tme10.logsumexp(ll))

        i=np.random.choice(range(len(p)),1,p=p).sum()

        times[v]=newt[i]
        np.copyto(sa,np.array(la[i]))
        np.copyto(sb,np.array(lb[i]))


#??????



#ne marche pas du tout 

# def gb(graph,infections,maxT,sampler,burnin,ref,period,k1,k2):
#     nbNodes=len(graph[0])
#     times=np.array([maxT]*nbNodes,dtype=float)
#     eps=1e-5
#     times_copy=times.copy()
#     preds,succs=getPredsSuccs(graph)
#     mses = []
#     times_arr = []
#     for i in range(period):
#         choice_list = np.arange(nbNodes)
#         for _ in range(nbNodes):
#             ll,sa,sb=compute_ll(times_copy,preds, maxT, eps)
#             v = np.random.choice(choice_list)
#             np.delete(choice_list, v)
#             sampler(v,times_copy,preds,succs,sa,sb,k1,k2)
#             if i > burnin:
#                 times_arr.append(times_copy)
#                 mses.append((times_copy-ref)**2)
#     return mses
