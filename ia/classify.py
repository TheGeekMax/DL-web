import tensorflow as tf
from tensorflow.keras.models import load_model as keras_load_model

import requests

import numpy as np
import pandas as pd
import os
import sys
import shutil

classifier = None

model_handle_map = {
  "mlp1" : "mlp_default.h5"
}

def config (model_name) :
  def load_model (model_name) :
    global classifier
    classifier = None
    if classifier is None :
      print(model_handle_map[model_name])
      model_path = os.path.join("models",model_handle_map[model_name])
      if not os.path.exists(model_path):
        print(f"Model {model_name} does not exist")
        sys.exit(1)
      classifier = keras_load_model(model_path)


  def dry_run () :
    global classifier
    input_shape = classifier.input_shape
    concrete_input_shape = (1,) + input_shape[1:]
    warmup_input = tf.random.uniform(concrete_input_shape, 0, 1.0)
    warmup_logits = classifier.predict(warmup_input)
    print ("warmup done")

  load_model (model_name)
  dry_run ()
        
def classify (text) :
  global classifier
  if classifier is None :
    print("Classifier not configured")
    return None
  
  def preprocess_text(txt):
    text = np.fromstring(txt, dtype=float, sep="\t")

    input_shape = classifier.input_shape
    concrete_input_shape = (1,) + input_shape[1:]
    text = text.reshape(concrete_input_shape)

    return text

  def build_result (probabilities) :
    result = 1 if probabilities[0][0] > 0.5 else 0
    return result
  
  def classify_text (text) :
    text = preprocess_text(text)

    probabilities = classifier.predict(text)
    result = build_result(probabilities)
    return result

  return classify_text(text)

