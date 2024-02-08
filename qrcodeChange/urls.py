from django.urls import path, include
from . import views


urlpatterns = [
    # ... 기존의 url 패턴들 ...
    path('qrcode', views.generate_qrcode),
]
