from typing import Callable, Any
import logging
from django.core.exceptions import PermissionDenied
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpRequest, JsonResponse
from django.views.generic import View
from client_app.schemas import (
    ClientSchemaIncoming,
    ClientCredentialSchema,
    TokenSchema,
    RequestSchemaIncoming,
    FeedbackSchemaIncoming,
)
from catalog_app.schemas import GoodListSchemaIncoming
from client_app.models import Client
from order_app.schemas import (
    OrderStatusListUpdateSchemaIncoming,
    AddCartItemSchemaIncoming,
)
from api_app.schemas import DataSchema
from services import (
    good_service,
    client_service,
    region_service,
    price_service,
    order_service,
    property_service,
    sms_service,
)

logger = logging.getLogger(__name__)


def auth(only: bool = True) -> Callable:
    def out_wrapper(view_function: Callable) -> Callable:
        def in_wrapper(
            obj: Any, request: HttpRequest, **kwargs: dict[str, Any]
        ) -> JsonResponse:
            token = client_service.extract_token(request)
            client = client_service.client_by_token(token)
            if only and client is None:
                raise PermissionDenied("bad Auth token")
            return view_function(obj, request, client, **kwargs)

        return in_wrapper

    return out_wrapper


@method_decorator(csrf_exempt, name="dispatch")
class PinView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        client_schema = ClientSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        pin = client_service.fetch_pin_by_client(client_schema)
        if pin:
            message = f"Добро пожаловать на goodcup.ru! Ваш код доступа {pin}"
            sms_service.send_pin_by_sms("goodcup.ru", message, client_schema.name)
            return JsonResponse({}, status=200)
        return JsonResponse({}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class TokenView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        credential = ClientCredentialSchema.model_validate_json(
            request.body.decode("utf-8")
        )
        token = client_service.fetch_token_by_credentials(credential)
        if not token:
            raise PermissionDenied("bad name or pin")
        response = JsonResponse(TokenSchema(token=token).model_dump(), status=200)
        response.set_cookie("Authorization", token)
        return response


@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):
    def get(self, request: HttpRequest, slug: str = "") -> JsonResponse:
        if slug:
            category = good_service.fetch_category_by_slug(slug)
            return JsonResponse(category.model_dump(), status=200)
        categories = good_service.fetch_all_categories()
        return JsonResponse(categories.model_dump(), status=200)


@method_decorator(csrf_exempt, name="dispatch")
class GoodView(View):
    @auth()
    def post(self, request: HttpRequest, client: Client) -> JsonResponse:
        goods = GoodListSchemaIncoming.model_validate_json(request.body.decode("utf-8"))
        return JsonResponse(goods.model_dump(), status=200)

    @auth(False)
    def get(self, request: HttpRequest, client: Client, slug: str = "") -> JsonResponse:
        region = client.region if client else None
        page_number = request.GET.get("page", 0)
        if slug:
            good = good_service.fetch_good_by_slug(slug, region)
            if good:
                return JsonResponse(good.model_dump(), status=200)
            return JsonResponse({}, status=400)
        search = request.GET.get("search")
        if search:
            goods = good_service.search_goods(search, region, page_number)
            return JsonResponse(goods.model_dump(), status=200)
        category_slug = request.GET.get("category")
        if category_slug:
            goods = good_service.fetch_good_by_category(
                category_slug, region, page_number
            )
            return JsonResponse(goods.model_dump(), status=200)
        goods = good_service.fetch_all_goods(region, page_number)
        return JsonResponse(goods.model_dump(), status=200)


@method_decorator(csrf_exempt, name="dispatch")
class DataView(View):
    @auth()
    def post(self, request: HttpRequest, client: Client) -> JsonResponse:
        data = DataSchema.model_validate_json(request.body.decode("utf-8"))
        good_service.create_or_update_goods(data.goods)
        property_service.create_properties(data.properties)
        region_service.create_or_update_regions(data.regions)
        price_service.create_or_update_price(data.prices)
        order_service.create_or_update_statuses(data.order_statuses)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class NewOrderView(View):
    @auth()
    def get(self, request: HttpRequest, client: Client) -> JsonResponse:
        new_orders = order_service.fetch_new_orders()
        return JsonResponse(new_orders.model_dump(), status=200)


@method_decorator(csrf_exempt, name="dispatch")
class UpdateOrderStatusView(View):
    @auth()
    def post(self, request: HttpRequest, client: Client) -> JsonResponse:
        data = OrderStatusListUpdateSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        order_service.update_order_statuses(data)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CartView(View):
    @auth()
    def get(self, request: HttpRequest, client: Client) -> JsonResponse:
        items = order_service.fetch_cart_items(client)
        return JsonResponse(items.model_dump(), status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CartSetView(View):
    @auth()
    def post(self, request: HttpRequest, client: Client) -> JsonResponse:
        data = AddCartItemSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        order_service.set_item_to_cart(data, client)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CartDeleteView(View):
    @auth()
    def post(self, request: HttpRequest, client: Client) -> JsonResponse:
        data = AddCartItemSchemaIncoming.model_validate_json(
            request.body.decode("utf-8")
        )
        order_service.drop_item_from_cart(data, client)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CartClearView(View):
    @auth()
    def get(self, request: HttpRequest, client: Client) -> JsonResponse:
        order_service.clear_cart(client)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class RequestView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        data = RequestSchemaIncoming.model_validate_json(request.body.decode("utf-8"))
        logger.info({"request_data": data})
        client_service.process_incoming_request(request=data)
        return JsonResponse({}, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class FeedbackView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        data = FeedbackSchemaIncoming.model_validate_json(request.body.decode("utf-8"))
        logger.info({"feedback_data": data})
        client_service.process_feedback(feedback=data)
        return JsonResponse({}, status=200)
