from django.shortcuts import render
from .models import PaddyAreaDetail, PaddyAreaInfo, PaddyAreaRiskDisease
from information.models import RiskDiseaseSolutionRelationship
from django.db.models import Max

# Create your views here.
def homepage(request):
    #getting only latest info from each area
    filter_ = PaddyAreaInfo.objects.values('paddy_area').annotate(latest_date=Max('date_time')).order_by('paddy_area')

    paddy_area_info = [ PaddyAreaInfo.objects.get(paddy_area=x['paddy_area'],date_time=x['latest_date'])
                        for x in filter_]

    # queryset = PaddyAreaInfo.objects.filter(id=1)
    # print(queryset.values())

    risk_disease = PaddyAreaRiskDisease.objects.filter(paddy_area_info__in=paddy_area_info)
    rd_ids = set(i['paddy_area_info_id'] for i in risk_disease.values())

    rd_solution = RiskDiseaseSolutionRelationship.objects.all()

    informations = {
        'info': paddy_area_info,
        'risk_disease': risk_disease,
        'rd_solution': rd_solution,
        'rd_ids': rd_ids,
    }

    return render(request, 'dashboard/homepage.html', informations)

def test(request):
    return render(request, 'dashboard/index.html')
