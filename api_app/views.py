from typing import Callable, Any
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpRequest, JsonResponse
from django.views.generic import View
from client_app.schemas import (
    ClientSchemaIncoming,
    PinSchema,
    ClientCredentialSchema,
    TokenSchema,
)
from catalog_app.schemas import GoodListSchema
from order_app.schemas import OrderStatusListUpdateSchemaIncoming
from api_app.schemas import DataSchema
from services import (
    good_service,
    client_service,
    region_service,
    price_service,
    order_service,
    property_service,
)


def check_token(view_function: Callable) -> Callable:
    def wrapper(obj: Any, request: HttpRequest) -> JsonResponse:
        token = client_service.extract_token(request)
        client_service.check_token(token)
        return view_function(obj, request)

    return wrapper


@method_decorator(csrf_exempt, name="dispatch")
class PinView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        client_schema = ClientSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        pin = client_service.fetch_pin_by_client(client_schema)
        return JsonResponse(PinSchema(pin=pin).model_dump(), status=200)


@method_decorator(csrf_exempt, name="dispatch")
class TokenView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        credential = ClientCredentialSchema.model_validate_json(
            request.body.decode("utf-8")
        )
        token = client_service.fetch_token_by_credentials(credential)
        response = JsonResponse(TokenSchema(token=token).model_dump(), status=200)
        response.set_cookie("Authorization", token)
        return response


@method_decorator(csrf_exempt, name="dispatch")
class GoodView(View):
    @check_token
    def post(self, request: HttpRequest) -> JsonResponse:
        goods = GoodListSchema.model_validate_json(request.body.decode("utf-8"))
        return JsonResponse(goods.model_dump(), status=200)

    @check_token
    def get(self, request: HttpRequest) -> JsonResponse:
        goods = good_service.fetch_all_goods()
        return JsonResponse(goods.model_dump(), status=200)


@method_decorator(csrf_exempt, name="dispatch")
class DataView(View):
    @check_token
    def post(self, request: HttpRequest) -> JsonResponse:
        data = DataSchema.model_validate_json(request.body.decode("utf-8"))
        good_service.create_or_update_goods(data.goods)
        property_service.create_properties(data.properties)
        region_service.create_or_update_regions(data.regions)
        price_service.create_or_update_price(data.prices)
        order_service.create_or_update_statuses(data.order_statuses)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class NewOrderView(View):
    @check_token
    def get(self, request: HttpRequest) -> JsonResponse:
        new_orders = order_service.fetch_new_orders()
        return JsonResponse(new_orders.model_dump(), status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UpdateOrderStatusView(View):
    @check_token
    def post(self, request: HttpRequest) -> JsonResponse:
        data = OrderStatusListUpdateSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        order_service.update_order_statuses(data)
        return JsonResponse({}, status=200)
