from typing import Any, Optional, List, Literal
from pydantic import BaseModel

from .constants import ZERO_ADDRESS

class ApiCreds(BaseModel):
    api_key: str
    api_secret: str
    api_passphrase: str


class RequestArgs(BaseModel):
    method: str
    request_path: str
    body: Optional[Any] = None


class BookParams(BaseModel):
    token_id: str
    side: str = ""


class OrderArgs(BaseModel):
    token_id: str
    """
    TokenID of the Conditional token asset being traded
    """

    price: float
    """
    Price used to create the order
    """

    size: float
    """
    Size in terms of the ConditionalToken
    """

    side: str
    """
    Side of the order
    """

    fee_rate_bps: int = 0
    """
    Fee rate, in basis points, charged to the order maker, charged on proceeds
    """

    nonce: int = 0
    """
    Nonce used for onchain cancellations
    """

    expiration: int = 0
    """
    Timestamp after which the order is expired.
    """

    taker: str = ZERO_ADDRESS
    """
    Address of the order taker. The zero address is used to indicate a public order.
    """


class MarketOrderArgs(BaseModel):
    token_id: str
    """
    TokenID of the Conditional token asset being traded
    """

    amount: float
    """
    Amount in terms of Collateral.
    """

    price: float = 0.0
    """
    Price used to create the order.
    """

    fee_rate_bps: int = 0
    """
    Fee rate, in basis points, charged to the order maker, charged on proceeds.
    """

    nonce: int = 0
    """
    Nonce used for onchain cancellations.
    """

    taker: str = ZERO_ADDRESS
    """
    Address of the order taker. The zero address is used to indicate a public order.
    """


class TradeParams(BaseModel):
    id: Optional[str] = None
    maker_address: Optional[str] = None
    market: Optional[str] = None
    asset_id: Optional[str] = None
    before: Optional[int] = None
    after: Optional[int] = None


class OpenOrderParams(BaseModel):
    id: Optional[str] = None
    market: Optional[str] = None
    asset_id: Optional[str] = None


class DropNotificationParams(BaseModel):
    ids: Optional[List[str]] = None


class OrderSummary(BaseModel):
    price: Optional[str] = None
    size: Optional[str] = None

    @property
    def __dict__(self):
        return self.model_dump()

    @property
    def json(self):
        return self.json()


class OrderBookSummary(BaseModel):
    market:str asset_id timestamp:str
