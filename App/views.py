from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import datetime

from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.decorators import otp_required

from . import models
from . import correo
from . import utils
from . import validaciones
from . import ecc
from admins import config

import bleach


class Login(View):
    def get(self,request):
        if not request.user.is_authenticated:
            return render(request,"login/login.html")
        if request.user.is_staff:
            return redirect("admin_panel")
        else:
            return redirect("panel")
    #####
    def post(self,request):
        if not request.user.is_authenticated:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            print(request.POST)
            if user is not None:
                login(request, user)
                user.verify = False
                user.save()

                if user.email_verify == False and not user.is_staff:
                    enviar_mail_validacion(request.user)

                if request.user.is_staff:
                    return redirect("admin_panel")
                else:
                    return redirect("panel")
            else:
                return render(request, 'login/login.html', {'Error': 'Invalid username or password'})
        else:
            if request.user.is_staff:
                return redirect("admin_panel")
            else:
                return redirect("panel")
    
    @staticmethod
    def Alerta(request,Error=None,Success=None):
        if not request.user.is_authenticated:
            return render(request,"login/login.html",{
                "Error":Error,"Success":Success
            })
        else:
            if request.user.is_staff:
                return redirect("admin_panel")
            else:
                return redirect("panel")



class Register(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request,"login/register.html")
        else:
            if request.user.is_staff:
                return redirect("admin_panel")
            else:
                return redirect("panel")
            
    def post(self,request):
        if not request.user.is_authenticated:
            nombre = str(bleach.clean(request.POST.get("nombre")).strip().title())
            email = str(bleach.clean(request.POST.get("email")).strip())
            telefono = str(bleach.clean(request.POST.get("telefono")).strip())
            username = str(bleach.clean(request.POST.get("username")).strip())
            password1 = str(bleach.clean(request.POST.get("password1")).strip().title())
            password2 = str(bleach.clean(request.POST.get("password2")).strip().title())

            if "" in [nombre,email,telefono,username,password1,password2]:
                return Register.Alerta(request=request, Error="Todos los campos son obligatorios")
            #################
            if not validaciones.Verificador.mayuscula_minuscula_espacio(nombre) and len(nombre) <= 25:
                return Register.Alerta(request=request, Error="El nombre solo admite Mayusculas, Minusculas y caracter Espacio y menos de 25 caracteres")
            if User.objects.filter(nombre=nombre).exists():
                return Register.Alerta(request=request, Error="El nombre ya esta en uso")                        
            #################
            if not validaciones.Verificador.validar_correo(email) and len(email) <= 200:
                return Register.Alerta(request=request, Error="Formato de correo incorrecto o demaciado largo")
            if User.objects.filter(email=email).exists():
                return Register.Alerta(request=request, Error="El email ya esta en uso")
            #################
            if not validaciones.Verificador.validar_numero_telefono(telefono):
                return Register.Alerta(request=request, Error="El formato del teléfono es incorrecto")
            #################
            if not validaciones.Verificador.mayuscula_minuscula_numeros(username):
                return Register.Alerta(request=request, Error="EL username solo admite Mayusculas, Minusculas, numeros y el caracter '_'")
            if User.objects.filter(username=username).exists():
                return Register.Alerta(request=request, Error="El username ya esta en uso")
            #################
            pw = validaciones.Verificador.validar_password(password1,password2)
            if pw!="OK":
                return Register.Alerta(request=request, Error=pw)
            
            uid=""
            while(User.objects.filter(UID=uid).exists() or uid == ""):
                uid=utils.get_tocken()

            user = User(username=username,nombre=nombre,email=email,telefono=telefono,UID=uid)
            user.set_password(password1)
            user.save()
            user = authenticate(request, username=username, password=password1)
            login(request, user)
            if user.email_verify == False:
                enviar_mail_validacion(request.user)
            return redirect("panel")
        else:
            if request.user.is_staff:
                return redirect("admin_panel")
            else:
                return redirect("panel")

    @staticmethod
    def Alerta(request,Error=None,Success=None):
        if not request.user.is_authenticated:
            return render(request,"login/register.html",{
                "Error":Error,
                "Success":Success,
            })
        else:
            if request.user.is_staff:
                return redirect("admin_panel")
            else:
                return redirect("panel")

def Logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("login")

########################################################################################

def licencia_vencimiento_valida(user: User) -> bool:
    try:
        if user.licencia:
            hoy = timezone.now().date()
            vencimiento = datetime.fromisoformat(str(user.licencia_vencimiento)).date()
            return vencimiento >= hoy
        return False
    except Exception as e:
        return False




def enviar_mail_validacion(usuario):
    if usuario.email_verify == False:
        usuario.mailtocken = utils.get_tocken()
        usuario.save()
        Asunto = "Elias IA - Confirmación de tu Email"
        mensaje = f'''
Estimado {usuario.nombre}:

Gracias por registrarte con nosotros. Por favor, haz clic en el enlace a continuación para confirmar tu dirección de correo electrónico:

{config.url_base}validar_mail/{usuario.UID}/{usuario.mailtocken}/

Si no te has registrado con nosotros, por favor ignora este correo.

¡Nos vemos pronto!

Saludos, Elias IA

'''
        correo.enviar_correo(usuario.email,Asunto=Asunto,s=mensaje)

########################################################################################



class Index(View):
    def get(self,request):
        if request.user.is_authenticated:
            request.user.tocken = ""
            request.user.save()
            if request.user.action_verify and request.user.verify == False:
                return redirect("verificar_2fa")
            if request.user.is_staff:
                return redirect("admin_panel")
            
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
            


            dataset_predictions = list(models.Prediccion.objects.all().order_by('id'))
            if len(data) >= 20:
                dataset_predictions = dataset_predictions[-20:]
            else:
                dataset_predictions += [None] * (20 - len(dataset_predictions))
            
            min_valor = float('inf')
            max_valor = float('-inf')
            found = False
            for pred in dataset_predictions:
                if not pred is None:
                    found = True
                    min_valor = min(min_valor, pred.prediccion)
                    max_valor = max(max_valor, pred.prediccion)
                    if not pred.real is None:
                        min_valor = min(min_valor, pred.real)
                        max_valor = max(max_valor, pred.real)
            if found == False:
                min_valor = 10
                max_valor = 50
            
            return render(request,"panel/index.html",{
                "text_code":text_code,
                'data_set_balance':objetos,
                "licencia_valida":licencia_vencimiento_valida(request.user),
                'dataset_predictions':dataset_predictions,
                'max_valor_prediccion':max_valor,
                'min_valor_prediccion':min_valor,
            })
        return redirect('login')

    @staticmethod
    def Alerta(request,Error=None,Success=None):
        if request.user.is_authenticated:
            request.user.tocken = ""
            request.user.save()
            if request.user.action_verify and request.user.verify == False:
                return redirect("verificar_2fa")
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

            
            dataset_predictions = list(models.Prediccion.objects.all().order_by('id'))
            if len(data) >= 20:
                dataset_predictions = dataset_predictions[-20:]
            min_valor = float('inf')
            max_valor = float('-inf')
            found = False
            for pred in dataset_predictions:
                if not pred is None:
                    found = True
                    min_valor = min(min_valor, pred.prediccion, pred.real)
                    max_valor = max(max_valor, pred.prediccion, pred.real)
            if found == False:
                min_valor = 10
                max_valor = 50


            return render(request,"panel/index.html",{
                "text_code":text_code,
                'data_set_balance':objetos,
                "licencia_valida":licencia_vencimiento_valida(request.user),
                'dataset_predictions':dataset_predictions,
                'max_valor_prediccion':max_valor,
                'min_valor_prediccion':min_valor,
                "Error":Error,
                "Success":Success
            })
        return redirect('login')


