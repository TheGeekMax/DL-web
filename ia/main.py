import classify
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

import os

app = Flask(__name__)



@app.route ('/config', methods=['POST'])
def doConfiguration():
   print ("configuring")
   model_name = "mlp1"
   if 'name' in request.args:
      model_name = request.args['graph']
   classify.config(model_name)
   print ("done")
   return { "status" : "ok", "data": "configuration is done" }


@app.route ('/classify', methods=['POST'])
def doClassification():
   print ("classifying")
   """
   if 'picture' not in request.files:
      return ("bad url", 400)
   picture = request.files['picture']
   if not picture :
      return ("picture is wrong", 400)
   if picture.filename == '':
      return ("picture is empty", 400)
   if not allowed_file(picture.filename):
      return ("picture is empty", 400)
   filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(picture.filename))
   picture.save(filename)
   result = classify.classify(filename);
   print (result)
   """
   list = []
   if 'text' in request.form:
      list = request.form['text'].split("\n")
   if 'text' in request.args:
      list = request.args['text'].split("\n")
   if 'text' in request.json:
      list = request.json['text'].split("\n")
   if len(list) == 0:
      return ("no text to classify", 400)
   classifier = classify.classify(list[0])
   result = []
   for i in range(len(list)):
      res = classify.classify(list[i])
      result.append({"text": list[i], "result": res})
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

