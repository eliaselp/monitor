from django.shortcuts import render,redirect
from django.views import View
from django.http import JsonResponse
from django.middleware.csrf import get_token
# Create your views here.

from . import models

class Index(View):
    def get(self,request):
        text_code = None
        try:
            if not models.Metadata.objects.filter(key="text_code").exists():
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
        return render(request,"index.html",{
            "text_code":text_code,
            'data_set_balance':objetos
        })



import base64
import json

def descifrar_base64_a_dict(base64_str):
    try:
        # Decodificar la cadena base64
        json_str = base64.b64decode(base64_str).decode('utf-8')
        # Convertir la cadena JSON a un diccionario
        data_dict = json.loads(json_str)
        return data_dict
    except Exception as e:
        return None




class Update(View):
    def get(self,request,data):
        data = descifrar_base64_a_dict(data)
        if not data is None:
            key = data.get('key')
            error = None
            if key == "oGcEDduv9MsuMuNRH5cwmVrij7CSL2IOnjXHxsYNmuEueqA7tifnNFbgrasZMxHqMeePZ7X88h+v9emtVOHyXqk06OVsPDL4S2LyX3YZyJvz6QAT542qXgIHG8+LUeA9MPYugXpliMhqt0vI1dr0UebYMkKlWc5E4koQ75bGp14xo4G9IkAkqWUT53fAqip+ApPItf8TpViND6xP3LeBNIEVmkiWfLU5Vx3wIDAQABAoIBAHJ42ntgTHPlDUDK98uclew8scNUv8DapNajwKCpbQHZ657V6r+OHPfUe3M6wB3aiHU3+0ZvOhYBJPVhY3BYH8SKrPq4DKoSAgonSt5G5u4UiAsxxP8FqFd8dYzJzbikk5BDLyKHb5WLl0seqw7RQffwl3FGmpaU5gCTvBtGsyAGaPRaSJMUBdUQUFqBPWfXkfyfqy4fJ2rTNxJtmynToYcuJpRCBdir3+P8mHwQrSq33caiBCmgbwds5tRe8vwcDi4b+8RQmQbQyOj2bJMxHGF8rQVpHEJtPAfv4aeDpOF3PPo1KdYBmD0n43hSwy2UdiFX9sk3FSEdl8ECgYEA0DTN2cGaNv9ftBa3KgtorfQmjrb4iWd8a+a2u8ut5q9n9uE7wc4st1mJJGME8B39ERlbW6v5sXAxeMPYTOyVJlh5z+keR9tmszhnZpZ5mED+oI67J2oZJboPXLpvsgcG6WoX0OgkgHwhhzYNj0jgZ37AAXYWuAQGxvfeRnBECgYEAv7eT4qnQwa4FZ1XEel+LgxcjlQfJAwTXJQYnrx8j0cTftB0EiwDZBHvCiBdF+oKlntDK59fgVOWubfAunO2Be34GR8SiQbagENfGWu0pa9qGKy+jmmjmciJqv+wYIf3qqxuN6izefuFmMPQBb29dzp0sanfjUCAu55u3u8CgYEAoYfmEMQ4PeUAvfpFnpP9":
                try:
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
        data = descifrar_base64_a_dict(data)
        if not data is None:
            key = data.get('key')
            error = None
            if key == "oGcEDduv9MsuMuNRH5cwmVrij7CSL2IOnjXHxsYNmuEueqA7tifnNFbgrasZMxHqMeePZ7X88h+v9emtVOHyXqk06OVsPDL4S2LyX3YZyJvz6QAT542qXgIHG8+LUeA9MPYugXpliMhqt0vI1dr0UebYMkKlWc5E4koQ75bGp14xo4G9IkAkqWUT53fAqip+ApPItf8TpViND6xP3LeBNIEVmkiWfLU5Vx3wIDAQABAoIBAHJ42ntgTHPlDUDK98uclew8scNUv8DapNajwKCpbQHZ657V6r+OHPfUe3M6wB3aiHU3+0ZvOhYBJPVhY3BYH8SKrPq4DKoSAgonSt5G5u4UiAsxxP8FqFd8dYzJzbikk5BDLyKHb5WLl0seqw7RQffwl3FGmpaU5gCTvBtGsyAGaPRaSJMUBdUQUFqBPWfXkfyfqy4fJ2rTNxJtmynToYcuJpRCBdir3+P8mHwQrSq33caiBCmgbwds5tRe8vwcDi4b+8RQmQbQyOj2bJMxHGF8rQVpHEJtPAfv4aeDpOF3PPo1KdYBmD0n43hSwy2UdiFX9sk3FSEdl8ECgYEA0DTN2cGaNv9ftBa3KgtorfQmjrb4iWd8a+a2u8ut5q9n9uE7wc4st1mJJGME8B39ERlbW6v5sXAxeMPYTOyVJlh5z+keR9tmszhnZpZ5mED+oI67J2oZJboPXLpvsgcG6WoX0OgkgHwhhzYNj0jgZ37AAXYWuAQGxvfeRnBECgYEAv7eT4qnQwa4FZ1XEel+LgxcjlQfJAwTXJQYnrx8j0cTftB0EiwDZBHvCiBdF+oKlntDK59fgVOWubfAunO2Be34GR8SiQbagENfGWu0pa9qGKy+jmmjmciJqv+wYIf3qqxuN6izefuFmMPQBb29dzp0sanfjUCAu55u3u8CgYEAoYfmEMQ4PeUAvfpFnpP9":
                try:
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


