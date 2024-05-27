from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.register,name='register'),
    path('login/',views.login_f,name='login'),
    path('add_employee/',views.add_employee,name='add_employee'),
    
]