import re

def headerType(header,datatype):
	headertype=[]
	headerId=[i['typeId'] for i in header]
	for i in header:
		for j in datatype:
			if i['typeId']==j['id']:
				i["type"]=j["name"]
				i["typeValue"]=j["value"]
	return header

def procTable(header,datatype,table,entity,subj_prefix,pred_prefix):
	header=headerType(header,datatype)
	lines_new=table
	result=[]
	for i in range(len(table)):
		lines_new[i]=['a <'+entity+'>']+lines_new[i]
		lines_new[i]=['<'+subj_prefix+str(i+1)+'>']+lines_new[i]
		for j in range(2,len(lines_new[i])-1):
			count=0
			if lines_new[i][j]!='':
				lines_new[i][j]='<'+pred_prefix+str(header[j-2]["name"])+'> "'+lines_new[i][j]+'"'+str(header[j-2]["typeValue"])+' ;'
			else:
				count+=1

		if lines_new[i][-1]!='':
		   lines_new[i][-1]='<'+pred_prefix+str(header[-1]["name"])+'> "'+lines_new[i][-1]+'"'+str(header[-1]["typeValue"])+''	
    
    #delete all the empty element in lines_new
	for i in range(len(lines_new)):
		lines_new[i]=filter(None,lines_new[i])

	#prcoess list to a large string
	for i in lines_new:
		result.append(i[0]+'\n')
		for j in i[1:len(i)-1]:
			result.append('\t'+j+'\n')
		result.append('\t'+i[-1]+' .'+'\n')	
	return " ".join(result)		

def prefix_handler(text,namespace_text):
	if re.match(r'@prefix[^:].+<.+>',namespace_text) is not None:
		namespace=namespace_text.replace('@prefix','')
		prefixlis=namespace.split("\n")
		prefixdic={}
		for prefix in prefixlis:
			if prefix.find(':')!=1:
				prefixdic[prefix.split(":",1)[0].strip()+":"]=prefix.split(":",1)[1].strip()
		# print prefixdic
		# re.sub(r'%s'% value,re.match(r'%s'% value,text).group(1),"text")
		# re.sub("Date\((.+?)\)",r"\1",'{"date":Date(12455),"out_date":Date(45677)}')
		for key in prefixdic:
			# text=text.replace(prefixdic[key][:-1],key)
			pattern="\<"+prefixdic[key][1:-1]+"(.+?)\>"
			text=re.sub(pattern,key+r"\1",text)
	text=namespace_text+'\n'+text
	return text	