from django.urls import path, include
from . import views

app_name = 'Stat'

urlpatterns = [
    path('correctRateUpdate', views.correctRateUpdate),
    path('correctRate', views.correctRate),
    # path('pieGraph', views.pieGraph),
]
