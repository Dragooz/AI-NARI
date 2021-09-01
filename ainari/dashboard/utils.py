import requests
import json
import re

def use_model(file):
    url="https://visionpaddy-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/8a7f3e83-d2ed-4b14-9d03-e6f32addcd74/classify/iterations/paddy%20disease/image"
    headers={'content-type':'application/octet-stream','Prediction-Key':'c36745d24f8349ed94b4e4c38399f307'}
    r =requests.post(url,data=open(file,"rb"),headers=headers)
    content = json.loads(r.content.decode('utf-8'))

    return content['predictions']