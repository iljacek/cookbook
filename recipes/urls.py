from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'recipes'
urlpatterns = [
    path('show_recipe/<int:recipe>', views.show_recipe, name='show_recipe'),
    path('new_data/', views.new_recipe, name='new_data'),
    path('data_from_url/', views.new_from_url, name='data_from_url'),
    path('remove_recipe/<int:recipe>/', views.remove_recipe, name='remove_recipe'),
    path('edit_recipe/<int:recipe>/', views.edit_recipe, name='edit_recipe'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
