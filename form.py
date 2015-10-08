import os
import json
from flask import Flask, request, render_template, Response, jsonify
from mimi import csvtoturtle,prefix_handler


# UPLOAD_FOLDER = '/uploads'
# ALLOWED_EXTENSIONS = set(['csv','txt'])

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def my_form():
	return render_template("index.html",result='')

@app.route('/process',methods=["GET","POST"])
def process_file():
	# file = request.files['csv_file']
	# if not file:
	# 	return "No file"
	# file_contents = file.stream.read()
	if request.method=="POST":
		turtle=request.form["outputRDF"]
		return Response(turtle,mimetype="text/plain",headers={"Content-Disposition":"attachment;filename=test.txt"})
	csv_text=request.args.get("csv_text")
	csv_text=csv_text.encode("utf-8")
	entity=request.args.get("entity").strip()
	subj_prefix=request.args.get("subj_prefix").strip()
	pred_prefix=request.args.get("pred_prefix").strip()
	delimiter=request.args.get("delimiter")
	start = request.args.get("start")
	end = request.args.get("end")
	data_type=json.loads(request.args.get("data_type"))
	# pred_prefix=json.loads(request.args.get("pred_prefix"))
	namespace=request.args.get("namespace")
	result_text=csvtoturtle(str(csv_text),str(delimiter),int(start),int(end),str(subj_prefix),str(entity),data_type,str(pred_prefix))
	if len(namespace)>0:
		result_text=prefix_handler(result_text,str(namespace))
	return jsonify(result=result_text)
	# return Response(result,mimetype="text/plain",headers={"Content-Disposition":"attachment;filename=test.txt"})

# @app.route('/download')
# def process_file():
# 	turtle=request.form["outputRDF"]
# 	return Response(turtle,mimetype="text/plain",headers={"Content-Disposition":"attachment;filename=test.txt"})

if __name__ == '__main__':
	app.run(debug=True)