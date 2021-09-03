# # Full path and name to your csv file
import os, sys, django
import pandas as pd
import csv

from django.conf import settings
from django.core.files import File

# Full path to the directory immediately above your django project directory
your_djangoproject_home= settings.AINARI_PROJECT_PATH
sys.path.append(your_djangoproject_home)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ainari.settings')
django.setup()

os.chdir(your_djangoproject_home)

# path to csv
P_dashboard_paddyareadetail= os.path.join (os.getcwd(), 'dummy_data', 'dashboard_paddyareadetail.csv')
P_dashboard_paddyareainfo= os.path.join (os.getcwd(), 'dummy_data', 'dashboard_paddyareainfo.csv')
P_dashboard_paddyareariskdisease= os.path.join(os.getcwd(), 'dummy_data', 'dashboard_paddyareariskdisease.csv')
P_information_risk= os.path.join(os.getcwd(), 'dummy_data', 'information_disease.csv')
P_information_risksolution= os.path.join(os.getcwd(), 'dummy_data', 'information_solution.csv')
P_information_risksolutionrelationship= os.path.join(os.getcwd(), 'dummy_data', 'information_risksolutionrelationship.csv')
P_information_riskrecommendation = os.path.join(os.getcwd(), 'dummy_data', 'information_recommendation.csv')
P_information_riskrecommendationrelationship = os.path.join(os.getcwd(), 'dummy_data', 'information_riskrecommendationrelationship.csv')

from dashboard.models import *
from information.models import *

def createPaddyInfo():
    info_df = pd.read_csv(P_dashboard_paddyareainfo)

    riskdisease_df = pd.read_csv(P_dashboard_paddyareariskdisease)

    for idx, row_i in info_df.iterrows():
        dashboard_paddyareainfo = PaddyAreaInfo()
        dashboard_paddyareainfo.paddy_area = PaddyAreaDetail.objects.get(name=str(row_i[2]))
        dashboard_paddyareainfo.paddy_height = row_i[3]
        dashboard_paddyareainfo.humidity = row_i[4]
        dashboard_paddyareainfo.temperature = row_i[5]
        dashboard_paddyareainfo.water_level = row_i[6]
        dashboard_paddyareainfo.soil_nitrogen = row_i[7]
        dashboard_paddyareainfo.soil_phosphorous = row_i[8]
        dashboard_paddyareainfo.soil_potassium = row_i[9]
        dashboard_paddyareainfo.soil_pH = row_i[10]
        # dashboard_paddyareainfo.paddy_images = row_i[11]  
        dashboard_paddyareainfo.paddy_images.save(os.path.basename(row_i[11]), File(open(row_i[11], "rb")))
        dashboard_paddyareainfo.save()

        for _, row_r in riskdisease_df.loc[riskdisease_df['PaddyAreaInfo_ID']==idx+1].iterrows():
            if row_r[3]<0.5: #threshold
                continue
            else:
                dashboard_paddyareainfo.risk_disease.add(RiskDisease.objects.get(pk=int(row_r[1])), through_defaults={'confidence':row_r[3], 'happened':row_r[4]})


def createPaddyDetails():
    with open(P_dashboard_paddyareadetail, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            dashboard_paddyareadetail = PaddyAreaDetail()
            dashboard_paddyareadetail.name = row[0]
            dashboard_paddyareadetail.state = row[1]
            dashboard_paddyareadetail.latitude = row[2]
            dashboard_paddyareadetail.longitude = row[3]
            dashboard_paddyareadetail.save()


def createRisk():
    with open(P_information_risk, "r") as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)
        for row in csvreader:
            information_risk = RiskDisease()
            information_risk.name = row[1].lower().strip().replace(' ', '_')
            information_risk.description = row[2]
            # information_risk.risk_disease_image= row[3]
            information_risk.risk_disease_image.save(os.path.basename(row[3]), File(open(row[3], "rb")))
            information_risk.save()


def createSolution():
    solution_df = pd.read_csv(P_information_risksolution)
    risksolutionrel_df = pd.read_csv(P_information_risksolutionrelationship)

    for idx, row_rs in solution_df.iterrows():
        information_risksolution = Solution()
        information_risksolution.name = row_rs[1]
        information_risksolution.description = row_rs[2]
        # information_risksolution.solution_image = row_rs[3]
        information_risksolution.solution_image.save(os.path.basename(row_rs[3]), File(open(row_rs[3], "rb")))

        information_risksolution.save()

        for _, row_rel in risksolutionrel_df.loc[risksolutionrel_df['Solution']==idx+1].iterrows():
            information_risksolution.risk_disease.add(RiskDisease.objects.get(pk=row_rel[1]), through_defaults = {'happened':row_rel[3]})  


def createRecommendation():
    recommendation_df = pd.read_csv(P_information_riskrecommendation)
    riskrecommendationrel_df = pd.read_csv(P_information_riskrecommendationrelationship)

    for idx, row_rc in recommendation_df.iterrows():
        information_riskrecommendation = Recommendation()
        information_riskrecommendation.name = row_rc[1]
        information_riskrecommendation.description = row_rc[2]
        # information_riskrecommendation.recommendation_image = row_rc[3]
        information_riskrecommendation.recommendation_image.save(os.path.basename(row_rc[3]), File(open(row_rc[3], "rb")))
        information_riskrecommendation.save()

        for _, row_rel in riskrecommendationrel_df.loc[riskrecommendationrel_df['Recommendation_ID']==idx+1].iterrows():
            information_riskrecommendation.risk_disease.add(RiskDisease.objects.get(pk=row_rel[1]))
    
# createRisk()
# createPaddyDetails()
# createPaddyInfo()
# createSolution()
# createRecommendation()

