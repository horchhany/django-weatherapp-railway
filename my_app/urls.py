from django.urls import path
from . import views

urlpatterns = [
    path(route='', view=views.home, name='home'),
    path(route='products/', view=views.items_pro, name='products'),
    path(route='update_clear/<weather_id>/', view=views.update_clear, name='update_clear'),
]

'''
    localhost:8000/myapp/home
    localhost:8000/myapp/products

'''