# Coreum DEX - Protobuf Documentation

## Service: Msg

| Method | Request | Response | Description |
|--------|---------|----------|-------------|
| UpdateParams | MsgUpdateParams | EmptyResponse | Update module parameters |
| PlaceOrder | MsgPlaceOrder | EmptyResponse | Place order on orderbook |
| CancelOrder | MsgCancelOrder | EmptyResponse | Cancel an order |
| CancelOrdersByDenom | MsgCancelOrdersByDenom | EmptyResponse | Cancel all orders by denom |

## Service: Query

| Method | Request | Response | HTTP Endpoint |
|--------|---------|----------|---------------|
| Params | QueryParamsRequest | QueryParamsResponse | `/coreum/dex/v1/params` |
| Order | QueryOrderRequest | QueryOrderResponse | `/coreum/dex/v1/orders/{creator}/{id}` |
| Orders | QueryOrdersRequest | QueryOrdersResponse | `/coreum/dex/v1/orders/{creator}` |
| OrderBooks | QueryOrderBooksRequest | QueryOrderBooksResponse | `/coreum/dex/v1/order-books` |
| OrderBookParams | QueryOrderBookParamsRequest | QueryOrderBookParamsResponse | `/coreum/dex/v1/order-book-params` |
| OrderBookOrders | QueryOrderBookOrdersRequest | QueryOrderBookOrdersResponse | `/coreum/dex/v1/order-books/{base_denom}/{quote_denom}/orders` |
| AccountDenomOrdersCount | QueryAccountDenomOrdersCountRequest | QueryAccountDenomOrdersCountResponse | `/coreum/dex/v1/accounts/{account}/denoms/{denom}/orders-count` |

## Types

### OrderType (Enum)

| Name | Number | Description |
|------|--------|-------------|
| ORDER_TYPE_UNSPECIFIED | 0 | Default value |
| ORDER_TYPE_LIMIT | 1 | Limit order |
| ORDER_TYPE_MARKET | 2 | Market order |

### Side (Enum)

| Name | Number | Description |
|------|--------|-------------|
| SIDE_UNSPECIFIED | 0 | Default value |
| SIDE_BUY | 1 | Buy order |
| SIDE_SELL | 2 | Sell order |

### TimeInForce (Enum)

| Name | Number | Description |
|------|--------|-------------|
| TIME_IN_FORCE_UNSPECIFIED | 0 | Default value |
| TIME_IN_FORCE_GTC | 1 | Good till cancelled |
| TIME_IN_FORCE_IOC | 2 | Immediate or cancel |
| TIME_IN_FORCE_FOK | 3 | Fill or kill |

### Order

| Field | Type | Description |
|-------|------|-------------|
| creator | string | Order creator address |
| type | OrderType | Order type |
| id | string | Unique order ID |
| sequence | uint64 | Order sequence |
| base_denom | string | Base denomination |
| quote_denom | string | Quote denomination |
| price | string | Price (base per quote) |
| quantity | string | Quantity of base denom |
| side | Side | Buy or sell |
| remaining_base_quantity | string | Remaining quantity |
| remaining_spendable_balance | string | Remaining spendable balance |
| good_til | GoodTil | Expiration |
| time_in_force | TimeInForce | Time in force |
| reserve | Coin | Reserve required |

### GoodTil

| Field | Type | Description |
|-------|------|-------------|
| good_til_block_height | uint64 | Expire at block height |
| good_til_block_time | Timestamp | Expire at timestamp |

### MsgPlaceOrder

| Field | Type | Description |
|-------|------|-------------|
| sender | string | Order creator address |
| type | OrderType | Order type |
| id | string | Unique order ID |
| base_denom | string | Base denomination |
| quote_denom | string | Quote denomination |
| price | string | Price |
| quantity | string | Quantity |
| side | Side | Buy or sell |
| good_til | GoodTil | Expiration |
| time_in_force | TimeInForce | Time in force |

### MsgCancelOrder

| Field | Type | Description |
|-------|------|-------------|
| sender | string | Order creator address |
| id | string | Order ID to cancel |

### Events

| Event | Description |
|-------|-------------|
| EventOrderCreated | Order saved to order book |
| EventOrderPlaced | New order placed |
| EventOrderReduced | Order reduced during matching |
| EventOrderClosed | Order closed and removed |

### Params

| Field | Type | Description |
|-------|------|-------------|
| default_unified_ref_amount | string | Default USD reference amount |
| price_tick_exponent | int32 | Price tick exponent |
| quantity_step_exponent | int32 | Quantity step exponent |
| max_orders_per_denom | uint64 | Max orders per denom |
| order_reserve | Coin | Reserve requirement |
