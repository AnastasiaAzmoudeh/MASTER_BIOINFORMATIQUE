#AZMOUDEH ANASTASIA
#lire fichier fasta
def lire_fichier(fichier):
    f=open(fichier)
    chev=[]
    chevdico={}
    cpt=1
    seqlist=[]
    for lines in f.readlines():
        #print(lines)
        if lines[0]==">":
            chev.append(lines.split())
            chevdico[lines[5:-1]]=cpt
            cpt+=1
            


        
    names = [] 
    sequences = [] 
        
    f = open(fichier)
    une_seq = []
        
    for lines in f.readlines():
            
        if lines[0]== ">":
            sequences.append(une_seq) 
            une_seq = []
            if lines[-1]=="\n": 
                names.append(lines[1:-1])
            else: 
                names.append(lines[1:])
                    
        else:
            if lines[-1]=="\n": 
                une_seq.append(lines[:-1])
            else: 
                une_seq.append(lines)
                

    sequences.append(une_seq)
    sequences = sequences[1:] 
        
    nvlles_seq = []
    for liste in sequences: 
        longueur = len(liste)
        liste = [''.join(liste[:longueur])] 
        nvlles_seq.append(liste)
        
        
    lg=[]

    for i in range(len(nvlles_seq)):
        lg.append(len(nvlles_seq[i][0]))
            
    tmp=[]
    for i in range(len(chev)):
        chev[i][0]=chev[i][0].strip(">lcl|")
        stra=' '.join(chev[i])
        tmp.append(stra)

        
    dicofinal={}

    for i in range(len(chev)):
        dicofinal[chev[i][0]]=(chevdico[tmp[i]],lg[i])
    #print(dicofinal)

    return dicofinal

#lire blast 

def lire_blast(fichier):


    ff=open(fichier)

    res=[]

    for lines in ff.readlines():
        if lines[0]=="#":
            continue
        else:
            res.append(lines.split())
    for i in range(len(res)):
        res[i][0]=res[i][0].strip("lcl|")
    #print(res[0:5])

    dicores={}

    for i in range(len(res)):
        dicores[(res[i][0],res[i][1])]=res[i][10]
    
    return dicores

#fichier="QUERY-GCA_000014865.1_ASM1486v1_translated_cds__DB-GCA_000009985.1_ASM998v1_translated_cds.out"
def lire_blast_remplir(fichier):
    
    ll=[]
    f=open(fichier)
    for lines in f.readlines():
        if lines[0]=="#":
            continue
        else:
            ll.append(lines.split())

    for i in range(len(ll)):
        ll[i][0]=ll[i][0].strip("lcl|")
        ll[i][1]=ll[i][1].strip("lcl|")
        
        ll[i][2]=float(ll[i][2])
        ll[i][3]=float(ll[i][3])
        ll[i][4]=float(ll[i][4])
        ll[i][5]=float(ll[i][5])
        ll[i][6]=float(ll[i][6])
        ll[i][7]=float(ll[i][7])
        ll[i][8]=float(ll[i][8])
        ll[i][9]=float(ll[i][9])
        ll[i][10]=float(ll[i][10])
        ll[i][11]=float(ll[i][11])


    dico={}
    RES=[]

    for l in ll:

        if (l[0],l[1]) not in dico:
            q=l[0]
            s=l[1]

            
            dico[(q,s)]=[l]
            
        else:
            q=l[0]
            s=l[1]

            dico[(q,s)].append(l)
            
            

    temp={}
    for key,val in dico.items():
        t=[]
        if len(val)==1:
            for v in val: 
                temp[key]=v
        else:
            for v in val:
            
                t.append(v[10])
            vmin=min(t)
        
            indvmin=t.index(vmin)
            temp[key]=val[indvmin]



    for key,val in temp.items():
        RES.append(val)

    return RES


def etape0(file):
    
 
    
    liste_ligne = [] # liste des lignes
    
    
    f=open(file)
    lines=f.readlines()
    
    
    for line in lines: 
        if line[-1] == '\n':
            liste_ligne.append(line[:-1]) 
                                
        else: 
            liste_ligne.append(line)
    

    return liste_ligne

def make_drop(fichier_especes,fichier_assembly):
    list_especes=etape0(fichier_especes)
    list_assembly=etape0(fichier_assembly)
    drop=[]
    for i in range(len(list_assembly)):
        if list_assembly[i]=="vide1" or list_assembly[i]=="vide2" or list_assembly[i]=="vide3":
            ind=list_assembly.index(list_assembly[i])
            o=list_especes[ind]
            print(o)
            org=o.split()
            print(org)
            orga=org[0][0:8]
            print(orga)
            drop.append(orga)
        else:
            drop.append(list_assembly[i])
    return drop
