"""
URL configuration for tempfacetrace project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.register, name='Register'),
    path('admindashboard/', views.adminDashboard, name='AdminDashboard'),
    path('login/', views.loginuser, name='Login'),
    path('register/', views.register, name='Register'),
    path('logout/', views.logoutuser, name='Logout'),
    path('student/', views.student, name='Student'),
    path('profile/', views.profile, name='Profile'),
    path('queries/', views.queries, name='Queries'),
    path('send-query/', views.sendQuery, name='SendQuery'),
    path('get-data/', views.get_data, name='get_data'),
    path('user-is-valid/', views.userIsValid, name='UserIsValid'),
    path("__reload__/", include("django_browser_reload.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
