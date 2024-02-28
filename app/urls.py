from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('service',views.service, name='service'),
    path('add_participant',views.add_participant, name='add_participant'),
    path('list_participant',views.list_participant, name='list_participant'),
    path('attendance_view',views.attendance_view,name='attendance_view'),
    path('attendance_list',views.attendance_list,name='attendance_list'),
    path('add_membership_purchase',views.add_membership_purchase,name='add_membership_purchase'),
    path('membership_purchase_list',views.membership_purchase_list,name='membership_purchase_list'),
]
