def extraireAllFastaMulti(fileName):
	Seqs=[]
	IdSeq=[]
	chevron = []
	liste_seq=[]
	lkey=[]
	tmp=[]

	with open(fileName, 'r') as f:
		lines = f.readlines()
        
        
	for i in range (len(lines)):
		if lines[i][0]=='>':
			chevron.append(i)
			if lines[i][-1] == '\n': 
				lkey.append(lines[i][1:-1])
			else: 
				lkey.append(lines[i][1:])
                    
		print(chevron)        
		for i in range(len(chevron)-1):
			pre = chevron[i]

			post = chevron[i+1]

                
			liste_seq.append(lines[(pre+1):post])

	
	for l in liste_seq:
		s=""
		for e in l:
			if e=="\n" or e=="n":
				print("on saute")
				continue
			else:
				s+=e
		tmp.append(s)

	for a in tmp:
		Seqs.append(a.replace("\n",""))
			
	
                
            

	return IdSeq, Seqs

#IdSeq,Seqs=extraireAllFastaMulti("fasta/algnMult.fasta")
IdSeq2,Seqs2=extraireAllFastaMulti("fasta/algnMult2.fasta")
#print("IdSeq\n",IdSeq,"\n\nSeqs\n", Seqs)
print("IdSeq\n",IdSeq2,"\n\nSeqs\n", Seqs2)




# A = [1,2,3,4,5,6]

# print(A[1])
# print(A[(1+1):3])
# print(A[3])




