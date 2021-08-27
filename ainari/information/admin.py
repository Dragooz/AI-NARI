from django.contrib import admin
from .models import Risk, Disease, Solution, DiseaseSolutionRelationship, RiskSolutionRelationship

# Register your models here.

class DiseaseSolutionRelationshipInline(admin.TabularInline):
    model = DiseaseSolutionRelationship

class RiskSolutionRelationshipInline(admin.TabularInline):
    model = RiskSolutionRelationship

class DiseaseAdmin(admin.ModelAdmin):
    inlines = [DiseaseSolutionRelationshipInline, ]

class RiskAdmin(admin.ModelAdmin):
    inlines = [RiskSolutionRelationshipInline, ]

class SolutionAdmin(admin.ModelAdmin):
    inlines = [DiseaseSolutionRelationshipInline, RiskSolutionRelationshipInline, ]

admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Solution, SolutionAdmin)
admin.site.register(Risk, RiskAdmin)

# admin.site.register(Disease)
# admin.site.register(DiseaseSolution)
# admin.site.register(DiseaseSolutionRelationship)
# admin.site.register(Risk)