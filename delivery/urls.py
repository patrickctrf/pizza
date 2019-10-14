from django.urls import path

from . import views

app_name = 'delivery'

urlpatterns = [
    path('', views.index, name='index'),
    path('login_forms', views.login_forms, name='login_forms'),
    path('logup_forms', views.logup_forms, name='logup_forms'),
    path('logup', views.logup, name='logup'),
    path('menu', views.menu, name='menu'),
    path('menu_forms', views.menu_forms, name='menu_forms'),
    path('basket_forms', views.basket_forms, name='basket_forms'),
    path('final', views.final, name='final'),
    path('disconnectlogout', views.disconnectlogout, name='disconnectlogout'),
]
