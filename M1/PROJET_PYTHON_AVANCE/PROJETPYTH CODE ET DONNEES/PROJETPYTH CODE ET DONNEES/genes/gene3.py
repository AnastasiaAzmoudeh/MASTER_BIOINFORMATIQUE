import psycopg2

conn=psycopg2.connect("dbname=aa_proj")
cur=conn.cursor()
fichier="GCA_000026265.1_ASM2626v1_translated_cds.faa"
f=open(fichier)
chev=[]
chevdico={}
cpt=1
for lines in f.readlines():

    if lines[0]==">":
        chev.append(lines.split())
        chevdico[lines[5:-1]]=cpt
        cpt+=1

names = [] # contient les noms des séquences du fichier FASTA
sequences = [] # contient les séquences présentes dans le fichier FASTA
    
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
sequences = sequences[1:] # pour supprimer la première liste qui est vide
    
nvlles_seq = []
for liste in sequences: 
    longueur = len(liste)
    liste = [''.join(liste[:longueur])] # pour qu'une même séquence écrite sur 2 lignes du fichier FASTA soit dans un seul item de la liste 
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
    

cur.execute("SELECT nomorg,assembly FROM organisme\
             WHERE assembly = 'GCA_000026265.1'")
             
res = cur.fetchall()


for key,val in dicofinal.items():
    pos,lg=val
    #cur.execute("INSERT INTO BLASTINTERM (qseqid,sseqid,pident,length,mismatch,gapopen,qstart,qend,sstart,send,evalue,bitscore) VALUES ('ll[i][0]','ll[i][1]',ll[i][2],ll[i][3],ll[i][4],ll[i][5],ll[i][6],ll[i][7],ll[i][8],ll[i][9],ll[i][10],ll[i][11])")
    
    cur.execute("INSERT INTO GENE (nomgene,assembly,nomorg,ranggene,lgseq) VALUES (%s,%s,%s,%s,%s)",(key,res[0][1],res[0][0],pos,lg))


conn.commit()
conn.close()