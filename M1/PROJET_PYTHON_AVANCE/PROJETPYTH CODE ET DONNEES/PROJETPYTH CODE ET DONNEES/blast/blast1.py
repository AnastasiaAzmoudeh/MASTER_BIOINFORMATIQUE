import psycopg2

conn=psycopg2.connect("dbname=aa_proj")
cur=conn.cursor()
fichier="QUERY-GCA_000014865.1_ASM1486v1_translated_cds__DB-GCA_000009985.1_ASM998v1_translated_cds.out"
ll=[]
f=open(fichier)
for lines in f.readlines():
    if lines[0]=="#":
        continue
    else:
        ll.append(lines.split())

for i in range(len(ll)):
    ll[i][0]=ll[i][0].strip("lcl|")
    
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



for e in RES:
    #cur.execute("INSERT INTO BLASTINTERM (qseqid,sseqid,pident,length,mismatch,gapopen,qstart,qend,sstart,send,evalue,bitscore) VALUES ('ll[i][0]','ll[i][1]',ll[i][2],ll[i][3],ll[i][4],ll[i][5],ll[i][6],ll[i][7],ll[i][8],ll[i][9],ll[i][10],ll[i][11])")
    
    cur.execute("INSERT INTO BLASTINTERM (qseqid,sseqid,pident,length,mismatch,gapopen,qstart,qend,sstart,send,evalue,bitscore) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(e[0],e[1],e[2],e[3],e[4],e[5],e[6],e[7],e[8],e[9],e[10],e[11]))


conn.commit()
conn.close()