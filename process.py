import os
import json
from flask import Flask, request, render_template, Response, jsonify
from turtle import procTable,prefix_handler


# UPLOAD_FOLDER = '/uploads'
# ALLOWED_EXTENSIONS = set(['csv','txt'])

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def my_form():
	return render_template("index.html",result='')

@app.route("/process",methods=["GET","POST"])
def process_file():
	if request.method=="POST":
		if request.json:
			data = json.loads(request.data)
			header=data["header"]
			table=data["tableau"]
			datatype=data["datatype"]
			start=int(data["start"])
			end=int(data["end"])
			entity=str(data["entity"]).strip()
			subj_prefix=str(data["subjPrefix"]).strip()
			pred_prefix=str(data["predPrefix"]).strip()
			namespace=str(data["namespace"])
			table=table[start-1:end-1]
			result_text=procTable(header,datatype,table,entity,subj_prefix,pred_prefix)
			result_text=prefix_handler(result_text,namespace)
		else:
			print "download"
			turtle=request.form["outputRDF"]
			return Response(turtle,mimetype="text/plain",headers={"Content-Disposition":"attachment;filename=download.ttl"})
	return result_text
	# return Response(result,mimetype="text/plain",headers={"Content-Disposition":"attachment;filename=test.txt"})

# @app.route('/download')
# def download_file():
# 	turtle=request.form["outputRDF"]
# 	return Response(turtle,mimetype="text/plain",headers={"Content-Disposition":"attachment;filename=test.txt"})

if __name__ == '__main__':
	app.run(debug=True)