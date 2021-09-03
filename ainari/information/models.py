from django.db import models

# Create your models here.

class RiskDisease(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    risk_disease_image = models.ImageField(default='default.png', blank=True, upload_to='risk_disease_images')

    def __str__(self):
        return self.name.replace('_', ' ').capitalize()

    def display_name(self):
        return ' '.join([i.capitalize() for i in self.name.split('_')])    

class Solution(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    solution_image = models.ImageField(default='default.png', blank=True, upload_to='solution_images')
    risk_disease = models.ManyToManyField(RiskDisease, through='RiskDiseaseSolutionRelationship')

    def __str__(self):
        return self.name

class Recommendation(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    recommendation_image = models.ImageField(default='default.png', blank=True, upload_to='recommendations_images')
    risk_disease = models.ManyToManyField(RiskDisease, through='RiskDiseaseRecommendationRelationship')

    def __str__(self):
        return self.name

#bridges
class RiskDiseaseSolutionRelationship(models.Model): #RD_S_Intermediate
    risk_disease = models.ForeignKey(RiskDisease, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    happened = models.BooleanField()

    def get_solution(self):
        return self.solution.name

class RiskDiseaseRecommendationRelationship(models.Model): #RD_S_Intermediate
    risk_disease = models.ForeignKey(RiskDisease, on_delete=models.CASCADE)
    recommendation = models.ForeignKey(Recommendation, on_delete=models.CASCADE)

    def get_recommendation(self):
        return self.recommendation.name