class backend_verificacion_email(View):
    def get(self, request, opc:int):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                return redirect("verificar_2fa")
            
            tocken = utils.get_tocken()
            request.user.tocken = tocken
            request.user.save()
            accion = "habilitar"
            if request.user.action_verify == True:
                accion = "deshabilitar"
            if opc == 1:
                Asunto = f"Confirmacion para {accion} 2FA"
                Mensaje = f'''
Hola {request.user.username},

Tu solicitud para {accion} la autenticación de dos factores (2FA) ha sido recibida. 
Para completar el proceso, por favor utiliza el siguiente código de confirmación:

Código de Confirmación: {tocken}

Si no has solicitado habilitar el 2FA, por favor ignora este mensaje o contacta con nuestro soporte.

Gracias,
El equipo de webditech

    '''
                correo.enviar_correo(email=request.user.email,Asunto=Asunto,s=Mensaje)
            return HttpResponse(status=204)
        return redirect("login")
    
    def post(self,request,opc):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                return redirect("../../../../../../../verificar/")
            
            tocken = str(bleach.clean(request.POST.get('tocken'))).strip()
            location = str(bleach.clean(request.POST.get('location')))
            if "" in [tocken,location]:
                return render(request,f"panel/{location}.html",{
                    "Error":"Todos los campos son obligatorios",
                    "licencia_valida":licencia_vencimiento_valida(request.user),
                })
            if tocken != request.user.tocken:
                return render(request,f"panel/{location}.html",{
                    "Error":"Error: Tocken Invalido",
                    "licencia_valida":licencia_vencimiento_valida(request.user),
                })
            tocken = utils.get_tocken()
            request.user.tocken = tocken
            request.user.save()
            return redirect(f"../../../../../../../../../../../../mfa/{tocken}/")
        return redirect("login")


class Validar_Mail(View):
    def get(self,request, uid, tocken, *args, **kwargs):
        if User.objects.filter(UID=uid).exists():
            usuario = User.objects.get(UID=uid)
            if usuario.mailtocken == tocken:
                usuario.email_verify = True
                usuario.save()
                if request.user.is_authenticated:
                    return Login.Alerta(request=request,Success="Correo electronico validado correctamente")
                else:
                    return Index.Alerta(request=request,Success="Correo electronico validado correctamente")
        if request.user.is_authenticated:
            return Login.Alerta(request=request,Error="Acceso Denegado")
        else:
            return Index.Alerta(request=request,Error="Acceso Denegado")
                        


###################################
######### 2FA #####################
###################################

class MFA(View):
    def get(self, request,tocken):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                return redirect("../../../../../../../verificar/")

            tocken = bleach.clean(tocken)
            if tocken != request.user.tocken or tocken=="":
                return render(request,f"panel/index.html",{
                    "Error":"Acceso Denegado",
                    "licencia_valida":licencia_vencimiento_valida(request.user),
                })
            user = request.user
            device, created = TOTPDevice.objects.get_or_create(user=user, name='default')
            if created:
                device.save()
            qr_code = utils.generate_qr_code(device.config_url)
            request.user.action_verify = True
            request.user.save()

            if request.user.is_staff:
                return render(request, 'admin/setup_2fa.html', {
                    'qr_code': qr_code,
                    'tocken':tocken,
                    "licencia_valida":licencia_vencimiento_valida(request.user),
                })
            else:    
                return render(request, 'panel/setup_2fa.html', {
                    'qr_code': qr_code,
                    'tocken':tocken,
                    "licencia_valida":licencia_vencimiento_valida(request.user),
                })
        return redirect("login")

    @staticmethod
    def Alerta(request,tocken,Error=None,Success=None):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                return redirect("../../../../../../../verificar/")

            tocken = bleach.clean(tocken)
            if tocken != request.user.tocken or tocken=="":
                return render(request,f"panel/index.html",{
                    "Error":"Acceso Denegado",
                    "licencia_valida":licencia_vencimiento_valida(request.user),
                })
            user = request.user
            device, created = TOTPDevice.objects.get_or_create(user=user, name='default')
            if created:
                device.save()
            qr_code = utils.generate_qr_code(device.config_url)
            request.user.action_verify = True
            request.user.save()

            if request.user.is_staff:
                return render(request, 'admin/setup_2fa.html', {
                    'qr_code': qr_code,
                    'tocken':tocken,
                    'Error':Error,
                    "Success":Success,
                    "licencia_valida":licencia_vencimiento_valida(request.user),
                })
            else:    
                return render(request, 'panel/setup_2fa.html', {
                    'qr_code': qr_code,
                    'tocken':tocken,
                    "licencia_valida":licencia_vencimiento_valida(request.user),
                    'Error':Error,
                    "Success":Success,
                    "licencia_valida":licencia_vencimiento_valida(request.user),
                })
        return redirect("login")
        

