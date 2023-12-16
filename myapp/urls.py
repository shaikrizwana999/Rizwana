from django.urls import path
from myapp.views import *
app_name='myapp'

urlpatterns = [
 path('',index,name='index'),
 path('login/',login,name='login'),
 path('about/',about,name='about'),
 path('contactus/',contact,name='contact'),
 path('register/',register,name='register'),
 path('detail/',detail,name='detail'),
 path('searchtrain/',search,name="search"),
 path('pnr/', pnr, name='pnr'), 
 path('canceltrain/',cancel,name="cancel"),
 path('logout/',logout,name="logout"),
 path('bookticket/',book,name="book"),
 path('otp/<str:otp>/<str:username>/<str:password>/<str:email>/',otp, name='otp'),

]