from django.urls import path
from django.views.generic import TemplateView
from .views import *

app_name = 'apps.blog_auth'

urlpatterns = [
    path('registro',registro, name='registro'),
    path('login', auth_views.LoginView.as_view(template_name='registration/login.html'), 
         name='login'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('registrocompletado', TemplateView.as_view(
        template_name = 'registration/registrocompleto.html'),
        name='registrocompleto')
    #path('login', login_view, name='login')
]