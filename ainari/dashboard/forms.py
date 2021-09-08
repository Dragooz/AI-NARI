from django import forms
from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field

class CreatePaddyAreaInfo(forms.ModelForm):

    class Meta:
        model = models.PaddyAreaInfo
        fields = '__all__'
        exclude = ('risk_disease',)

        labels = {
            'paddy_height': ('Paddy Height (m)'),
            'humidity': ('Humidity (g/kg)'),
            'temperature': ('Temperature (Celcius)'),
            'water_level': ('Water Level (m)'),
            'soil_nitrogen': ('Soil Nitrogen (mg/kg)'),
            'soil_phosphorous': ('Soil Phosphorous (mg/kg)'),
            'soil_potassium': ('Soil Potassium (mg/kg)'),
            'soil_pH': ('Soil pH'),
            'rain_fall': ('Rain Fall (mm)'),
        }
        # help_texts = {
        #     'paddy_height': ('1'),
        # }
        # error_messages = {
        #     'name': {
        #         'max_length': ("This writer's name is too long."),
        #     },
        # }

class TestImage(forms.ModelForm):

    class Meta:
        model = models.TestImage
        fields = ['paddy_images',]

class TestInfo(forms.ModelForm):
    class Meta:
        model = models.TestInfo
        fields = '__all__'

        labels = {
            'humidity': ('Humidity (g/kg)'),
            'temperature': ('Temperature (Celcius)'),
            'water_level': ('Water Level (m)'),
            'soil_nitrogen': ('Soil Nitrogen (mg/kg)'),
            'soil_phosphorous': ('Soil Phosphorous (mg/kg)'),
            'soil_potassium': ('Soil Potassium (mg/kg)'),
            'soil_pH': ('Soil pH'),
            'rain_fall': ('Rain Fall (mm)'),
        }