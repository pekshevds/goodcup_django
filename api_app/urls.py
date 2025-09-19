from django.urls import path
from api_app.views import PinView, TokenView, GoodView, DataView

app_name = "api_app"

urlpatterns = [
    path("v1/pin/", PinView.as_view()),
    path("v1/token/", TokenView.as_view()),
    path("v1/good/", GoodView.as_view()),
    path("v1/data/", DataView.as_view()),
]
