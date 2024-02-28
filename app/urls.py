from django.urls import path
from .views import *

urlpatterns = [
    path("",home,name="home"),
    path("home",home,name="home"),
    path("inv",inv,name="inven"),
    path("deli",deli,name="deli"),
    path("dashboard",dashboard,name="dashboard"),
    path("reg",reg,name="reg"),
    path("log",log,name="log"),
    path("logout",logout,name="logout"),
    path("request",req,name="req"),
    path("additem",additem,name="additem"),
    path("profile",profile,name="profile"),
    path("increasestock",increasestock,name="increasestock"),
    path("deliver/<int:pk>",deliver,name="deliver"),
]