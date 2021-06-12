from django.urls import path
from . import views


urlpatterns = [
    path('callback/', views.callback, name='callback'), # add this line
    path('updatedb/', views.updatedb, name='updatedb'), # send request to view for update data to db
    path('permission_check/', views.permission_check, name='permission_check'), # send request to view for update data to db
    
]