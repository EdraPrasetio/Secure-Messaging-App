from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('conversation', views.conversation, name='conversation'),
    path('conversation/send', views.send_to_conversation, name='send')
]
