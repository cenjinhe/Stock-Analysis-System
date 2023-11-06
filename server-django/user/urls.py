from django.urls import include, path
from user import views


urlpatterns = [
    path(r'login/', views.login),
    path(r'userinfo/', views.userinfo),
    path(r'menus/', views.menus),
]
