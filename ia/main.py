import classify
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)



@app.route ('/config', methods=['POST'])
def doConfiguration():
   print ("configuring")
   model_name = "mlp1"
   if 'model' in request.args:
      model_name = request.args['model']
      print ("model name is " + model_name)
   classify.config(model_name)
   print ("done")
   return { "status" : "ok", "data": "configuration is done" }


@app.route ('/classify', methods=['POST'])
def doClassification():
   print ("classifying")
   text = ""
   if 'text' in request.form:
      text = request.form['text']
   if 'text' in request.args:
      text = request.args['text']
   if 'text' in request.json:
      text = request.json['text']
   
   res = classify.classify(text)
   result = {}
   if res is not None:
      result = { "result": res }
   else:
      result = { "result": "error" }
   
   print (result)
   print ("done")
   return { "status" : "ok", "data": result}

@app.route ('/validate', methods=['POST'])
def doValidation():
   print ("validating")
   labels = []
   validation_data = []
   with open("validation/labels.tsv", "r") as f:
      for line in f:
         labels.append(int(line))

   with open("validation/values.tsv", "r") as f:
      for line in f:
          validation_data.append(line)
   
   result = []
   print(labels)
   for i in range(len(validation_data)):
      res = classify.classify(validation_data[i])
      result.append({"label": int(labels[i]), "result": res})
   print (result)
   print ("done")
   return { "status" : "ok", "data": result }
  
@app.route ('/', methods=['GET'])
def doHome():
   return '''
   <!doctype html>
   <html>
	   <head>
	      <title>Sismic Classifier</title>
         <meta charset="UTF-8" />
	   </head>
	   <body>
	      <h1>Hello World</h1>
	   </body>
   </html>
   '''

if __name__ == '__main__' :
   print ("starting")
   app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)
   print ("done")

