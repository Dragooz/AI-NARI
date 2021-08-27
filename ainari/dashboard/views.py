from django.shortcuts import render
from .models import PaddyAreaDetail, PaddyAreaInfo, PaddyAreaDisease, PaddyAreaRisk
from information.models import DiseaseSolutionRelationship, RiskSolutionRelationship
from django.db.models import Max

# Create your views here.
def homepage(request):
    #getting only latest info from each area
    filter_ = PaddyAreaInfo.objects.values('paddy_area').annotate(latest_date=Max('date_time')).order_by('paddy_area')

    paddy_area_info = [ PaddyAreaInfo.objects.get(paddy_area=x['paddy_area'],date_time=x['latest_date'])
                        for x in filter_]

    # queryset = PaddyAreaInfo.objects.filter(id=1)
    # print(queryset.values())

    pad_obj = PaddyAreaDisease.objects.filter(paddy_area_info__in=paddy_area_info)
    disease_ids = set(i['paddy_area_info_id'] for i in pad_obj.values())

    par_obj = PaddyAreaRisk.objects.filter(paddy_area_info__in=paddy_area_info)
    risk_ids = set(i['paddy_area_info_id'] for i in par_obj.values())

    disease_solution = DiseaseSolutionRelationship.objects.all()
    risk_solution = RiskSolutionRelationship.objects.all()

    informations = {
        'info': paddy_area_info,
        'disease': pad_obj,
        'risk': par_obj,
        'disease_solution': disease_solution,
        'risk_solution': risk_solution,
        'disease_ids': disease_ids,
        'risk_ids': risk_ids,
    }

    return render(request, 'dashboard/homepage.html', informations)

def test(request):
    return render(request, 'dashboard/index.html')
