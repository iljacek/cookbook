"""Cookbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from recipes.views import home
from chef.views import SignUp

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('recipes/', include('recipes.urls')),
    path('login/', LoginView.as_view(template_name="Cookbook/login_form.html"), name="player_login"),
    path('logout/', LogoutView.as_view(), name="player_logout"),
    path('signup/', SignUp.as_view(), name="signup"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
