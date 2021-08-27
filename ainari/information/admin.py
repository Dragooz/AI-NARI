from django.contrib import admin
from .models import RiskDisease, Solution, RiskDiseaseSolutionRelationship

# Register your models here.

class RiskDiseaseSolutionRelationship(admin.TabularInline):
    model = RiskDiseaseSolutionRelationship

class RiskDiseaseAdmin(admin.ModelAdmin):
    inlines = [RiskDiseaseSolutionRelationship, ]

class SolutionAdmin(admin.ModelAdmin):
    inlines = [RiskDiseaseSolutionRelationship, ]

admin.site.register(RiskDisease, RiskDiseaseAdmin)
admin.site.register(Solution, SolutionAdmin)
