from django.urls import include, path
from . import views

app_name='home'
urlpatterns = [
    path('', views.index, name='home'),
    # path('getdata/', views.index, name='getdata'),
    # path('', views.leagueform, name='leagueform'),
    # path('getdata/', views.leagueform, name='getdata')
    path('test/', views.testview, name='testview'),
    path('tasty/', views.tastyview, name='tasty'),
]
