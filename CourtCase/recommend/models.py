from django.db import models

# Create your models here.
class Case(models.Model):
	title = models.CharField(max_length = 200)
	keyWords = models.TextField()
	content = models.TextField()