from django.contrib import admin
from .models import *

# Register your models here.

class PaddyAreaDiseaseInline(admin.TabularInline):
    model = PaddyAreaDisease

class PaddyAreaRiskInline(admin.TabularInline):
    model = PaddyAreaRisk

class PaddyAreaInfoAdmin(admin.ModelAdmin):
    inlines = [PaddyAreaDiseaseInline, PaddyAreaRiskInline, ]


admin.site.register(PaddyAreaInfo, PaddyAreaInfoAdmin)
admin.site.register(PaddyAreaDetail)

# admin.site.register(PaddyAreaInfo)
# admin.site.register(PaddyAreaDetail)
# admin.site.register(PaddyAreaDisease)
# admin.site.register(PaddyAreaRisk)