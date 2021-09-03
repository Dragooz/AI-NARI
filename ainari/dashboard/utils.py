import requests
import json
import re

import urllib.request
import os
import ssl
import base64

from django.conf import settings

def use_model(img_path):
    url="https://visionpaddy-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/8a7f3e83-d2ed-4b14-9d03-e6f32addcd74/classify/iterations/paddy%20disease/image"
    headers={'content-type':'application/octet-stream','Prediction-Key':'c36745d24f8349ed94b4e4c38399f307'}
    r =requests.post(url,data=open(img_path,"rb"),headers=headers)
    content = json.loads(r.content.decode('utf-8'))

    return content['predictions']

def use_modelv2(img_path):

    with open(img_path, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode('utf-8')

    def allowSelfSignedHttps(allowed):
        # bypass the server certificate verification on client side
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context

    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

    # Request data goes here
    data = {
        "Inputs": {
            "WebServiceInput0":
            [
                {
                    'image': "data:image/png;base64,"+ b64_string,
                    'id': "0",
                    'category': "BrownSpot",
                },
            ],
        },
        "GlobalParameters": {
        }
    }

    body = str.encode(json.dumps(data))

    url = 'http://23.99.111.74:80/api/v1/service/ainari-v1/score'
    api_key = 'bnzCIcdiVUuHQSSa8GKbqJtitQIt3yhq' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        content = json.loads(response.read())
        return content['Results']['WebServiceOutput0']

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        return json.loads(error.read().decode("utf8", 'ignore'))

def get_image_directory(image_instance_path):
    a= str(settings.BASE_DIR).split('\\')
    a[0] = 'D:\\'
    b= str(image_instance_path).split('/')
    return os.path.join(*a,*b) 