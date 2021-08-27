from django.db import models
from information.models import RiskDisease
from django.contrib.auth.models import User

# Create your models here.

class PaddyAreaDetail(models.Model):
    paddy_area_name = models.CharField(max_length=5)
    state = models.CharField(max_length=20)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.paddy_area_name

    def get_coordinates(self):
        return 'LONG: ' + str(self.longitude) + ', LAT: ' + str(self.latitude)

    def get_state(self):
        return self.state

class PaddyAreaInfo(models.Model): #child
    date_time = models.DateTimeField(auto_now_add=True)
    paddy_area = models.ForeignKey(PaddyAreaDetail, on_delete=models.CASCADE, default=None)
    paddy_height = models.FloatField()
    humidity = models.FloatField()
    temperature = models.FloatField()
    water_level = models.FloatField()
    soil_nitrogen = models.FloatField(default= 0)
    paddy_images = models.ImageField(default='default.png', blank=True)

    #many-to-many
    risk_disease = models.ManyToManyField(RiskDisease, through='PaddyAreaRiskDisease')

    def __str__(self):
        return self.paddy_area.paddy_area_name

#bridges
class PaddyAreaRiskDisease(models.Model): #PAI_D_Intermediate
    risk_disease = models.ForeignKey(RiskDisease, on_delete=models.CASCADE)
    paddy_area_info = models.ForeignKey(PaddyAreaInfo, on_delete=models.CASCADE)
    confidence = models.FloatField()
    happened = models.BooleanField()

    def get_id(self):
        return self.paddy_area_info.id

    def get_disease_name(self):
        return self.risk_disease.name

    def get_confidence(self):
        return self.confidence