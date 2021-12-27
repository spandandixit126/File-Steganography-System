from django.urls import path
from . import views

urlpatterns = [
    path('group_chat', views.group_chat, name='group_chat'),
    path('private_chat', views.private_chat, name='private_chat'),
    path('send', views.send, name='send'),
    path('data_fetching', views.data_fetching, name='data_fetching'),
    path('get_messages_company/<str:comp_name>/', views.get_messages_company, name='get_messages_company'),
]