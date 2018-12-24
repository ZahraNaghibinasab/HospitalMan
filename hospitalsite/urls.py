from django.urls import path
from hospitalsite import views

urlpatterns = [
    # path('', views.hospital, name='hospital'),
    path('', views.login, name='login'),
    path('signin/',views.signin, name='signin'),
    path('success/',views.success, name='success'),
]