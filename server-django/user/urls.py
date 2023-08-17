from django.urls import include, path
from user import views


urlpatterns = [
    path(r'searchUser/', views.searchUser),
]
