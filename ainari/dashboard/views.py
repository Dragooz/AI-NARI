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
        map_ = my_folium.getMap(ee=False, paddy_area_info=paddy_area_info, colour=colour)
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
        map_ = my_folium.getMap(ee=False, paddy_area_info=paddy_area_info, colour=colour)
    else:
        map_ = my_folium.getMap()

    informations = {
        'info': paddy_area_info,
        'pd_risk_disease': pd_risk_disease,
        'rd_solution': rd_solution,
        'rd_ids':rd_ids,
        'map': map_,
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
            # predictions = utils.use_model(my_image_path)
            predictions = utils.use_modelv2(my_image_path)
            
            diseases = []
            probability = []
            
            #modelv1
            # for dict_ in predictions:
            #     for k, v in dict_.items():
            #         if k=='probability':
            #             probability.append(v)
            #         elif k=='tagName':
            #             diseases.append(v)

            #modelv2
            for dict_ in predictions:
                for k, v in dict_.items():
                    print(k)
                    print(v)
                    if 'Scored Prob' in k:
                        diseases.append(k.split('_')[-1].lower().strip().replace(' ', '_'))
                        probability.append(v)
            print('prediction done!')

            #add relationship
            
            for i in range(len(diseases)):
                if probability[i] >= 0.5 and diseases[i] != 'Healthy':
                    instance.risk_disease.add(RiskDisease.objects.get(name=diseases[i]), 
                                              through_defaults={'confidence':probability[i], 'happened':True})

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
            # predictions = utils.use_model(my_image_path)
            predictions = utils.use_modelv2(my_image_path)
            print('prediction done!')
            
            diseases = []
            probability = []
            
            #modelv1
            # for dict_ in predictions:
            #     for k, v in dict_.items():
            #         if k=='probability':
            #             probability.append(v)
            #         elif k=='tagName':
            #             diseases.append(v)

            #modelv2
            for dict_ in predictions:
                for k, v in dict_.items():
                    print(k)
                    print(v)
                    if 'Scored Prob' in k:
                        diseases.append(k.split('_')[-1].strip())
                        probability.append(v)

            info = {
                'image':instance.paddy_images.url,
                'diseases_probability': zip(diseases,probability),
            }

            return render(request, 'dashboard/test_image.html', {'form': form, 'info': info})
    else:
        form = forms.CreatePaddyAreaInfo()

    return render(request, 'dashboard/test_image.html', {'form': form})
