from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpRequest, JsonResponse
from django.views.generic import View
from client_app.schemas import (
    ClientSchema,
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
)


@method_decorator(csrf_exempt, name="dispatch")
class PinView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        client_schema = ClientSchema.model_validate_json(request.body.decode("utf-8"))
        pin = client_service.fetch_pin_by_client(client_schema)
        return JsonResponse(PinSchema(pin=pin).model_dump())


@method_decorator(csrf_exempt, name="dispatch")
class TokenView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        credential = ClientCredentialSchema.model_validate_json(
            request.body.decode("utf-8")
        )
        token = client_service.fetch_token_by_credentials(credential)
        response = JsonResponse(TokenSchema(token=token).model_dump())
        response.set_cookie("Authorization", token)
        return response


@method_decorator(csrf_exempt, name="dispatch")
class GoodView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        token = client_service.extract_token(request)
        client_service.check_token(token)
        goods = GoodListSchema.model_validate_json(request.body.decode("utf-8"))
        return JsonResponse(goods.model_dump())

    def get(self, request: HttpRequest) -> JsonResponse:
        token = client_service.extract_token(request)
        client_service.check_token(token)
        goods = good_service.fetch_all_goods_as_schema()
        return JsonResponse(goods.model_dump())


@method_decorator(csrf_exempt, name="dispatch")
class DataView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        token = client_service.extract_token(request)
        client_service.check_token(token)
        data = DataSchema.model_validate_json(request.body.decode("utf-8"))
        good_service.create_or_update_goods(data.goods)
        region_service.create_or_update_regions(data.regions)
        price_service.create_or_update_price(data.prices)
        order_service.create_or_update_statuses(data.order_statuses)
        return JsonResponse(data.model_dump())


@method_decorator(csrf_exempt, name="dispatch")
class NewOrderView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        token = client_service.extract_token(request)
        client_service.check_token(token)
        new_orders = order_service.fetch_new_orders()
        return JsonResponse(new_orders.model_dump())


@method_decorator(csrf_exempt, name="dispatch")
class UpdateOrderStatusView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        token = client_service.extract_token(request)
        client_service.check_token(token)
        data = OrderStatusListUpdateSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        order_service.update_order_statuses(data)
        return JsonResponse(data=None)
