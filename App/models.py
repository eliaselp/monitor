from django.db import models

# Create your models here.

class dataset(models.Model):
    numero_analisis = models.IntegerField(null=False,blank=False,unique=True)
    valor_actual = models.IntegerField(null=False,blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

class Metadata(models.Model):
    key = models.TextField(null=False,blank=False)
    texto = models.TextField(null=False,blank=False)