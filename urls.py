from django.urls import path
from . import views
urlpatterns= [
    path('',views.home),
    path('about/',views.about),
    path('login/',views.login,name='login'),
    path('base/',views.base),
    path('reg/',views.reg,name='reg'),
    path('contact/',views.contact),
    path('services/',views.service),
    path('rules/',views.rules),
    path('user',views.user,name='user'),
    path('logout/',views.logout,name='logout'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('forgotPassword/', views.forgotPassword, name='forgotPassword'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('librarian/',views.librarian,name='librarian'),
    path('display',views.display,name='display'),
    path('bookdisplay',views.bookdisplay,name='bookdisplay'),
    path('add/',views.add,name='add'),
    path('<int:bk_id>',views.view,name='view'),
    path('edit/<int:bk_id>/', views.edit, name='edit'),
    path('delete/<int:bk_id>/', views.delete, name='delete'),
]



