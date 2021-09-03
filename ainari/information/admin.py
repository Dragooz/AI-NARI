from django.contrib import admin
from .models import RiskDisease, Solution, RiskDiseaseSolutionRelationship, Recommendation, RiskDiseaseRecommendationRelationship

# Register your models here.

class RiskDiseaseSolutionRelationship(admin.TabularInline):
    model = RiskDiseaseSolutionRelationship

class RiskDiseaseRecommendationRelationship(admin.TabularInline):
    model = RiskDiseaseRecommendationRelationship

class RiskDiseaseAdmin(admin.ModelAdmin):
    inlines = [RiskDiseaseSolutionRelationship, ]

class SolutionAdmin(admin.ModelAdmin):
    inlines = [RiskDiseaseSolutionRelationship, ]

class RecommendationAdmin(admin.ModelAdmin):
    inlines = [RiskDiseaseRecommendationRelationship, ]

admin.site.register(RiskDisease, RiskDiseaseAdmin)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(Recommendation, RecommendationAdmin)