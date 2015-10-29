import os
import zipfile
import StringIO
import json
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
			table=data["tableau"]
			datatype=data["datatype"]
			# start=int(data["start"])
			# end=int(data["end"])
			entity=str(data["entity"]).strip()
			subj_prefix=str(data["subjPrefix"]).strip()
			pred_prefix=str(data["predPrefix"]).strip()
			namespace=str(data["namespace"])
			# table=table[start-1:end-1]
			result_text=procTable(header,datatype,table,entity,subj_prefix,pred_prefix)
			result_text=namespace+"\n"+prefix_handler(result_text,namespace)
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
						ttl_text=csvtoturtle(str(file_contents),str(delimiter),int(start),int(end),str(subj_prefix),str(entity),datatype,str(pred_prefix))
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