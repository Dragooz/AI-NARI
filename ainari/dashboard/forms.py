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
            'soil_nitrogen': ('Soil Nitrogen (mg/kg)')
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