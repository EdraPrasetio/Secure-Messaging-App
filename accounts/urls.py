from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('del_user', views.del_user, name='del_user'),
    path('register', views.register, name='register'),
    path('registration_successful', views.registration_successful, name='registration_successful')
]