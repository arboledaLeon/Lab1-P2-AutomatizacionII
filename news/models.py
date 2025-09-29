from django.db import models

# Create your models here.
class News(models.Model):
    headline = models.CharField(max_length =200)
    body = models.TextField()
    date = models.DateField()

    def __str__(self): return self.headline

    class Meta:
        app_label = 'news'   # 👈 fuerza a Django a asociar el modelo con la app 'news'

