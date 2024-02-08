from django.urls import path, include
from . import views

app_name = 'Stat'

urlpatterns = [
    path('correctRateUpdate', views.correctRateUpdate),
    # path('pieGraph', views.pieGraph),
    path('correctRate', views.correctRate),
]
