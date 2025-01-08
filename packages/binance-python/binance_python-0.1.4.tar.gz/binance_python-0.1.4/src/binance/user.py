from dataclasses import dataclass
from datetime import datetime
import json
from urllib.parse import urlencode
from decimal import Decimal
from pydantic import BaseModel, TypeAdapter
from binance.types import OrderStatus, Side
from .client import ClientMixin
from .util import sign, binance_timestamp

@dataclass
class UserMixin(ClientMixin):
  api_key: str
  api_secret: str
  base: str = 'https://api.binance.com'

  def sign(self, query_string: str) -> str:
    return sign(query_string, secret=self.api_secret)
  
  def signed_query(self, params: dict) -> str:
    query = urlencode(params)
    return query + '&signature=' + self.sign(query)
  

class Balance(BaseModel):
  asset: str
  free: str
  locked: str

class BalanceResponse(BaseModel):
  balances: list[Balance]

  def free(self, asset: str) -> Decimal:
    for b in self.balances:
      if b.asset == asset:
        return Decimal(b.free)
    return Decimal(0)
  
@dataclass
class _Balance(UserMixin):
  @UserMixin.with_client
  async def balance(self, recvWindow: int = 5000, omitZeroBalances: bool = True) -> BalanceResponse:
    query = self.signed_query({
      'timestamp': binance_timestamp(datetime.now()),
      'recvWindow': recvWindow,
      'omitZeroBalances': json.dumps(omitZeroBalances),
    })
    r = await self.client.get(
      f'{self.base}/api/v3/account?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return r.json()
    return BalanceResponse.model_validate_json(r.text)
  

class Order(BaseModel):
  price: str
  side: Side
  orderId: int
  origQty: str
  status: OrderStatus

OrdersAdapter = TypeAdapter(list[Order])

@dataclass
class _Orders(UserMixin):
  @UserMixin.with_client
  async def orders(self, symbol: str, recvWindow: int = 5000) -> list[Order]:
    query = self.signed_query({
      'symbol': symbol,
      'timestamp': binance_timestamp(datetime.now()),
      'recvWindow': recvWindow,
    })
    r = await self.client.get(
      f'{self.base}/api/v3/allOrders?{query}',
      headers={'X-MBX-APIKEY': self.api_key},
    )
    return OrdersAdapter.validate_json(r.text)
  

@dataclass
class User(_Balance, _Orders):
  ...