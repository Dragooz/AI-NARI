from django.db import models

# Create your models here.

class RiskDisease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Solution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    risk_disease = models.ManyToManyField(RiskDisease, through='RiskDiseaseSolutionRelationship')

    def __str__(self):
        return self.name

#bridges
class RiskDiseaseSolutionRelationship(models.Model): #RD_S_Intermediate
    risk_disease = models.ForeignKey(RiskDisease, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    happened = models.BooleanField()

    def get_solution(self):
        return self.solution.name

