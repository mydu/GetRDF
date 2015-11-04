import StringIO
import csv

SUBJPREFIX="SUBJPREFIX"
CLASS="csv"


def csvtolist(f,sep):
	lines=[]
	reader = csv.reader(f.split('\n'), delimiter=sep)
	for line in reader:
		lines.append(line)
	return lines

def listcombination(lines,subj_prefix,entity,data_type,pred_prefix):
	lines_new=lines

	for i in range(1,len(lines_new)):
		
		lines_new[i]=['a <'+entity+'>']+lines_new[i]
		lines_new[i]=['<'+subj_prefix+'/'+str(i)+'>']+lines_new[i]
		for j in range(2,len(lines_new[i])-1):
			count=0
			if lines_new[i][j]!='':
				lines_new[i][j]='<'+str(pred_prefix[j-2])+lines[0][j-2]+'> "'+lines_new[i][j]+str(data_type[j-2])+'" ;'
			else:
				count+=1

		if lines_new[i][-1]!='':
			lines_new[i][-1]='<'+str(pred_prefix[-(count+1)])+lines[0][-1]+'> "'+lines_new[i][-1]+'"'		
	return lines_new			

def listextraction(lines,start=None,end=None):
	lines_new=lines[start:end+1]
	
	return lines_new

# b=listextraction(a,0,4)
def csvtoturtle(filename,sep,start=1,end=None,subj_prefix=SUBJPREFIX,entity=CLASS,data_type=[],pred_prefix=[]):

#a is a list contains all of the original info of the csv file
	a=csvtolist(filename,sep)
	if end is None:
		end=len(a)	
#the function listcombination is the function that adds prefix to the original info of csv
	b=listcombination(a,subj_prefix,entity,data_type,pred_prefix)
#c is extraction	
	c=listextraction(b,start,end)
	result=[]

#delete all the empty element in c
	for i in range(len(c)):
		c[i]=filter(None,c[i])
	
#write file 
	for i in c:
		result.append(i[0]+'\n')
		for j in i[1:len(i)-1]:
			result.append('\t'+j+'\n')
		result.append('\t'+i[-1]+' .'+'\n')	
	return " ".join(result)
	# file.close()
	

# csvtoturtle('taxi.csv',';')
