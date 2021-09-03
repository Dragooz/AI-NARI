from django.shortcuts import render
from information.models import RiskDiseaseSolutionRelationship, RiskDisease, Solution, RiskDiseaseRecommendationRelationship

# Create your views here.

def information(request):

    disease_obj = RiskDisease.objects.all()

    informations = {
        'disease_obj': disease_obj,
    }

    #4 diseases here
    return render(request, 'information/information.html', informations)

def information_detail(request, id):

    disease_obj = RiskDisease.objects.get(id=id)
    rd_solution_obj = RiskDiseaseSolutionRelationship.objects.filter(risk_disease__id = id)
    recommendation_obj = RiskDiseaseRecommendationRelationship.objects.filter(risk_disease__id = id)

    informations = {
        'disease_obj': disease_obj,
        'rd_solution_obj': rd_solution_obj,
        'recommendation_obj': recommendation_obj,
    }

    return render(request, 'information/information_detail.html', informations)