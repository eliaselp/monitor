from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


User.add_to_class('action_verify', models.BooleanField(null=False,default=False))
User.add_to_class('tocken', models.TextField(null=True,blank=True))
User.add_to_class('mailtocken', models.TextField(null=True,blank=True))
User.add_to_class('verify', models.BooleanField(null=False,default=False))

User.add_to_class('licencia', models.BooleanField(null=False,default=False))
User.add_to_class('licencia_vencimiento',models.DateField(default=timezone.now().date().isoformat(),null=True,blank=True))

User.add_to_class('email_verify', models.BooleanField(null=False,default=False))
User.add_to_class('nombre', models.TextField(null=True,blank=True))
User.add_to_class('telefono', models.TextField(null=True,blank=True))
User.add_to_class('UID', models.TextField(null=False,blank=True,default=""))

User.add_to_class('public_key', models.TextField(null=True,blank=True))
User.add_to_class('private_key', models.TextField(null=True,blank=True))

User.add_to_class('public_key_comunicacion', models.TextField(null=True,blank=True))
User.add_to_class('private_key_comunicacion', models.TextField(null=True,blank=True))

class dataset(models.Model):
    numero_analisis = models.IntegerField(null=False,blank=False,unique=True)
    valor_actual = models.IntegerField(null=False,blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


class Metadata(models.Model):
    key = models.TextField(null=False,blank=False)
    texto = models.TextField(null=False,blank=False)




class Prediccion(models.Model):
    analisis = models.IntegerField(null=False)
    prediccion = models.FloatField(null=False)
    real = models.FloatField(null=True)