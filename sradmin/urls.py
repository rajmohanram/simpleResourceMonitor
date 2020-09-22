from django.urls import path, include
from . import views


urlpatterns = [
    path('auth/', views.authenticate_user, name='srm.auth'),
    path('chpasswd/', views.change_password, name='srm.chpasswd'),
    path('logout/', views.logout_user, name='srm.logout'),
    path('get-interval/', views.get_monitoring_interval, name='srm.monitorInterval'),
    path('upd-interval/', views.upd_monitoring_interval, name='srm.updInterval'),
    path('user-mgmt/', views.users, name='srm.usermgmt'),
    path('user-del/', views.del_user, name='srm.delUser'),
    path('user-upd/', views.upd_user, name='srm.updUser'),
]