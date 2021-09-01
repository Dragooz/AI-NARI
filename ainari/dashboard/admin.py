from django.contrib import admin
from .models import PaddyAreaDetail, PaddyAreaInfo, PaddyAreaRiskDisease, TestImage

# Register your models here.

class PaddyAreaRiskDiseaseInline(admin.TabularInline):
    model = PaddyAreaRiskDisease


class PaddyAreaInfoAdmin(admin.ModelAdmin):
    inlines = [PaddyAreaRiskDiseaseInline, ]

admin.site.register(PaddyAreaDetail)
admin.site.register(PaddyAreaInfo, PaddyAreaInfoAdmin)
admin.site.register(TestImage)

# admin.site.register(PaddyAreaInfo)
# admin.site.register(PaddyAreaDetail)
# admin.site.register(PaddyAreaDisease)
# admin.site.register(PaddyAreaRisk)