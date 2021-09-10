from django.shortcuts import render
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import redirect 
from django.forms.models import model_to_dict
from django.conf import settings

from .models import PaddyAreaDetail, PaddyAreaInfo, PaddyAreaRiskDisease
from information.models import RiskDiseaseSolutionRelationship, RiskDisease

from . import forms
from . import utils
from . import my_folium

from collections import defaultdict

import os
import time
import requests
import json
import re

ee = False

# Create your views here.
def homepage(request):
    #getting only latest info from each area
    filter_ = PaddyAreaInfo.objects.values('paddy_area').annotate(latest_date=Max('date_time')).order_by('paddy_area')

    paddy_area_info = [ PaddyAreaInfo.objects.get(paddy_area=x['paddy_area'],date_time=x['latest_date'])
                        for x in filter_]

    # queryset = PaddyAreaInfo.objects.filter(id=1)
    # print(queryset.values())
    # print(paddy_area_info)
    #objects
    pd_risk_disease = PaddyAreaRiskDisease.objects.filter(paddy_area_info__in=paddy_area_info)
    rd_solution = RiskDiseaseSolutionRelationship.objects.filter(risk_disease__id__in=pd_risk_disease.values_list('id'))
    # print(rd_solution)

    #ids
    potential_ids = set()
    warning_ids = set()

    # for i in pd_risk_disease.values():
    #     if i['happened'] == True and i['action_taken'] == False:
    #         warning_ids.add(i['paddy_area_info_id'])
    #     elif i['happened'] == False and i['action_taken'] == False:
    #         potential_ids.add(i['paddy_area_info_id'])

    for i in pd_risk_disease.values():
        if i['happened'] == True:
            warning_ids.add(i['paddy_area_info_id'])
        elif i['happened'] == False:
            potential_ids.add(i['paddy_area_info_id'])

    #map
    colour = []
    for i in paddy_area_info:
        if warning_ids or potential_ids:
            if i.id in warning_ids:
                colour.append('red')
            elif i.id in potential_ids:
                colour.append('yellow')
            else:
                colour.append('green')

    #map
    if paddy_area_info != []:
        map_ = my_folium.getMap(ee=ee, paddy_area_info=paddy_area_info, colour=colour)
    else:
        map_ = my_folium.getMap()

    informations = {
        'info': paddy_area_info,
        'pd_risk_disease': pd_risk_disease,
        'rd_solution': rd_solution,
        'potential_ids': potential_ids,
        'warning_ids': warning_ids,
        'map': map_,
    }

    return render(request, 'dashboard/homepage.html', informations)

def paddy_area_detail(request, paddy_area_name):
    paddy_area_info = PaddyAreaInfo.objects.filter(paddy_area__name=paddy_area_name).order_by('-date_time')
    # print(paddy_area_info.values_list('id'))
    #objects
    pd_risk_disease = PaddyAreaRiskDisease.objects.filter(paddy_area_info__id__in = paddy_area_info.values_list('id'))
    # print('rd:', [i.risk_disease.name for i in risk_disease])
    # print('rd:', [i.risk_disease.id for i in risk_disease])
    risk_disease_ids = set([i.risk_disease.id for i in pd_risk_disease]) #the ids of the risk_disease
    # print(risk_disease.values_list('id'))
    rd_solution = RiskDiseaseSolutionRelationship.objects.filter(risk_disease__id__in=risk_disease_ids)
    # print('rd:', rd_solution)
    # print('rd:', [i.solution.name for i in rd_solution])
    rd_ids = set([i['paddy_area_info_id'] for i in pd_risk_disease.values()])
    # print('rd_ids:', rd_ids)

    #maps

    rd_check_colour = PaddyAreaRiskDisease.objects.filter(paddy_area_info=paddy_area_info[0])
    #ids
    potential_ids = set()
    warning_ids = set()

    # for i in rd_check_colour.values():
    #     if i['happened'] == True and i['action_taken'] == False:
    #         warning_ids.add(i['paddy_area_info_id'])
    #     elif i['happened'] == False and i['action_taken'] == False:
    #         potential_ids.add(i['paddy_area_info_id'])

    for i in rd_check_colour.values():
        if i['happened'] == True:
            warning_ids.add(i['paddy_area_info_id'])
        elif i['happened'] == False:
            potential_ids.add(i['paddy_area_info_id'])

    if warning_ids:
        colour = ['red']
    elif potential_ids:
        colour = ['yellow']
    else:
        colour = ['green']

    #map
    if paddy_area_info != []:
        map_ = my_folium.getMap(ee=ee, paddy_area_info=paddy_area_info, colour=colour)
    else:
        map_ = my_folium.getMap()

    informations = {
        'info': paddy_area_info,
        'pd_risk_disease': pd_risk_disease,
        'rd_solution': rd_solution,
        'rd_ids':rd_ids,
        'map': map_,
        'lastest_info': paddy_area_info[0],
    }

    return render(request, 'dashboard/paddy_area_detail.html', informations)

