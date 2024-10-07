from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views import View
from django.utils import timezone

from datetime import datetime

from App import models
from App import ecc
from . import models as local_models
import bleach
# Create your views here.

class Index(View):
    def get(self, request):
        if request.user.is_authenticated:
            request.user.tocken = ""
            request.user.save()
            if request.user.action_verify and request.user.verify == False:
                return redirect("verificar_2fa")
            if not request.user.is_staff:
                return redirect("panel")
            

            
            return render(request,"admin/index.html",{
            })
        return redirect('login')
    
    @staticmethod
    def Alerta(request,Error=None,Success=None):
        if request.user.is_authenticated:
            request.user.tocken = ""
            request.user.save()
            if request.user.action_verify and request.user.verify == False:
                return redirect("verificar_2fa")
            if not request.user.is_staff:
                return redirect("panel")
            text_code = None
            try:
                if models.Metadata.objects.filter(key="text_code").exists():
                    text_code = models.Metadata.objects.get(key="text_code")
                    text_code = text_code.texto
            except Exception as e:
                print(e)

            data = list(models.dataset.objects.all().order_by('id'))
            # Asegurarse de que la lista tenga al menos 20 elementos
            objetos = []
            if len(data) < 20:
                # Rellenar con ceros al principio si hay menos de 20 elementos
                objetos = [None] * (20 - len(data)) + data
            # Devolver los últimos 20 elementos
            else:
                objetos = data[-20:]
            
            return render(request,"admin/index.html",{
                "text_code":text_code,
                'data_set_balance':objetos,
                'Error':Error,
                "Success":Success,
            })
        return redirect('login')
    


class Licencias(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                if request.user.action_verify and request.user.verify == False:
                    return redirect("verificar_2fa")
                
                return render(request,"admin/licencias.html",{
                    "clientes":Licencias.get_licencias(request=request),
                })
            else:
                return redirect("panel")
        else:
            return redirect("login")

    @staticmethod
    def Alerta(request,Error=None,Success=None):
        if request.user.is_authenticated:
            if request.user.is_staff:
                if request.user.action_verify and request.user.verify == False:
                    return redirect("verificar_2fa")
                return render(request,"admin/licencias.html",{
                    "clientes":Licencias.get_licencias(request=request),
                    "Error":Error,"Success":Success,
                })
            else:
                return redirect("panel")
        else:
            return redirect("login")


    def post(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                if request.user.action_verify and not request.user.verify:
                    return redirect("verificar_2fa")

                uid = str(bleach.clean(request.POST.get("uid")).strip())
                fecha_limite = bleach.clean(request.POST.get("fecha_limite"))

                usuario = None
                if User.objects.filter(UID=uid).exists():
                    usuario = User.objects.get(UID=uid)
                else:
                    return Licencias.Alerta(request=request, Error="UID NO REGISTRADO")

                if usuario.email_verify == False:
                    return Licencias.Alerta(request=request, Error="El usuario no ha confirmado el email")
                
                hoy = timezone.now().date()
                if fecha_limite:
                    try:
                        fecha_limite_date = datetime.fromisoformat(fecha_limite).date()
                        if fecha_limite_date > hoy:
                            usuario.licencia = True
                            usuario.licencia_vencimiento = fecha_limite_date

                            private_key_pem , public_key_pem = ecc.generate_ecdsa_key_pair()
                            usuario.private_key = private_key_pem
                            usuario.public_key = public_key_pem
                            usuario.save()

                            return Licencias.Alerta(request=request, Success="Licencia otorgada correctamente")
                        else:
                            return Licencias.Alerta(request=request, Error="La fecha debe ser posterior a la fecha actual.")
                    except ValueError as e:
                        return Licencias.Alerta(request=request, Error="Formato de fecha no válido.")
                else:
                    return Licencias.Alerta(request=request, Error="Debe proporcionar una fecha límite.")
            else:
                return redirect("panel")
        else:
            return redirect("login")

    @staticmethod
    def get_licencias(request):
        if request.user.is_authenticated and request.user.is_staff:
            usuarios = User.objects.filter(licencia=True)
            i = 1
            contexto = []
            for u in usuarios:
                if Licencias.licencia_vencimiento_valida(u):
                    aux = {"i":i,"usuario":u}
                    contexto.append(aux)
                    i += 1
                else:
                    u.licencia = False
                    u.save()
            return contexto
                
    @staticmethod
    def licencia_vencimiento_valida(user: User) -> bool:
        try:
            if user.licencia:
                hoy = timezone.now().date()
                vencimiento = datetime.fromisoformat(str(user.licencia_vencimiento)).date()
                return vencimiento >= hoy
            return False
        except Exception as e:
            return False
    

class Eliminar_licencia(View):
    def get(self,request,uid):
        if request.user.is_authenticated:
            if request.user.is_staff:
                if request.user.action_verify and not request.user.verify:
                    return redirect("verificar_2fa")
                
                if not User.objects.filter(UID=uid).exists():
                    return Licencias.Alerta(request=request,Error="UID no registrado")
                try:
                    usuario = User.objects.get(UID=uid)
                    if usuario.licencia == False:
                        return Licencias.Alerta(request=request,Error="El usuario no tiene licencia")
                    else:
                        usuario.licencia = False
                        usuario.save()
                        return Licencias.Alerta(request=request,Success="Licencia eliminada con exito")
                except Exception as e:
                    return Licencias.Alerta(request=request,Error=str(e))

            else:
                return redirect("panel")
        else:
            return redirect("login")