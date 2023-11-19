from flask import Flask, request, jsonify
import tensorflow as tf
import os
import time
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
model=tf.keras.models.load_model("right.h5")
INPUTLENGTH=32
app = Flask(__name__)

@app.post("/predict")
def predict():
  now=round(time.time() * 1000)
  try:
    if(len(request.json['prediction_input'][0])!=INPUTLENGTH):
      raise Exception('Invalid input given')
    result=model.predict(request.json['prediction_input'])
    maxIdx=maxIndex(result)
    return jsonify({
      "name":request.json['name'],
      "hand":request.json['hand'],
      "timestamp":now,
      "probability":result[0][maxIdx]*1,
      "result":labels[maxIdx],
      "input_length":len(request.json['prediction_input'][0])
    })
  except Exception:
    return jsonify({
    "error":"Invalid input given"
  }),400
  

labels = [
  'Modified Skull Crushers',
  'Seated Rows',
  'Reserve Flyes',
  'Forward Punches',
  'Diagonal Shoulder Raise',
  'Overhead Triceps',
  'Lateral Raise',
  'Bicep Curls',
  'Overhead Press'
]

def maxIndex(arr):
  max=0
  idx=0
  for i,e in enumerate(arr[0]):
    if(e>max):
      max=e
      idx=i
  return idx
  