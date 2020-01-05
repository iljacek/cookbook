from django.urls import path

from . import views

app_name = 'recipes'
urlpatterns = [
    path('<int:site>/get_data/', views.get_from_url, name='get_data'),
    path('new_data/', views.new_recipe, name='new_data'),
    path('data_from_url/', views.new_from_url, name='data_from_url'),
    path('<int:recipe>/new_step/', views.new_step, name='new_step'),
]