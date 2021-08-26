from django.contrib import admin
from .models import *

# Register your models here.

class DiseaseSolutionRelationshipInline(admin.TabularInline):
    model = DiseaseSolutionRelationship

class DiseaseAdmin(admin.ModelAdmin):
    inlines = [DiseaseSolutionRelationshipInline, ]

class DiseaseSolutionAdmin(admin.ModelAdmin):
    inlines = [DiseaseSolutionRelationshipInline, ]

admin.site.register(Disease, DiseaseAdmin)
admin.site.register(DiseaseSolution, DiseaseSolutionAdmin)
admin.site.register(Risk)

# admin.site.register(Disease)
# admin.site.register(DiseaseSolution)
# admin.site.register(DiseaseSolutionRelationship)
# admin.site.register(Risk)