class DisableMFA(View):
    def get(self, request, tocken):
        if request.user.is_authenticated:
            tocken = bleach.clean(tocken)
            if tocken != request.user.tocken or tocken=="":
                Index.Alerta(request=request,Error="Acceso Denegado")
            user = request.user
            try:
                device = TOTPDevice.objects.get(user=user, name='default')
                device.delete()
                request.user.action_verify = False
                request.user.save()
                if request.user.is_staff:
                    return render(request, 'admin/setup_2fa.html',{
                        'tocken':tocken,
                        "licencia_valida":licencia_vencimiento_valida(request.user),
                        "Success":"Autenticacion multifactor deshabilitada correctamente"
                    })
                else:
                    return render(request, 'panel/setup_2fa.html',{
                        'tocken':tocken,
                        "licencia_valida":licencia_vencimiento_valida(request.user),
                        "Success":"Autenticacion multifactor deshabilitada correctamente"
                    })
            except TOTPDevice.DoesNotExist:
                return render(request, "panel/setup_2fa.html", {
                    "Error": "No se encontró un dispositivo MFA para deshabilitar",
                    'tocken':tocken,
                    "licencia_valida":licencia_vencimiento_valida(request.user),
                })
        else:
            return redirect('login')

class RenewMFA(View):
    def get(self, request, tocken):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                return redirect("../../../../../../../verificar/")
            
            tocken = bleach.clean(tocken)
            if tocken != request.user.tocken or tocken=="":
                return render(request, "panel/index.html", {
                    "Error": "Acceso Denegado",
                    "licencia_valida":licencia_vencimiento_valida(request.user),
                })
            user = request.user
            try:
                device = TOTPDevice.objects.get(user=user, name='default')
                device.delete()
            except TOTPDevice.DoesNotExist:
                pass
            return redirect(f"../../../../../../../../../../mfa/{tocken}/")
        else:
            return redirect('login')

