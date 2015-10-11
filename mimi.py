import StringIO
import csv
import re

SUBJPREFIX="SUBJPREFIX"
CLASS="csv"


def csvtolist(f,sep):
	lines=[]
	reader = csv.reader(f.split('\n'), delimiter=sep)
	for line in reader:
		lines.append(line)
	return lines

def listcombination(lines,subj_prefix,entity,data_type,pred_prefix):
	print lines
	lines_new=lines

	for i in range(1,len(lines_new)):
		
		lines_new[i]=['a <'+entity+'>']+lines_new[i]
		lines_new[i]=['<'+subj_prefix+str(i)+'>']+lines_new[i]
		for j in range(2,len(lines_new[i])-1):
			count=0
			if lines_new[i][j]!='':
				lines_new[i][j]='<'+str(pred_prefix)+lines[0][j-2]+'> "'+lines_new[i][j]+'"'+str(data_type[j-2])+' ;'
			else:
				count+=1

		if lines_new[i][-1]!='':
			lines_new[i][-1]='<'+str(pred_prefix)+lines[0][-1]+'> "'+lines_new[i][-1]+'"'+str(data_type[-(count+1)])+''		
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
def prefix_handler(text,namespace_text):
	namespace=namespace_text.replace('@prefix','')
	prefixlis=namespace.split("\n")
	prefixdic={}
	for prefix in prefixlis:
		prefixdic[prefix.split(":",1)[0].strip()+":"]=prefix.split(":",1)[1].strip()
	# print prefixdic
	# re.sub(r'%s'% value,re.match(r'%s'% value,text).group(1),"text")
	# re.sub("Date\((.+?)\)",r"\1",'{"date":Date(12455),"out_date":Date(45677)}')
	for key in prefixdic:
		# text=text.replace(prefixdic[key][:-1],key)
		pattern="\<"+prefixdic[key][1:-1]+"(.+?)\>"
		print pattern
		text=re.sub(pattern,key+r"\1",text)
	text=namespace_text+'\n'+text
	return text	

# csvtoturtle('taxi.csv',';')
