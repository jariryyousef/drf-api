from django.urls import path
from .views import CarList, CarDetail


urlpatterns = [
        path('',CarList.as_view(), name = 'car_list'),
        path('<int:pk>/',CarDetail.as_view(), name = 'car_detail'),

]