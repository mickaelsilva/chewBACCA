#!/usr/bin/python
import sys
import csv
import numpy as np
from numpy import array
import argparse
import collections
from collections import OrderedDict

def presAbs (d3,listgenomesRemove):	

	d2c=np.copy(d3)
	

	geneslist= d2c[:1,:]
	genomeslist= d2c[:,:1]
	genomeslist=(genomeslist.tolist())
	
	geneslistaux=[]
	for genome in genomeslist:
		geneslistaux.append(genome[0])
	
	#remove genomes
	listidstoremove=[]
	print "removing the following genomes..."
	for genome in geneslistaux:
		if genome in listgenomesRemove:
			print genome
			rowid=geneslistaux.index(genome)
			listidstoremove.append(rowid)
			#geneslistaux.pop(rowid)
	
	listidstoremove=sorted(listidstoremove, reverse=True)	
	for idtoremove in listidstoremove:
		d3=np.delete(d3, idtoremove, 0)
		d2c=np.delete(d2c, idtoremove, 0)

	print "all genomes removed"
	
	print "building the presence and abscence matrix..."
	row=1
	row2Del=[]
	while row<d2c.shape[0]:
		column=1
		while column<d2c.shape[1]:
			try:

				aux=int(d2c[row,column])
				if aux>0:
					d2c[row,column]=1
				else :
					d2c[row,column]=0
					row2Del.append(int(column))
			except:
				try:
					aux=str((d2c[row,column])).replace ("INF-","")
					aux=int(aux)
					d2c[row,column]=1
				except Exception as e:
					d2c[row,column]=0
					row2Del.append(int(column))
				
			column+=1
		row+=1
	
	print "presence and abscence matrix built"

	d2d=d2c.tolist()
	
	with open ("presence.txt","wb") as f:
		
		writer = csv.writer(f,delimiter='	')
		writer.writerows(d2d)
	
	row2Del=set(row2Del)
	row2Del=list(row2Del)	
	
	return d2c,d3,row2Del

def clean (inputfile,outputfile,totaldeletedgenes,rangeFloat,toremovegenes,toremovegenomes):
	
	#open the raw file to be clean
	
	with open(inputfile) as f:
		reader = csv.reader(f, delimiter="\t")
		d = list(reader)
	
	originald2 = array(d)
	
	#get presence abscence matrix
	d2,originald2,del2CG=presAbs (originald2,toremovegenomes)
	
	genomeslist= d2[1:,:1]
	geneslist= (d2[:1,1:])[0]
	
	originald2=originald2.T
	d2=d2.T
	rowid=(d2.shape[0])-1
	deleted=0
	abscenceMatrix=True
	balldel=0
	cgMLST=0
	
	numbergenomes=len(genomeslist)
	pontuationmatrix=[0]*numbergenomes	
	lostgenesList=[]
	
	#clean the original matrix, using the information on the presence/abscence matrix
	print "processing the matrix"
	while rowid> 0:
		columnid=1
		genomeindex=0
		print str(rowid)+"/"+str(d2.shape[0])
		#~ print type((d2[rowid,1:])[0]
		if rowid in del2CG:
			originald2=np.delete(originald2, rowid, 0)
			d2=np.delete(d2, rowid, 0)
			totaldeletedgenes+=1
			deleted+=1
			#~ rowid-=1
			columnid=1
		
		elif geneslist[rowid-1] in toremovegenes:
				
			originald2=np.delete(originald2, rowid, 0)
			#~ d2=np.delete(d2, rowid, 0)
			totaldeletedgenes+=1
			deleted+=1
			#~ rowid-=1
			columnid=1
			#~ break
		else:
			cgMLST+=1


		rowid-=1
	
	originald2=originald2.T
	originald2=originald2.tolist()
	
	#write the output file
	
	with open(outputfile, "wb") as f:
		writer = csv.writer(f,delimiter='	')
		writer.writerows(originald2)
	
	#chewbbaca files have INF that needs to be removed
	file = open(outputfile)
	contents = file.read()
	contents = contents.replace('INF-', '')

	
	with open(outputfile, 'w') as f:
			f.write(contents)
	

	print "deleted : %s loci" % totaldeletedgenes
	print "total loci remaining : "+ str(cgMLST)


def main():

	parser = argparse.ArgumentParser(description="This program cleans an output file for phyloviz")
	parser.add_argument('-i', nargs='?', type=str, help='output to clean', required=True)
	parser.add_argument('-o', nargs='?', type=str, help='name of the clean file', required=True)
	parser.add_argument('-r', nargs='?', type=str, help='listgenes to remove', required=False)
	parser.add_argument('-g', nargs='?', type=str, help='listgenomes to remove', required=False)
	
	args = parser.parse_args()

	
	pathOutputfile = args.i
	newfile = args.o
	
	
	
	genesToRemove=[]
	genomesToRemove=[]
	
	try:
		genesToRemoveFile = (args.r)
		fp = open(genesToRemoveFile, 'r')
		
		for geneFile in fp:

			geneFile = geneFile.rstrip('\n')
			geneFile = geneFile.rstrip('\r')
			geneFile = (geneFile.split('\t'))[0]
			
			genesToRemove.append( geneFile )
	except:		
		pass
	
	try:
		genomesToRemoveFile = (args.g)
		fp = open(genomesToRemoveFile, 'r')
		
		for genomeFile in fp:

			genomeFile = genomeFile.rstrip('\n')
			genomeFile = genomeFile.rstrip('\r')
			
			genomesToRemove.append( genomeFile )
			
	except:		
		pass
		
	clean(pathOutputfile,newfile,0,0.2,genesToRemove,genomesToRemove)

	

	
	
	
	
		
if __name__ == "__main__":
	main()
