from typing_extensions import TypedDict, NotRequired, Literal
from binance.types import Side, TimeInForce, OrderType


class BaseOrder(TypedDict):
  side: Side
  recvWindow: NotRequired[int]

class LimitOrder(BaseOrder):
  type: Literal['LIMIT']
  quantity: str
  price: str
  timeInForce: TimeInForce
  icebergQty: NotRequired[str]

class LimitMakerOrder(BaseOrder):
  type: Literal['LIMIT_MAKER']
  quantity: str
  price: str
  icebergQty: NotRequired[str]

class MarketOrder(BaseOrder):
  type: Literal['MARKET']
  quantity: str
  timeInForce: NotRequired[TimeInForce]

class MarketOrderQuote(BaseOrder):
  type: Literal['MARKET']
  quoteOrderQty: str
  timeInForce: NotRequired[TimeInForce]

Order = LimitOrder | MarketOrder | MarketOrderQuote | LimitMakerOrder
