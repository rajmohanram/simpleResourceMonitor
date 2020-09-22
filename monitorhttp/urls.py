from django.urls import path, include
from . import views


urlpatterns = [
    path('endpoints/', views.endpoints, name='monitorhttp.endpoints'),
    path('get-endpoint/', views.get_endpoint, name='monitorhttp.get-endpoint'),
    path('get-endpoints/', views.get_endpoints, name='monitorhttp.get-endpoints'),
    path('del-endpoint/', views.del_endpoint, name='monitorhttp.del-endpoint'),
    path('endpoints-status/', views.endpoints_status, name='monitorhttp.status'),
]