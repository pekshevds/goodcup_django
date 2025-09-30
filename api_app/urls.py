from django.urls import path
from api_app.views import (
    PinView,
    TokenView,
    GoodView,
    DataView,
    NewOrderView,
    UpdateOrderStatusView,
)

app_name = "api_app"

urlpatterns = [
    path("v1/pin/", PinView.as_view()),
    path("v1/token/", TokenView.as_view()),
    path("v1/good/", GoodView.as_view()),
    path("v1/good/<str:slug>/", GoodView.as_view()),
    path("v1/data/", DataView.as_view()),
    path("v1/orders/get-new/", NewOrderView.as_view()),
    path("v1/orders/update-statuses/", UpdateOrderStatusView.as_view()),
]
