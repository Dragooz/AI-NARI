from django.db import models
from information.models import Disease, Risk
from django.contrib.auth.models import User

# Create your models here.

class PaddyAreaDetail(models.Model):
    paddy_area_name = models.CharField(max_length=5)
    state = models.CharField(max_length=20)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return self.paddy_area_name

class PaddyAreaInfo(models.Model): #child
    date_time = models.DateTimeField(auto_now_add=True)
    paddy_area = models.ForeignKey(PaddyAreaDetail, on_delete=models.CASCADE, default=None)
    paddy_height = models.FloatField()
    humidity = models.FloatField()
    temperature = models.FloatField()
    water_level = models.FloatField()
    paddy_images = models.ImageField(default='default.png', blank=True)

    #many-to-many
    disease = models.ManyToManyField(Disease, through='PaddyAreaDisease')
    risk = models.ManyToManyField(Risk, through='PaddyAreaRisk')

    def __str__(self):
        return self.paddy_area.paddy_area_name

#bridges
class PaddyAreaDisease(models.Model): #PAI_D_Intermediate
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    paddy_area_info = models.ForeignKey(PaddyAreaInfo, on_delete=models.CASCADE)
    d_confidence = models.FloatField()

class PaddyAreaRisk(models.Model): #PAI_R_Intermediate
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE)
    paddy_area_info = models.ForeignKey(PaddyAreaInfo, on_delete=models.CASCADE)
    r_confidence = models.FloatField()
