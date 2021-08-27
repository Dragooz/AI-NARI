from django.db import models

# Create your models here.

class Risk(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Solution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    disease = models.ManyToManyField(Disease, through='DiseaseSolutionRelationship')
    risk = models.ManyToManyField(Risk, through='RiskSolutionRelationship')

    def __str__(self):
        return self.name

#bridges
class DiseaseSolutionRelationship(models.Model): #D_S_Intermediate
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)

    def get_solution(self):
        return self.solution.name

class RiskSolutionRelationship(models.Model): #R_S_Intermediate
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)

    def get_solution(self):
        return self.solution.name


