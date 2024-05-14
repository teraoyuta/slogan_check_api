from django.urls import path
from . import views

urlpatterns = [
    path('get_kana_from_slogan/', views.get_kana_from_slogan, name='get_kana_from_slogan'),
    path('check_slogan/', views.check_slogan, name='check_slogan'),
    path('save_slogan/', views.save_slogan, name='save_slogan'),
    path('delete_slogan/', views.delete_slogan, name='delete_slogan'),
    path('get_slogan_list/', views.get_slogan_list, name='get_slogan_list')
]