def take_action(request): #get PaddyAreaRiskDisease's ID and modify the action boolean
    #get information
    pard_id = request.POST.get('pard_id')
    next_ = request.POST.get('next')
    action_name = request.POST.get('action_name')

    #call the robot to do something
    
    #update database
    obj = PaddyAreaRiskDisease.objects.get(id=pard_id)
    obj.action_taken = True

    # print('here',obj)
    try:
        obj.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False})

def create_info(request):
    if request.method == 'POST':
        form = forms.CreatePaddyAreaInfo(request.POST, request.FILES)
        if form.is_valid():
            
            #save to db
            instance = form.save(commit=True) #true here to save the img to db in order to be retrieved

            #hardcode the path first, future change
            my_image_path = utils.get_image_directory(instance.paddy_images.url)
            print('predicting...')

            # predicting using images
            predictions = utils.resnet_model(my_image_path)

            #predicting using informations
            risk_predictions = utils.model_predict_risk(instance)

            #modelv2
            diseases, probability = utils.get_disease_prob(predictions)
            risk_diseases, risk_probability = utils.get_disease_prob(risk_predictions)

            print('prediction done!')

            #add relationship

            #modelv2 using images
            for i in range(len(diseases)):
                if probability[i] >= 0.5 and diseases[i] != 'healthy':
                    instance.risk_disease.add(RiskDisease.objects.get(name=diseases[i]), 
                                              through_defaults={'confidence':probability[i], 'happened':True})

            #risk using informations
            for i in range(len(risk_diseases)):
                if risk_probability[i] >= 0.5 and risk_diseases[i] != 'healthy':
                    instance.risk_disease.add(RiskDisease.objects.get(name=risk_diseases[i]), 
                                              through_defaults={'confidence':risk_probability[i], 'happened':False})

            #save
            instance.save()
            
            return redirect('dashboard:homepage')

    else:
        form = forms.CreatePaddyAreaInfo()

    return render(request, 'dashboard/create_info.html', {'form': form})

def test_image(request):

    if request.method == 'POST':
        form = forms.TestImage(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=True) #true here to save the img to db in order to be retrieved

            #hardcode the path first, future change

            my_image_path = utils.get_image_directory(instance.paddy_images.url)

            print('predicting...')

            #using kaggle model
            predictions = utils.resnet_model(my_image_path)
            diseases, probability = utils.get_disease_prob(predictions)
            probability = [i*100 for i in probability]

            #using custom vision
            test_pred = utils.custom_vision_model(my_image_path)
            test_diseases, test_probability = utils.get_disease_prob_custom_vision(test_pred)
            test_probability = test_probability * 100
            print('prediction done!')

            info = {
                'image':instance.paddy_images.url,
                'diseases_probability': zip(diseases, probability),
                'custom_vision_diseases': test_diseases, 
                'custom_vision_probability':test_probability,
            }

            return render(request, 'dashboard/test_image.html', {'form': form, 'info': info})
    else:
        form = forms.TestImage()

    return render(request, 'dashboard/test_image.html', {'form': form})

def test_info(request):

    if request.method == 'POST':
        form = forms.TestInfo(request.POST)
        if form.is_valid():
            instance = form.save(commit=True) #true here to save the img to db in order to be retrieved

            print('predicting...')
            risk_predictions = utils.model_predict_risk(instance)
            risk_diseases, risk_probability = utils.get_disease_prob(risk_predictions)
            risk_probability = [i*100 for i in risk_probability]
            print('prediction done!')

            info = {
                'risk_diseases_probability': zip(risk_diseases,risk_probability),
            }

            return render(request, 'dashboard/test_info.html', {'form': form, 'info': info})
    else:
        form = forms.TestInfo()

    return render(request, 'dashboard/test_info.html', {'form': form})
