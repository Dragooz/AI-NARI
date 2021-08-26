from django.db import models

# Create your models here.

class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class DiseaseSolution(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    disease = models.ManyToManyField(Disease, through='DiseaseSolutionRelationship')

    def __str__(self):
        return self.name

#bridges
class DiseaseSolutionRelationship(models.Model): #D_DS_Intermediate
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    disease_solution = models.ForeignKey(DiseaseSolution, on_delete=models.CASCADE)

class Risk(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