class Verify_2fa(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                return render(request, 'login/verify_2fa.html')
            return redirect("panel")
        return redirect("login")
        
    
    def post(self,request):
        if request.user.is_authenticated:
            if request.user.action_verify and request.user.verify == False:
                print(request.POST)
                tocken =  bleach.clean(str(request.POST.get('tocken')).strip())
                if v2fa(request=request,tocken=tocken):
                    request.user.verify = True
                    request.user.save()
                    return redirect('panel')
                else:
                    return render(request, 'login/verify_2fa.html', {'error': 'Error: Tocken Inválido'})
            return redirect("panel")
        return redirect("login")
    





def v2fa(request,tocken):
    device = TOTPDevice.objects.get(user=request.user, name='default')
    if device.verify_token(tocken):
        return True
    return False









#############################################
############ VISTAS DE LA API ###############
#############################################
class Setup_chanel(View):
    def get(self,request,data):
        data = utils.descifrar_base64_a_dict(data)
        error = ""
        if User.objects.filter(UID=data.get('uid')).exists():
            user = User.objects.get(UID=data.get('uid'))
            try:
                if str(user.public_key) == str(data.get('key')):
                    private_key, public_key = ecc.generate_keys()
                    user.public_key_comunicacion = public_key
                    user.private_key_comunicacion = private_key
                    user.save()
                    data = {
                        'status': 'success',
                        'public_key':utils.cifrar_base64(user.public_key_comunicacion)
                    }
                    return JsonResponse(data, status=200)
            except Exception as e:
                print(e)
                error = str(e)
        data = {
            'status': error
        }
        return JsonResponse(data, status=405)
            




class Update(View):
    def get(self,request,data):
        data = utils.descifrar_base64_a_dict(data)
        error=""
        if not data is None:
            if User.objects.filter(UID=data.get('uid')).exists():
                try:
                    user = User.objects.get(UID=data.get('uid'))
                    if ecc.verify_signature(data.get('data'), data.get("sign"), user.public_key):
                        data = data.get('data')
                        data = utils.descifrar_base64(data)
                        data = ecc.decrypt_message(user.private_key_comunicacion, data)
        
                        data = utils.descifrar_base64_a_dict(data)
                        
                        valor = data.get('valor')
                        numero_analisis = data.get('numero_analisis')
                        
                        if not models.dataset.objects.filter(numero_analisis=numero_analisis).exists():
                            new_data = models.dataset(numero_analisis=numero_analisis,valor_actual=valor)
                            new_data.save()
                        data = {
                            'status': 'success'
                        }
                        return JsonResponse(data, status=200)
                except Exception as e:
                    error = str(e)
                    print(error)
        data = {
            'status': error
        }
        return JsonResponse(data, status=405)






class update_text_code(View):
    def get(self,request,data):
        data = utils.descifrar_base64_a_dict(data)
        error=""
        if not data is None:
            if User.objects.filter(UID=data.get('uid')).exists():
                try:
                    user = User.objects.get(UID=data.get('uid'))
                    if ecc.verify_signature(data.get('data'), data.get("sign"), user.public_key):
                        data = data.get('data')
                        data = utils.descifrar_base64(data)
                        data = ecc.decrypt_message(user.private_key_comunicacion, data)
                        data = utils.descifrar_base64_a_dict(data)
                        if not data is None:
                            mensaje = data.get('mensaje')
                            if models.Metadata.objects.filter(key="text_code").exists():
                                k = models.Metadata.objects.get(key="text_code")
                                k.texto = mensaje
                                k.save()
                            else:
                                k = models.Metadata(key="text_code",texto=mensaje)
                                k.save()
                            data = {
                                'status': 'success'
                            }
                            return JsonResponse(data, status=200)
                except Exception as e:
                    error = str(e)
                    print(error)
        data = {
            'status': error
        }
        return JsonResponse(data, status=405)


class update_test_predictions(View):
    def get(self,request,data):
        data = utils.descifrar_base64_a_dict(data)
        error=""
        if not data is None:
            if User.objects.filter(UID=data.get('uid')).exists():
                try:
                    user = User.objects.get(UID=data.get('uid'))
                    if ecc.verify_signature(data.get('data'), data.get("sign"), user.public_key):
                        data = data.get('data')
                        data = utils.descifrar_base64(data)
                        data = ecc.decrypt_message(user.private_key_comunicacion, data)
                        data = utils.descifrar_base64_a_dict(data)
                        if not data is None:
                            prediction = float(data.get("prediction"))
                            current_price = float(data.get("current_price"))
                            predict_step = float(data.get("predict_step"))
                            analisis = int(data.get('analisis'))

                            new_prediction = models.Prediccion(prediccion=prediction,analisis=analisis)
                            new_prediction.save()
                            last_prediction = new_prediction.id - predict_step
                            if models.Prediccion.objects.filter(id = last_prediction).exists():
                                lp = models.Prediccion.objects.get(id = last_prediction)
                                lp.real = current_price
                                lp.save()
                            data = {
                                'status': 'success'
                            }
                            return JsonResponse(data, status=200)
                except Exception as e:
                    error = str(e)
                    print(error)
        data = {
            'status': error
        }
        return JsonResponse(data, status=405)
                            


class reset(View):
    def post(self, request):
        if request.user.is_authenticated:
            data = models.dataset.objects.all()
            for k in data:
                k.delete()
            try:
                text_code = models.Metadata.objects.get(key="text_code")
                text_code.delete()
            except Exception:
                pass
            data = models.Prediccion.objects.all()
            for k in data:
                k.delete()
        return redirect("panel")



