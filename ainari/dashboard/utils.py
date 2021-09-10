import requests
import json
import re

import urllib.request
import os
import ssl
import base64

from django.conf import settings

def custom_vision_model(img_path):
    url="https://ainaricustomvision-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/7c329cd7-a59f-4a89-a1e9-5e0b551fda32/detect/iterations/ainari-objectDetection/image"
    headers={'content-type':'application/octet-stream','Prediction-Key': settings.CUSTOM_VISION_OBJ_DETECTION_KEY}
    r =requests.post(url,data=open(img_path,"rb"),headers=headers)
    content = json.loads(r.content.decode('utf-8'))
    # print(content)
    return content['predictions'][0]

def resnet_model(img_path):

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
                },
            ],
        },
        "GlobalParameters": {
        }
    }

    body = str.encode(json.dumps(data))

    url = 'http://52.175.16.149:80/api/v1/service/ainari-resnet/score'
    api_key = settings.RESNET_API_KEY # Replace this with the API key for the web service
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

def get_disease_prob(predictions):
    diseases = []
    probability = []

    for dict_ in predictions:
        for k, v in dict_.items():
            '''
            Scored Probabilities_brown_spot
            0.005899534560739994
            Scored Probabilities_healthy
            0.5360434055328369
            Scored Probabilities_hispa
            0.2814338803291321
            Scored Probabilities_leaf_blast
            0.17662310600280762
            '''
            if 'Scored Prob' in k:
                diseases.append(k.split('_', 1)[-1].lower().strip().replace(' ', '_'))
                probability.append(round(v, 4))

    return diseases, probability

def get_disease_prob_custom_vision(predictions):
    if predictions['probability'] >= 0.5:
        return predictions['tagName'], round(predictions['probability'],4)
    else:
        return 'healthy', '1.0'

def model_predict_risk(info):

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
                'Risk': "Brown Spot",
                'Temperature': info.temperature,
                'Humidity': info.humidity,
                'Water Level': info.water_level,
                'Nitrogen': info.soil_nitrogen,
                'Phosphorus': info.soil_phosphorus,
                'Potasium': info.soil_potassium,
                'pH': info.soil_pH,
                'Rainfall': info.rain_fall,
            },
        ],
    },
    "GlobalParameters": {
    }
}

    body = str.encode(json.dumps(data))

    url = 'http://52.175.16.149:80/api/v1/service/riskpredictor/score'
    api_key = settings.RISK_PREDICTOR_API_KEY # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        content = json.loads(response.read())
        print(content)
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