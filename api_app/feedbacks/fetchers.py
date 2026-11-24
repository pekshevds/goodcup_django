import asyncio
from datetime import datetime

import httpx
from asgiref.sync import async_to_sync
from django.conf import settings

from api_app.feedbacks.schemas import Feedback, FeedbackParam, Feedbacks


async def fetch_feedbacks_from_wb(nmId: int, take: int = 10) -> Feedbacks:
    result: list[Feedback] = []
    uri = f"https://feedbacks-api.wildberries.ru/api/v1/feedbacks?isAnswered=true&take={take}&skip=0&nmId={nmId}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                uri,
                headers={"Authorization": settings.AUTHORIZATION_WB},
            )
            response.raise_for_status()
        except httpx.HTTPError:
            return Feedbacks(feedbacks=[])
        except httpx.ConnectTimeout:
            return Feedbacks(feedbacks=[])
        data = response.json()
        for item in data["data"]["feedbacks"]:
            user_name = item["userName"]
            if user_name == "":
                user_name = "Пользователь ВБ"
            date_str = item["updatedDate"]
            date = datetime.fromisoformat(date_str.replace("Z", "+00:03"))
            feedback = Feedback(
                user_name=user_name,
                feedback=item["text"],
                date=date,
                valuation=item["productValuation"],
            )
            result.append(feedback)
        return Feedbacks(feedbacks=result)


async def fetch_data_from_ozon(take: int = 10) -> Feedbacks:
    result: list[Feedback] = []
    uri = "https://api-seller.ozon.ru/v2/review/list"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            uri,
            headers={
                "Client-Id": settings.CLIENT_ID_OZON,
                "Api-Key": settings.API_KEY_OZON,
            },
            data={
                "filters": {
                    "sku": [0],
                    "order_status": "DELIVERED",
                    "status": "NEW",
                    "published_from": datetime.fromisoformat(
                        "2026-01-01T00:00:00.257Z"
                    ),
                    "published_to": datetime.now(),
                },
                "last_id": "string",
                "limit": 100,
                "sort_dir": "ASC",
            },
        )
        try:
            response.raise_for_status()
        except httpx.HTTPError:
            return Feedbacks(feedbacks=[])
        except httpx.ConnectTimeout:
            return Feedbacks(feedbacks=[])
        data = response.json()
        for item in data["reviews"]:
            date_str = item["published_at"]
            date = datetime.fromisoformat(date_str.replace("Z", "+00:03"))
            feedback = Feedback(
                user_name="Пользователь Озон",
                feedback=item["text"],
                date=date,
                valuation=item["rating"],
            )
            result.append(feedback)
        return Feedbacks(feedbacks=result)


def _extract_text_from_yandex_description(description: dict[str, str]) -> str:
    result: list[str] = []
    advantages = description.get("advantages")
    if advantages:
        result.append(advantages)
    disadvantages = description.get("disadvantages")
    if disadvantages:
        result.append(disadvantages)
    comment = description.get("comment")
    if comment:
        result.append(comment)
    return "\n".join(result)


async def fetch_data_from_yandex(offerIds: list[str], take: int = 10) -> Feedbacks:
    result: list[Feedback] = []
    uri = f"https://api.partner.market.yandex.ru/v2/businesses/{settings.BUSINESS_ID_YANDEX}/goods-feedback?limit={take}"
    async with httpx.AsyncClient() as client:
        response = await client.post(
            uri,
            headers={
                "Api-Key": settings.API_KEY_YANDEX,
            },
            data={
                "feedbackIds": None,
                "dateTimeFrom": datetime.fromisoformat("2026-01-01T00:00:00+03:00"),
                "dateTimeTo": datetime.now(),
                "reactionStatus": "ALL",
                "ratingValues": None,
                "offerIds": offerIds,
                "paid": True,
            },
        )
        try:
            response.raise_for_status()
        except httpx.HTTPError:
            return Feedbacks(feedbacks=[])
        except httpx.ConnectTimeout:
            return Feedbacks(feedbacks=[])
        data = response.json()
        for item in data["result"]["feedbacks"]:
            user_name = item.get("author", "")
            if user_name == "":
                user_name = "Пользователь Яндекс"
            date_str = str(item["createdAt"])
            date = datetime.fromisoformat(date_str.replace("Z", "+00:03"))
            feedback = Feedback(
                user_name=user_name,
                feedback=_extract_text_from_yandex_description(item["description"]),
                date=date,
                valuation=item["statistics"]["rating"],
            )
            result.append(feedback)
        return Feedbacks(feedbacks=result)


async def run_all_tasks(param: FeedbackParam) -> list[Feedbacks]:
    tasks = []
    for nmId in param.wb_nmId_list:
        tasks.append(fetch_feedbacks_from_wb(nmId, 50))
    for offerId in param.ya_offerId_list:
        tasks.append(fetch_data_from_yandex([offerId], 50))
    results = await asyncio.gather(*tasks, return_exceptions=False)
    return results


def fetch_feedbacks_from_mp(param: FeedbackParam) -> Feedbacks:
    data = async_to_sync(run_all_tasks)(param)
    feedbacks = []
    for item in data:
        feedbacks.extend(item.feedbacks)
    feedbacks = sorted(feedbacks, key=lambda item: item.date, reverse=True)
    return Feedbacks(feedbacks=feedbacks)
