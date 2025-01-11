import httpx
from poly_apis.clob_types import (
    DropNotificationParams,
    BalanceAllowanceParams,
    OrderScoringParams,
    OrdersScoringParams,
    TradeParams,
    OpenOrderParams,
)
from ..exceptions import PolyApiException

GET = "GET"
POST = "POST"
DELETE = "DELETE"
PUT = "PUT"

def overload_headers(method: str, headers: dict) -> dict:
    if headers is None:
        headers = {}
    headers["User-Agent"] = "poly_apis"
    headers["Accept"] = "*/*"
    headers["Connection"] = "keep-alive"
    headers["Content-Type"] = "application/json"
    if method == GET:
        headers["Accept-Encoding"] = "gzip"
    return headers

def request(endpoint: str, method: str, headers=None, data=None):
    try:
        headers = overload_headers(method, headers)
        with httpx.Client() as client:
            resp = client.request(
                method=method,
                url=endpoint,
                headers=headers,
                json=data if data else None
            )
        if resp.status_code != 200:
            raise PolyApiException(resp)
        try:
            return resp.json()
        except httpx.JSONDecodeError:
            return resp.text
    except httpx.RequestError as exc:
        raise PolyApiException(error_msg=f"Request exception: {exc}")

def post(endpoint, headers=None, data=None):
    return request(endpoint, POST, headers, data)

def get(endpoint, headers=None, data=None):
    return request(endpoint, GET, headers, data)

def delete(endpoint, headers=None, data=None):
    return request(endpoint, DELETE, headers, data)

def build_query_params(url: str, param: str, val: str) -> str:
    url_with_params = url
    last = url_with_params[-1]
    if last == "?":
        url_with_params = f"{url_with_params}{param}={val}"
    else:
        url_with_params = f"{url_with_params}&{param}={val}"
    return url_with_params

def add_query_trade_params(base_url: str, params: TradeParams = None, next_cursor="MA==") -> str:
    url = base_url
    if params:
        url += "?"
        if params.market:
            url = build_query_params(url, "market", params.market)
        if params.asset_id:
            url = build_query_params(url, "asset_id", params.asset_id)
        if params.after:
            url = build_query_params(url, "after", params.after)
        if params.before:
            url = build_query_params(url, "before", params.before)
        if params.maker_address:
            url = build_query_params(url, "maker_address", params.maker_address)
        if params.id:
            url = build_query_params(url, "id", params.id)
        if next_cursor:
            url = build_query_params(url, "next_cursor", next_cursor)
    return url

def add_query_open_orders_params(base_url: str, params: OpenOrderParams = None, next_cursor="MA==") -> str:
    url = base_url
    if params:
        url += "?"
        if params.market:
            url = build_query_params(url, "market", params.market)
        if params.asset_id:
            url = build_query_params(url, "asset_id", params.asset_id)
        if params.id:
            url = build_query_params(url, "id", params.id)
        if next_cursor:
            url = build_query_params(url, "next_cursor", next_cursor)
    return url

def drop_notifications_query_params(base_url: str, params: DropNotificationParams = None) -> str:
    url = base_url
    if params and params.ids:
        url += f"?ids={','.join(params.ids)}"
    return url

def add_balance_allowance_params_to_url(base_url: str, params: BalanceAllowanceParams = None) -> str:
    url = base_url
    if params:
        url += "?"
        if params.asset_type:
            url = build_query_params(url, "asset_type", str(params.asset_type))
        if params.token_id:
            url = build_query_params(url, "token_id", params.token_id)
        if params.signature_type is not None:
            url = build_query_params(url, "signature_type", params.signature_type)
    return url

def add_order_scoring_params_to_url(base_url: str, params: OrderScoringParams = None) -> str:
    url = base_url
    if params and params.orderId:
        url += f"?order_id={params.orderId}"
    return url

def add_orders_scoring_params_to_url(base_url: str, params: OrdersScoringParams = None) -> str:
    url = base_url
    if params and params.orderIds:
        url += f"?order_ids={','.join(params.orderIds)}"
    return url
