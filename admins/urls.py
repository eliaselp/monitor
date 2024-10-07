
from django.contrib import admin
from django.urls import path
from App import views
from . import views as local_views
urlpatterns = [
    path('',local_views.Index.as_view(),name="admin_panel"),
    path('licencias/',local_views.Licencias.as_view(),name="licencias"),
    path('eliminar_licencia/<str:uid>/',local_views.Eliminar_licencia.as_view(),name="eliminar_licencia"),
]


'''
    path('reset_data/',views.reset.as_view(),name="reset_data"),
    path('logout/',views.Logout,name="logout"),
    
    path('verificar/',views.Verify_2fa.as_view(),name="verificar_2fa"),
    path('verificar_mail/<int:opc>/',views.backend_verificacion_email.as_view()),
    path('mfa/<str:tocken>/',views.MFA.as_view()),
    path('disablemfa/<str:tocken>/',views.DisableMFA.as_view(),name="disablemfa"),
    path('renewmfa/<str:tocken>/',views.RenewMFA.as_view(),name="renewmfa"),


    path('api/',views.Api.as_view(),name="api"),


    ##url de api
    path('update/<str:data>/',views.Update.as_view()),
    path('update_text_code/<str:data>/',views.update_text_code.as_view()),
'''
