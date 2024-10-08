
from django.contrib import admin
from django.urls import path,include
from App import views
urlpatterns = [
    path('admin/',include("admins.urls")),


    path('login/',views.Login.as_view(),name="login"),
    path('register/',views.Register.as_view(),name="register"),
    path('',views.Index.as_view(),name="panel"),
    path('reset_data/',views.reset.as_view(),name="reset_data"),
    path('logout/',views.Logout,name="logout"),
    path('validar_mail/<str:uid>/<str:tocken>/',views.Validar_Mail.as_view(),name="validar_mail"),
    path('verificar/',views.Verify_2fa.as_view(),name="verificar_2fa"),
    path('verificar_mail/<int:opc>/',views.backend_verificacion_email.as_view()),
    path('mfa/<str:tocken>/',views.MFA.as_view(),name="mfa"),
    path('disablemfa/<str:tocken>/',views.DisableMFA.as_view(),name="disablemfa"),
    path('renewmfa/<str:tocken>/',views.RenewMFA.as_view(),name="renewmfa"),


    #path('api/',views.Api.as_view(),name="api"),


    ##url de api
    path('setup_chanel/<str:data>/',views.Setup_chanel.as_view()),


    path('update/<str:data>/',views.Update.as_view()),
    path('update_text_code/<str:data>/',views.update_text_code.as_view()),
    path('update_test_predictions/<str:data>/',views.update_test_predictions.as_view()),


]
