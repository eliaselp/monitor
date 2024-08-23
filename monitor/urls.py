
from django.contrib import admin
from django.urls import path
from App import views
urlpatterns = [
    #path('admin/', admin.site.urls),
    path('',views.Index.as_view()),
    path('update/<str:data>/',views.Update.as_view()),
    path('update_text_code/<str:data>/',views.update_text_code.as_view()),
    path('reset_data/',views.reset.as_view()),
]
