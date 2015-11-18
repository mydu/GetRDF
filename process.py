import os
import zipfile
import StringIO
import urllib, json
from flask import Flask, request, render_template, Response, jsonify
from turtle import procTable,prefix_handler
from turtleAll import csvtoturtle
from werkzeug import secure_filename

# UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/')
def my_form():
	return render_template("index.html",result='')

@app.route("/process",methods=["GET","POST"])
def process_file():
	if request.method=="POST":
		if request.json:
			data = json.loads(request.data)
			# filetitle=data["filename"]
			header=data["header"]
			# print data["encode"]
			encode=data["encode"]
			table=data["tableau"]
			datatype=data["datatype"]
			onto=data["onto"]
			# start=int(data["start"])
			# end=int(data["end"])
			entity=str(data["entity"]).strip()
			subj_prefix=str(data["subjPrefix"]).strip()
			pred_prefix=str(data["predPrefix"]).strip()
			namespace=str(data["namespace"])
			# table=table[start-1:end-1]
			result_text=procTable(header,datatype,onto,table,entity,subj_prefix,pred_prefix,encode)
			result_text=prefix_handler(result_text,namespace)
			return result_text
		elif request.form["download"]=="currentFile":
			# filetitle=request.form["fileSelect"].split(".",1)[0]
			turtle=request.form["outputRDF"]
			return Response(turtle,mimetype="text/plain",headers={"Content-Disposition":"attachment;filename=download.ttl"})
		
		elif request.form["download"]=="allFile":
			uploaded_files = request.files.getlist("file[]")
			delimiter=request.form["delimiterSelect"]
			start = request.form["start"]
			end = request.form["end"]
			# entity=request.form["entity"].strip()
			# subj_prefix = request.form["subjPrefix"].strip()
			# pred_prefix= request.form["predPrefix"].strip()

			datatype= request.form.getlist("datatype")
			# namespace= request.form["namespace"]
			filenames = []
			# result_text=namespace+"\n"
			namespace=""
			result_text=""
			for file in uploaded_files:
				if file and allowed_file(file.filename):
					file_contents =file.stream.read()
					fileitem= secure_filename(file.filename)
					entity="http://localhost/"+fileitem+"/data#"+fileitem+""
					subj_prefix="http://localhost/"+fileitem+"/data/"
					pred_prefix="http://localhost/"+fileitem+"/data#"
					# namespace=namespace+""subj_prefix+"\n"+pred_prefix+"\n"
					ttl_text=csvtoturtle(str(file_contents),str(delimiter),int(start),int(end),str(subj_prefix),str(entity),datatype,str(pred_prefix))
					# if len(namespace)>0:
						#ttl_text=prefix_handler(ttl_text,str(namespace))
					result_text=result_text+ttl_text+"\n"
					# # fileitem= str(file.filename)
					# # filenames.append(str(file.filename))
					# file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileitem))
					# filenames.append(fileitem)
			# zipped_file = StringIO.StringIO()
			# with zipfile.ZipFile(zipped_file, 'w') as zip:
			# 	zip.writestr("test.ttl",result_text)
			# zipped_file.seek(0)
			return Response(result_text,mimetype="text/plain",headers={"Content-Disposition":"attachment;filename=Turtlefile.ttl"})
		
		elif request.form["download"]=="multiFile":
			uploaded_files = request.files.getlist("file[]")
			delimiter=request.form["delimiterSelect"]
			encode=request.form["unicode"]
			start = request.form["start"]
			end = request.form["end"]
			# entity=request.form["entity"].strip()
			# subj_prefix = request.form["subjPrefix"].strip()
			# pred_prefix= request.form["predPrefix"].strip()

			datatype= request.form.getlist("datatype")
			# print datatype
			ontotype= request.form.getlist("onto")
			queryURL = request.form["queryURL"]
			# url="http://localhost:9091/sparql?query=PREFIX%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%20PREFIX%20owl%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%20PREFIX%20g%3A%20%3Chttp%3A%2F%2Flocalhost%3A9091%2Fproject%2Fvcard%2Fsource%2Fvcard-owl-1%3E%20SELECT%20*%20WHERE%20%7B%20GRAPH%20g%3A%20%7B%20%7B%20%3Fs%20a%20owl%3ADatatypeProperty%20.%7D%20optional%20%7B%20%3Fs%20rdfs%3Alabel%20%3Flabel%20.%20%7D%20optional%20%7B%20%3Fs%20rdfs%3Acomment%20%3Fcomment%20.%20%7D%20%7D%7D&format=json"
			response = urllib.urlopen(queryURL)
			owlJSON = json.loads(response.read())
			owlDict={"1":""}
			for i in range(len(owlJSON["results"]["bindings"])):
				owlDict[str(i+2)]=owlJSON["results"]["bindings"][i]["s"]["value"]
			print owlDict
			# namespace= request.form["namespace"]
			filenames = []
			# result_text=namespace+"\n"
			namespace=""
			# result_text=""
			zipped_file = StringIO.StringIO()
			with zipfile.ZipFile(zipped_file, 'w') as zip:
				for file in uploaded_files:
					if file and allowed_file(file.filename):
						file_contents =file.stream.read()
						fileitem= secure_filename(file.filename)
						entity="http://localhost/"+fileitem+"/data#"+fileitem+""
						subj_prefix="http://localhost/"+fileitem+"/data/"
						pred_prefix="http://localhost/"+fileitem+"/data#"
						# namespace=namespace+""subj_prefix+"\n"+pred_prefix+"\n"
						ttl_text=csvtoturtle(str(file_contents),str(delimiter),int(start),int(end),str(subj_prefix),str(entity),datatype,ontotype,str(pred_prefix),"utf-8",owlDict)
						# if len(namespace)>0:
							#ttl_text=prefix_handler(ttl_text,str(namespace))
						# result_text=result_text+ttl_text+"\n"
						itemname=fileitem.split(".",1)[0]
						zip.writestr(itemname+".ttl",ttl_text)
						# # fileitem= str(file.filename)
						# # filenames.append(str(file.filename))
						# file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileitem))
						# filenames.append(fileitem)
			zipped_file.seek(0)
			# return "testJSON!"
			return Response(zipped_file,mimetype="application/zip",headers={"Content-Disposition":"attachment;filename=Turtlefile.zip"})
		else:
			return "invalid!"
	# return Response(result,mimetype="text/plain",headers={"Content-Disposition":"attachment;filename=test.txt"})

# @app.route("/processAll",methods=["GET","POST"])
# def process_all():
# 	if request.method=="POST":
# 		if request.json:
# 			uploaded_files = json.loads(request.data)
# 			filenames = []
# 			for file in uploaded_files:
# 				print file
# 				# if file and allowed_file(file.filename):
# 				# 	fileitem= secure_filename(file.filename)
# 				# 	file.save(os.path.join(app.config['UPLOAD_FOLDER'], fileitem))
# 				# 	filenames.append(fileitem)
# 			return "process all"
# 		else:
# 			return "invalid!"
# @app.route('/download')
# def download_file():
# 	turtle=request.form["outputRDF"]
# 	return Response(turtle,mimetype="text/plain",headers={"Content-Disposition":"attachment;filename=test.txt"})

if __name__ == '__main__':
	app.run(debug=True)