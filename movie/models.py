from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=100)  # Para el título
    description = models.CharField(max_length=250)  # Para descripción
    image = models.ImageField(upload_to='movie/images/')  # Para la imagen
    url = models.URLField(blank=True)
    
