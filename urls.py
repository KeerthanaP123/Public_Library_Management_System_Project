from django.urls import path
from . import views
urlpatterns= [
    path('',views.home),
    path('about/',views.about),
    path('login/',views.login),
    path('base/',views.base),
    path(r'reg/',views.reg),
    path('contact/',views.contact),
    path('services/',views.service),
    path('rules/',views.rules)
]