class reset(View):
    def post(self, request):
        key = request.POST.get('key')
        if key == "oGcEDduv9MsuMuNRH5cwmVrij7CSL2IOnjXHxsYNmuEueqA7tifnNFbgrasZMxHqMeePZ7X88h+v9emtVOHyXqk06OVsPDL4S2LyX3YZyJvz6QAT542qXgIHG8+LUeA9MPYugXpliMhqt0vI1dr0UebYMkKlWc5E4koQ75bGp14xo4G9IkAkqWUT53fAqip+ApPItf8TpViND6xP3LeBNIEVmkiWfLU5Vx3wIDAQABAoIBAHJ42ntgTHPlDUDK98uclew8scNUv8DapNajwKCpbQHZ657V6r+OHPfUe3M6wB3aiHU3+0ZvOhYBJPVhY3BYH8SKrPq4DKoSAgonSt5G5u4UiAsxxP8FqFd8dYzJzbikk5BDLyKHb5WLl0seqw7RQffwl3FGmpaU5gCTvBtGsyAGaPRaSJMUBdUQUFqBPWfXkfyfqy4fJ2rTNxJtmynToYcuJpRCBdir3+P8mHwQrSq33caiBCmgbwds5tRe8vwcDi4b+8RQmQbQyOj2bJMxHGF8rQVpHEJtPAfv4aeDpOF3PPo1KdYBmD0n43hSwy2UdiFX9sk3FSEdl8ECgYEA0DTN2cGaNv9ftBa3KgtorfQmjrb4iWd8a+a2u8ut5q9n9uE7wc4st1mJJGME8B39ERlbW6v5sXAxeMPYTOyVJlh5z+keR9tmszhnZpZ5mED+oI67J2oZJboPXLpvsgcG6WoX0OgkgHwhhzYNj0jgZ37AAXYWuAQGxvfeRnBECgYEAv7eT4qnQwa4FZ1XEel+LgxcjlQfJAwTXJQYnrx8j0cTftB0EiwDZBHvCiBdF+oKlntDK59fgVOWubfAunO2Be34GR8SiQbagENfGWu0pa9qGKy+jmmjmciJqv+wYIf3qqxuN6izefuFmMPQBb29dzp0sanfjUCAu55u3u8CgYEAoYfmEMQ4PeUAvfpFnpP9":
            data = models.dataset.objects.all()
            for k in data:
                k.delete()
            try:
                text_code = models.Metadata.objects.get(key="text_code")
                text_code.delete()
            except Exception:
                pass
        return redirect("../../../../../../../../../../../../../../../")



