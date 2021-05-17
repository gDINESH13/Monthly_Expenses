from django.urls import path
from . import views

urlpatterns=[
    path('index',views.index,name="index"),
    path('piechart/<str:date>/<int:totalIncome>/<int:totalExpense>', views.piechart, name='piechart'),
    path('',views.login_view,name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register',views.register,name="register"),
    path('details',views.details_tab,name='details'),

]