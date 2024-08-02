#AZMOUDEH ANASTASIA 3801677
import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog as fd
from tkinter import messagebox
import sys
import tkinter.ttk as ttk
import subprocess
import psycopg2
import FctLireFiles as fct
from tkinter import scrolledtext


#conn= psycopg2.connect("dbname=aa_proj")

#cur = conn.cursor()



class AAZ_GUI_APP:
    conn= psycopg2.connect("dbname=aa_proj")
    cur = conn.cursor()
    def __init__(self):
        self.T=0
        self.S=0
        self.drop=fct.make_drop("especes3.txt","assembly.txt")
        self.creerInterface()
        

    def creerInterface(self):
        self.gui = tk.Tk()
        self.gui.title("AAZ_GUI_APP")
        # set window size
        self.gui.geometry("700x500")

        #set window color
        self.gui['background']='#a3c1ad'
        self.lab=tk.Label(self.gui,text="~~ W E L C O M E ~~",font=("Cascadia Code",18),bg="#a3c1ad",fg="white")
        self.lab.grid(row=0,column=1)
        self.qlab=tk.Label(self.gui,text=" QUERY ",font=("Cascadia Code",12),bg="#a3c1ad",fg="white")
        self.qlab.grid(row=1,column=0,pady=10)
        self.qcb = ttk.Combobox(self.gui, values=self.drop,font=("Cascadia Code",8))
        self.qcb.grid(row=1, column=1)

        self.qcb.bind("<<ComboboxSelected>>", self.update_list)
        self.qcb.bind("<KeyRelease>", self.update_list)

        self.slab=tk.Label(self.gui,text=" SUBJECT ",font=("Cascadia Code",12),bg="#a3c1ad",fg="white")
        self.slab.grid(row=2,column=0,pady=10)
        self.scb = ttk.Combobox(self.gui, values=self.drop,font=("Cascadia Code",8))
        self.scb.grid(row=2, column=1)

        self.scb.bind("<<ComboboxSelected>>", self.update_list)
        self.scb.bind("<KeyRelease>", self.update_list)




        self.thlab=tk.Label(self.gui,text=" THRESHOLD E-VALUE",font=("Cascadia Code",8),bg="#a3c1ad",fg="white")
        self.thlab.grid(row=3,column=0,pady=10)

        self.the=tk.Entry(self.gui,width=30,bg='#e8f4ea',font="white")
        self.the.insert(0,"Enter e-value threshold")
        self.the.grid(row=3,column=1)

        self.flab=tk.Label(self.gui,text=" FENÊTRE ",font=("Cascadia Code",12),bg="#a3c1ad",fg="white")
        self.flab.grid(row=4,column=0,pady=10)

        self.horizontal=tk.Scale(self.gui,from_=0,to=10,orient=tk.HORIZONTAL,bg="#e8f4ea")
        self.horizontal.grid(row=4,column=1)

        self.stlab=tk.Label(self.gui,text=" STRINGENCE ",font=("Cascadia Code",10),bg="#a3c1ad",fg="white")
        self.stlab.grid(row=5,column=0,pady=10)

        self.horst=tk.Scale(self.gui,from_=0,to=10,orient=tk.HORIZONTAL,bg="#e8f4ea")
        self.horst.grid(row=5,column=1)

        self.steplab=tk.Label(self.gui,text=" STEP/PAS ",font=("Cascadia Code",10),bg="#a3c1ad",fg="white")
        self.steplab.grid(row=6,column=0,pady=10)

        self.step=tk.Scale(self.gui,from_=0,to=5,orient=tk.HORIZONTAL,bg="#e8f4ea")
        self.step.grid(row=6,column=1)

    

        self.btn7=tk.Button(self.gui,text="QUIT",font=("Cascadia Code",10),bg="#a3c1ad",padx=10,command=self.gui.quit)
        self.btn7.grid(row=9,column=1,pady=10,padx=10,ipadx=75)

        #search org
        self.search_org_btn=tk.Button(self.gui,text="SEARCH_ORG",font=("Cascadia Code",10),bg="#a3c1ad",command=self.search_org)
        self.search_org_btn.grid(row=7,column=0,pady=10,padx=10,ipadx=55)

        test_btn=tk.Button(self.gui,text="ANALYSE",font=("Cascadia Code",10),bg="#a3c1ad",command=self.analysis)
        test_btn.grid(row=7, column=1,pady=10,ipadx=65)

        savd=tk.Button(self.gui,text="SAVE DOTPLOT",font=("Cascadia Code",10),bg="#a3c1ad",padx=10,command=self.save_graph)
        savd.grid(row=8,column=0,pady=10,padx=10,ipadx=50)

        self.btn6=tk.Button(self.gui,text="INFOS",font=("Cascadia Code",10),bg="#a3c1ad",padx=10,command=self.get_infos)
        self.btn6.grid(row=8,column=1,pady=10,padx=10,ipadx=70)


        self.gui.mainloop() 
    
    def get_infos(self):
        root = tk.Tk()

        TT="Les diagonales montantes centrées correspondent à des matches entre les deux gènomes\nSi elles sont décalées du centre il s'agit d'une translocation\nLes diagonales descendantes correspondent à des régions géniques inversées"

       
        text_widget = tk.Text(root, height=50, width=150)
        text_widget.insert(tk.END, TT)

        
        text_widget.pack()

    def sort_with_prefix(self,prefix,lst):
            
        prefix_list = []
        non_prefix_list = []
        for item in lst:
            if item.startswith(prefix):
                prefix_list.append(item)
            else:
                non_prefix_list.append(item)
        prefix_list.sort()
        return prefix_list + non_prefix_list

    def update_list(self,event):
        
        self.qcb['values'] = self.sort_with_prefix(self.qcb.get(), self.drop)
        self.scb['values'] = self.sort_with_prefix(self.scb.get(), self.drop)



    def search_org(self):
        self.search_org = tk.Tk()
        self.search_org.title("SEARCH ORG ")
        self.search_org.geometry("800x600")
        conn = psycopg2.connect("dbname=aa_proj")

        cur = conn.cursor()
        self.search_box = tk.Entry(self.search_org)

        def search_now():
            self.searched = self.search_box.get()
            sql = "SELECT nomorg,souche,assembly FROM organisme WHERE nomorg=%s"
            name = (self.searched,)
           
            cur.execute(sql, name)
            result = cur.fetchall()

            if not result:
                result = "L'organisme n'est pas la base de données"

            
            self.searched_text = scrolledtext.ScrolledText(self.search_org, width=100, height=50)
            self.searched_text.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
            
            
            for r in result:
                self.searched_text.insert(tk.END, str(r) + "\n")
            
            
        self.search_box.grid(row=0, column=1, padx=10, pady=10)
        self.search_box_label = tk.Label(self.search_org, text="Search Organism by name")
        self.search_box_label.grid(row=0, column=0, padx=10, pady=10)
        self.search_btn = tk.Button(self.search_org, text="Search", command=search_now)
        self.search_btn.grid(row=1, column=0, padx=10)



    def analysis(self):

        conn=psycopg2.connect("dbname=aa_proj")
        cur=conn.cursor()
        self.query=self.qcb.get()
        self.subject=self.scb.get()
        self.window_size = self.horizontal.get()
        self.window_size=int(self.window_size)
        self.step_size = self.step.get()
        self.step_size=int(self.step_size)
        self.T=self.the.get()
        self.T=float(self.T)
        self.S=self.horst.get()
        self.S=int(self.S)

    
        dico_blast={}
        query_dico={}
        subject_dico={}
        dico_blast_pos_ev={}
        extentionoutput="_translated_cds.faa"




        sqlquery="SELECT * FROM gene WHERE assembly = %s"
        queryassembly=(self.query,)
        sqlsubj="SELECT * FROM gene WHERE assembly = %s"
        subjectassembly=(self.subject,)

        cur.execute(sqlquery,queryassembly)
        rowsquery = cur.fetchall()
        #print("ROWSQUERY =",rowsquery)

        cur.execute(sqlsubj,subjectassembly)
        rowsubj=cur.fetchall()
        #print("ROWSSUBJECT = ",rowsubj)


        print("la longueur de rowsquery != 0 ????",len(rowsquery)!=0)
        print("la longueur de rowsubject != 0 ????",len(rowsubj)!=0)

        # Check if any rows were returned
        if len(rowsquery)!=0 and len(rowsubj)!=0:
            print('Value query et subject exists in table gene.')

            sqlcheckblast="SELECT * FROM blast WHERE assembly_query=%s AND assembly_subject=%s"

            cur.execute(sqlcheckblast,(queryassembly,subjectassembly))

            rowsblast = cur.fetchall()
            print("rowsblast",rowsblast)


            sqlgene="SELECT gene.nomgene,gene.ranggene,gene.lgseq FROM gene WHERE gene.assembly = %s"
            

            cur.execute(sqlgene,queryassembly)
            query_gene=cur.fetchall()

            cur.execute(sqlgene,subjectassembly)
            subject_gene=cur.fetchall()


                
            for e in query_gene:
                query_dico[e[0]]=(e[1],e[2])

                
            for e in subject_gene:
                subject_dico[e[0]]=(e[1],e[2])


            # Check if any rows were returned
            if rowsblast:
                print("The values exist in the table blast.")

                

                sql="SELECT query,subject,evalue FROM blast WHERE assembly_query=%s and assembly_subject=%s"
                cur.execute(sql,(queryassembly,subjectassembly))
                rowsblastdico=cur.fetchall()

                # Print the results
                for row in rowsblastdico:
                    #print(row)
                    dico_blast[(row[0],row[1])]=row[2]


                
                
                for key,val in dico_blast.items():
                    nom_query_gene,nom_subject_gene=key
                    
                    pos_query_gene,lg_query_gene=query_dico[nom_query_gene]
                    pos_subject_gene,lg_subject_gene=subject_dico[nom_subject_gene]
                        
                    dico_blast_pos_ev[(pos_query_gene,pos_subject_gene)]=float(val)
                

            else:
                print("The values do not exist in the table blast .")

                #____________________________________________________________________________________________
                # pour récupérer le nom du fichier pour query qui sert à lancer le blast 

                sqlqweb="SELECT organisme.lienweb FROM organisme WHERE assembly = %s"
                cur.execute(sqlqweb,queryassembly)
                res=cur.fetchall()
                urlq=res[0][0]

                    
                partsq = urlq.split("/")
                    
                last_partq = partsq[-1]  # Get the last part of the URL

                query_file=last_partq+extentionoutput # permet d'obtenir le nom du fichier query pour le blast
                print("query_file",query_file)

                #-----------------------------------------------------------------------------------------------

                # pour récupérer le nom du fichier pour subject qui sert à lancer le blast 

                sqlsweb="SELECT organisme.lienweb FROM organisme WHERE assembly = %s"
                cur.execute(sqlsweb,subjectassembly)
                res2=cur.fetchall()
                urls=res2[0][0]

                    
                partssb = urls.split("/")
                    
                last_partsb = partssb[-1]  # Get the last part of the URL
                subject_file=last_partsb+extentionoutput # permet d'obtenir le nom du fichier pour le blast
                print("subject_file",subject_file)

                #_________________________________________________________________________________________________


                #______________________________________________________________________________________________________________________________
                # LANCER LA COMMANDE BLAST ET ENTRER LES DONNEES DANS LA TABLE BLAST 
                    
                evalue = "1e-10"
                output_file ="QUERY-"+query_file.strip(".faa")+"__DB-"+subject_file.strip(".faa")+".out"

                print("outputfile",output_file)

                outfmt = "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore"

                command = ["blastp", "-query", query_file, "-subject", subject_file, "-evalue", evalue, "-out", output_file, "-outfmt", outfmt]

                subprocess.run(command, capture_output=True, text=True)

            #if result.returncode == 0:
            #    print("blastp completed successfully!")
            #else:
            #   print("blastp failed with return code", result.returncode)

                RES=fct.lire_blast_remplir(output_file)
                print("RES = ",RES)

                #---------------------------------------------------------------------------------------------------------------

                # entrer les données dans la table blastinterm
                for e in RES:
                    print(" e  = ",e)


                    cur.execute("INSERT INTO BLASTINTERM (qseqid,sseqid,pident,length,mismatch,gapopen,qstart,qend,sstart,send,evalue,bitscore) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(e[0],e[1],e[2],e[3],e[4],e[5],e[6],e[7],e[8],e[9],e[10],e[11]))

                    conn.commit()

                #entrer les données dans la table BLAST 

                sqlblasttable=""" INSERT INTO blast (query, subject, evalue, coverquery, coversubj, pourcid, startquery, endquery, startsubj, endsubj, assembly_query, assembly_subject)
                SELECT g1.nomgene, g2.nomgene, b.evalue, 
                CAST(((b.qend-b.qstart)*100) AS DECIMAL(10,2)) /g1.lgseq AS coverquery, 
                CAST(((b.send-b.sstart)*100) AS DECIMAL(10,2))/g2.lgseq AS coversubj,
                b.pident, b.qstart, b.qend, b.sstart, b.send, g1.assembly, g2.assembly
                FROM blastinterm b
                INNER JOIN gene g1 ON b.qseqid = g1.nomgene AND g1.assembly = %s
                INNER JOIN gene g2 ON b.sseqid = g2.nomgene AND g2.assembly = %s;
                """

                cur.execute(sqlblasttable,(queryassembly,subjectassembly))

                conn.commit()

                #_____________________________________________________________________________________________________________________________________________


                


                



        if len(rowsquery)==0 and len(rowsubj)!=0:
            print('Value query does not exist in table.')

            #_____________________________________________________________

            # QUERY N'EST PAS DANS GENE ALORS IL FAUT TELECHARGER LE FICHIER 
            

            sqlqweb="SELECT organisme.lienweb FROM organisme WHERE assembly = %s"
            cur.execute(sqlqweb,queryassembly)
            res=cur.fetchall()
            urlq=res[0][0]

                
            partsq = urlq.split("/")
                
            last_partq = partsq[-1]  # Get the last part of the URL
                
            extention="_translated_cds.faa.gz"
            extentionoutput="_translated_cds.faa"
            downloadlinkq=urlq+"/"+last_partq+extention

            query_file=last_partq+extentionoutput
            remote_dir = "/home/anastasia/proj"
            deziplinkq=last_partq+extention

            #cmd = ["wget", "-P", remote_dir, downloadlinkq]
            cmd = ["wget", downloadlinkq]
            subprocess.run(cmd)
            subprocess.run(['gunzip', '-k', '-f', deziplinkq])  # ON DEZIPE LE FICHIER 
            #subprocess.run(['unzip', downloadlinkq])
            #------------------------------------------------------------
            # METTRE LE FICHIER QUERY DANS LA TABLE GENE

            dicofinal_query=fct.lire_fichier(query_file)
            
            sqlgenequerytable="SELECT nomorg,assembly FROM organisme WHERE assembly = %s"

            cur.execute(sqlgenequerytable,queryassembly)
                
            query_res = cur.fetchall()


            for key,val in dicofinal_query.items():
                pos,lg=val
                    
                        
                cur.execute("INSERT INTO GENE (nomgene,assembly,nomorg,ranggene,lgseq) VALUES (%s,%s,%s,%s,%s)",(key,query_res[0][1],query_res[0][0],pos,lg))
            


            #-----------------------------------------------------------

            # RECUPERER LE NOM DU FICHIER POUR SUBJECT POUR LE BLAST  GRACE A L'URL
            sqlsweb="SELECT organisme.lienweb FROM organisme WHERE assembly = %s"
            cur.execute(sqlsweb,subjectassembly)
            res2=cur.fetchall()
            urls=res2[0][0]

                
            partssb = urls.split("/")
                
            last_partsb = partssb[-1]  # Get the last part of the URL
            subject_file=last_partsb+extentionoutput #NOM DU FICHIER FASTA



            #______________________________________________________________________________________________________________________________
            # LANCER LA COMMANDE BLAST ET ENTRER LES DONNEES DANS LA TABLE BLAST 
                
            evalue = "1e-10"
            output_file ="QUERY-"+query_file.strip(".faa")+"__DB-"+subject_file.strip(".faa")+".out"

            outfmt = "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore"

            command = ["blastp", "-query", query_file, "-subject", subject_file, "-evalue", evalue, "-out", output_file, "-outfmt", outfmt]

            subprocess.run(command, capture_output=True, text=True)

            #if result.returncode == 0:
            #    print("blastp completed successfully!")
            #else:
            #   print("blastp failed with return code", result.returncode)

            RES=fct.lire_blast_remplir(output_file)

            #---------------------------------------------------------------------------------------------------------------

            # entrer les données dans la table blastinterm
            for e in RES:


                cur.execute("INSERT INTO BLASTINTERM (qseqid,sseqid,pident,length,mismatch,gapopen,qstart,qend,sstart,send,evalue,bitscore) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(e[0],e[1],e[2],e[3],e[4],e[5],e[6],e[7],e[8],e[9],e[10],e[11]))

            conn.commit()

            #entrer les données dans la table BLAST 

            sqlblasttable=""" INSERT INTO blast (query, subject, evalue, coverquery, coversubj, pourcid, startquery, endquery, startsubj, endsubj, assembly_query, assembly_subject)
            SELECT g1.nomgene, g2.nomgene, b.evalue, 
            CAST(((b.qend-b.qstart)*100) AS DECIMAL(10,2)) /g1.lgseq AS coverquery, 
            CAST(((b.send-b.sstart)*100) AS DECIMAL(10,2))/g2.lgseq AS coversubj,
            b.pident, b.qstart, b.qend, b.sstart, b.send, g1.assembly, g2.assembly
            FROM blastinterm b
            INNER JOIN gene g1 ON b.qseqid = g1.nomgene AND g1.assembly = %s
            INNER JOIN gene g2 ON b.sseqid = g2.nomgene AND g2.assembly = %s;
            """

            cur.execute(sqlblasttable,(queryassembly,subjectassembly))

            conn.commit()

            #_____________________________________________________________________________________________________________________________________________


                
                
        if len(rowsquery)!=0 and len(rowsubj)==0:

            #________________________________________________________________________________________________
            
            #SUBJECT N EST PAS DANS GENE IL FAUT ALLER TELECHARGER LE FICHIER 

            sqlsweb="SELECT organisme.lienweb FROM organisme WHERE assembly = %s"
            cur.execute(sqlsweb,subjectassembly)
            res2=cur.fetchall()
            urls=res2[0][0]

                
            partssb = urls.split("/")
                
            last_partsb = partssb[-1]  # Get the last part of the URL
            extention="_translated_cds.faa.gz"
            extentionoutput="_translated_cds.faa"
            subject_file=last_partsb+extentionoutput
            

            downloadlinksb=urls+"/"+last_partsb+extention
            remote_dir = "/home/anastasia/proj"
            deziplinksb=last_partsb+extention
            #cmd = ["wget", "-P", remote_dir, downloadlinksb]
            cmd = ["wget", downloadlinksb]
            subprocess.run(cmd)
            subprocess.run(['gunzip', '-k', '-f', deziplinksb])
            #subprocess.run(['unzip', downloadlinksb])

            #----------------------------------------------------------------------------------------
            # RENTRER DONNEES SUBJECT DANS TABLE GENE

            dicofinal_subject=fct.lire_fichier(subject_file)
            sql="SELECT nomorg,assembly FROM organisme WHERE assembly = %s"


            cur.execute(sql,subjectassembly)
            
            subject_res = cur.fetchall()


            for key,val in dicofinal_subject.items():
                pos,lg=val
                    
                        
                cur.execute("INSERT INTO GENE (nomgene,assembly,nomorg,ranggene,lgseq) VALUES (%s,%s,%s,%s,%s)",(key,subject_res[0][1],subject_res[0][0],pos,lg))

            conn.commit()





            #__________________________________________________________________
            # RECUPERER NOM FICHIER QUERY POUR LANCER BLAST D'APRES LIEN WEB 

            sqlqweb="SELECT organisme.lienweb FROM organisme WHERE assembly = %s"
            cur.execute(sqlqweb,queryassembly)
            res=cur.fetchall()
            urlq=res[0][0]

                
            partsq = urlq.split("/")
                
            last_partq = partsq[-1]  # Get the last part of the URL

            query_file=last_partq+extentionoutput


            #______________________________________________________________________________________________________________________________
            # LANCER LA COMMANDE BLAST ET ENTRER LES DONNEES DANS LA TABLE BLAST 
                
            evalue = "1e-10"
            output_file ="QUERY-"+query_file.strip(".faa")+"__DB-"+subject_file.strip(".faa")+".out"

            outfmt = "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore"

            command = ["blastp", "-query", query_file, "-subject", subject_file, "-evalue", evalue, "-out", output_file, "-outfmt", outfmt]

            subprocess.run(command, capture_output=True, text=True)

            #if result.returncode == 0:
            #    print("blastp completed successfully!")
            #else:
            #   print("blastp failed with return code", result.returncode)
            RES=fct.lire_blast_remplir(output_file)

            #---------------------------------------------------------------------------------------------------------------

            # entrer les données dans la table blastinterm
            for e in RES:


                cur.execute("INSERT INTO BLASTINTERM (qseqid,sseqid,pident,length,mismatch,gapopen,qstart,qend,sstart,send,evalue,bitscore) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(e[0],e[1],e[2],e[3],e[4],e[5],e[6],e[7],e[8],e[9],e[10],e[11]))

            conn.commit()

            #entrer les données dans la table BLAST 

            sqlblasttable=""" INSERT INTO blast (query, subject, evalue, coverquery, coversubj, pourcid, startquery, endquery, startsubj, endsubj, assembly_query, assembly_subject)
            SELECT g1.nomgene, g2.nomgene, b.evalue, 
            CAST(((b.qend-b.qstart)*100) AS DECIMAL(10,2)) /g1.lgseq AS coverquery, 
            CAST(((b.send-b.sstart)*100) AS DECIMAL(10,2))/g2.lgseq AS coversubj,
            b.pident, b.qstart, b.qend, b.sstart, b.send, g1.assembly, g2.assembly
            FROM blastinterm b
            INNER JOIN gene g1 ON b.qseqid = g1.nomgene AND g1.assembly = %s
            INNER JOIN gene g2 ON b.sseqid = g2.nomgene AND g2.assembly = %s;
            """

            cur.execute(sqlblasttable,(queryassembly,subjectassembly))

            conn.commit()

            #_____________________________________________________________________________________________________________________________________________





        if  len(rowsquery)==0 and len(rowsubj)==0:

            #_____________________________________________________________

            # QUERY N'EST PAS DANS GENE ALORS IL FAUT TELECHARGER LE FICHIER 
            

            sqlqweb="SELECT organisme.lienweb FROM organisme WHERE assembly = %s"
            cur.execute(sqlqweb,queryassembly)
            res=cur.fetchall()
            urlq=res[0][0]

                
            partsq = urlq.split("/")
                
            last_partq = partsq[-1]  # Get the last part of the URL
                
            extention="_translated_cds.faa.gz"
            extentionoutput="_translated_cds.faa"
            downloadlinkq=urlq+"/"+last_partq+extention

            query_file=last_partq+extentionoutput
            remote_dir = "/home/anastasia/proj"
            deziplinkq=last_partq+extention

            #cmd = ["wget", "-P", remote_dir, downloadlinkq]
            cmd = ["wget", downloadlinkq]
            subprocess.run(cmd)
            subprocess.run(['gunzip', '-k', '-f', deziplinkq])  # ON DEZIPE LE FICHIER 
            #subprocess.run(['unzip', downloadlinkq])
            #------------------------------------------------------------
            # METTRE LE FICHIER QUERY DANS LA TABLE GENE

            dicofinal_query=fct.lire_fichier(query_file)
            
            sqlgenequerytable="SELECT nomorg,assembly FROM organisme WHERE assembly = %s"

            cur.execute(sqlgenequerytable,queryassembly)
                
            query_res = cur.fetchall()


            for key,val in dicofinal_query.items():
                pos,lg=val
                    
                        
                cur.execute("INSERT INTO GENE (nomgene,assembly,nomorg,ranggene,lgseq) VALUES (%s,%s,%s,%s,%s)",(key,query_res[0][1],query_res[0][0],pos,lg))
            

            #________________________________________________________________________________________________
            
            #SUBJECT N EST PAS DANS GENE IL FAUT ALLER TELECHARGER LE FICHIER 

            sqlsweb="SELECT organisme.lienweb FROM organisme WHERE assembly = %s"
            cur.execute(sqlsweb,subjectassembly)
            res2=cur.fetchall()
            urls=res2[0][0]

                
            partssb = urls.split("/")
                
            last_partsb = partssb[-1]  # Get the last part of the URL
            extention="_translated_cds.faa.gz"
            extentionoutput="_translated_cds.faa"
            subject_file=last_partsb+extentionoutput
            

            downloadlinksb=urls+"/"+last_partsb+extention
            remote_dir = "/home/anastasia/proj"
            deziplinksb=last_partsb+extention

            #cmd = ["wget", "-P", remote_dir, downloadlinksb]
            cmd = ["wget", downloadlinkq]
            subprocess.run(cmd)
            subprocess.run(['gunzip', '-k', '-f', deziplinksb])
            #subprocess.run(['unzip', downloadlinksb])
            #----------------------------------------------------------------------------------------
            # RENTRER DONNEES SUBJECT DANS TABLE GENE

            dicofinal_subject=fct.lire_fichier(subject_file)
            sql="SELECT nomorg,assembly FROM organisme WHERE assembly = %s"


            cur.execute(sql,subjectassembly)
            
            subject_res = cur.fetchall()


            for key,val in dicofinal_subject.items():
                pos,lg=val
                    
                        
                cur.execute("INSERT INTO GENE (nomgene,assembly,nomorg,ranggene,lgseq) VALUES (%s,%s,%s,%s,%s)",(key,subject_res[0][1],subject_res[0][0],pos,lg))

            conn.commit()


            #______________________________________________________________________________________________________________________________
            # LANCER LA COMMANDE BLAST ET ENTRER LES DONNEES DANS LA TABLE BLAST 
                
            evalue = "1e-10"
            output_file ="QUERY-"+query_file.strip(".faa")+"__DB-"+subject_file.strip(".faa")+".out"

            outfmt = "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore"

            command = ["blastp", "-query", query_file, "-subject", subject_file, "-evalue", evalue, "-out", output_file, "-outfmt", outfmt]

            subprocess.run(command, capture_output=True, text=True)

            #if result.returncode == 0:
            #    print("blastp completed successfully!")
            #else:
            #   print("blastp failed with return code", result.returncode)

            RES=fct.lire_blast_remplir(output_file)

            #---------------------------------------------------------------------------------------------------------------

            # entrer les données dans la table blastinterm
            for e in RES:


                cur.execute("INSERT INTO BLASTINTERM (qseqid,sseqid,pident,length,mismatch,gapopen,qstart,qend,sstart,send,evalue,bitscore) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(e[0],e[1],e[2],e[3],e[4],e[5],e[6],e[7],e[8],e[9],e[10],e[11]))

            conn.commit()

            #entrer les données dans la table BLAST 

            sqlblasttable=""" INSERT INTO blast (query, subject, evalue, coverquery, coversubj, pourcid, startquery, endquery, startsubj, endsubj, assembly_query, assembly_subject)
            SELECT g1.nomgene, g2.nomgene, b.evalue, 
            CAST(((b.qend-b.qstart)*100) AS DECIMAL(10,2)) /g1.lgseq AS coverquery, 
            CAST(((b.send-b.sstart)*100) AS DECIMAL(10,2))/g2.lgseq AS coversubj,
            b.pident, b.qstart, b.qend, b.sstart, b.send, g1.assembly, g2.assembly
            FROM blastinterm b
            INNER JOIN gene g1 ON b.qseqid = g1.nomgene AND g1.assembly = %s
            INNER JOIN gene g2 ON b.sseqid = g2.nomgene AND g2.assembly = %s;
            """

            cur.execute(sqlblasttable,(queryassembly,subjectassembly))

            conn.commit()

            #_____________________________________________________________________________________________________________________________________________





            # Get the user inputs
        #query_assembly = qcb.get()
        #subject_assembly =scb.get()

        sql_blastinterm_dico="SELECT * FROM blast WHERE assembly_query=%s and assembly_subject=%s"
        cur.execute(sql_blastinterm_dico, (queryassembly, subjectassembly))
        rowsinterm = cur.fetchall()
        print("ROWSINTERM != NONE ? ",rowsinterm!=None)

        print("rowsinterm lg liste !=0 ???",len(rowsinterm)!=0)
            
        sql_blast_dico="SELECT query,subject,evalue FROM blast WHERE assembly_query=%s and assembly_subject=%s"

            # Execute the query
            #with conn.cursor() as cur:
        cur.execute(sql_blast_dico, (queryassembly, subjectassembly))
        rows = cur.fetchall()

        print("rows != None ???",rows!=None)

        print("rows test si dans blast ",rows)

        print("rows test  2 avec lg liste est =/=0 si dans blast ",len(rows)!=0)


        dico_blast={}

            # Print the results
        for row in rows:
                #print(row)
            dico_blast[(row[0],row[1])]=row[2]

        print(" DICO BLAST \n")
        print(dico_blast)




        sqlgene="SELECT gene.nomgene,gene.ranggene,gene.lgseq FROM gene WHERE gene.assembly = %s"
        #query_assembly2 = 'GCA_000014865.1'
        #subject_assembly2 ='GCA_000009985.1'

        cur.execute(sqlgene,queryassembly)
        query_gene=cur.fetchall()

        cur.execute(sqlgene,subjectassembly)
        subject_gene=cur.fetchall()


        #query_dico={}
        for e in query_gene:
            query_dico[e[0]]=(e[1],e[2])

        #print("QUERY DICO",query_dico)

        #subject_dico={}
        for e in subject_gene:
            subject_dico[e[0]]=(e[1],e[2])

        #print("SUBJECT_dico",subject_dico)
        #dico_blast_pos_ev={}
        for key,val in dico_blast.items():
            nom_query_gene,nom_subject_gene=key
            
            pos_query_gene,lg_query_gene=query_dico[nom_query_gene]
            pos_subject_gene,lg_subject_gene=subject_dico[nom_subject_gene]
                
            dico_blast_pos_ev[(pos_query_gene,pos_subject_gene)]=float(val)

        print("dico_blast_pos_ev= ",dico_blast_pos_ev )
            
            #listes positions query et subject

        x_query_list=[]
        y_subject_list=[]
        for key,val in dico_blast_pos_ev.items():
            posq,possbj=key
            x_query_list.append(posq)
            y_subject_list.append(possbj)

        mat=np.zeros((max(x_query_list)+1,max(y_subject_list)+1))
            #x_query_list et y_query_list on la même taille 
        for i in range(len(x_query_list)):
            mat[x_query_list[i]][y_subject_list[i]]=1
            #return mat


        all_gene_list_query=[]
        all_gene_list_subject=[]
        res_query_x=[]
        res_subject_y=[]
         

            # num_genes1 = len(gene_list1)
            # num_genes2 = len(gene_list2)
        num_genes_query = max(x_query_list)
        num_genes_subject = max(y_subject_list)

        for a in range(num_genes_query):
            all_gene_list_query.append(a)
        for b in range(num_genes_subject):
            all_gene_list_subject.append(b)

            
        similarity_matrix = np.zeros((num_genes_query, num_genes_subject))

        for i in range(0, num_genes_query - self.window_size + 1, self.step_size):
            for j in range(0, num_genes_subject - self.window_size + 1, self.step_size):
                  
                window_genes1 = all_gene_list_query[i:i+self.window_size]
                window_genes2 = all_gene_list_subject[j:j+self.window_size]
                    
                    
                similar_count = 0
                for k in range(self.window_size):
                        
                    for l in range(self.window_size):
                            
                        if (window_genes1[k], window_genes2[l]) in dico_blast_pos_ev:
                               
                            if dico_blast_pos_ev[(window_genes1[k], window_genes2[l])] <self.T:
                                similar_count+=1

                if similar_count>=self.S:
                        

                    similarity_matrix[i+self.window_size//2, j+self.window_size//2]=1
                    res_query_x.append(i+self.window_size//2)
                    res_subject_y.append(j+self.window_size//2)

            

        plt.scatter(res_query_x, res_subject_y,s=0.01,c='black')
        plt.xlabel("genes QUERY")
        plt.ylabel("genes SUBJECT")
        plt.title("Dotplot with plt.scatter() of QUERY : "+self.query+" and SUBJECT : "+self.subject)
        plt.show()


            
    def save_graph(self):
        
        file_path = fd.asksaveasfilename(defaultextension='.png')

        
        plt.savefig(file_path)

    
 
    
       

    conn.close()  

        

       

test=AAZ_GUI_APP()