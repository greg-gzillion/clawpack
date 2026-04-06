# Coreum Fee Model - Protobuf Documentation

## Service: Query

| Method | Request | Response | HTTP Endpoint |
|--------|---------|----------|---------------|
| MinGasPrice | QueryMinGasPriceRequest | QueryMinGasPriceResponse | `/coreum/feemodel/v1/min_gas_price` |
| RecommendedGasPrice | QueryRecommendedGasPriceRequest | QueryRecommendedGasPriceResponse | `/coreum/feemodel/v1/recommended_gas_price` |
| Params | QueryParamsRequest | QueryParamsResponse | `/coreum/feemodel/v1/params` |

## Service: Msg

| Method | Request | Response | Description |
|--------|---------|----------|-------------|
| UpdateParams | MsgUpdateParams | EmptyResponse | Update fee model parameters |

## Types

### Params

| Field | Type | Description |
|-------|------|-------------|
| model | ModelParams | Fee model parameters |

### ModelParams

| Field | Type | Description |
|-------|------|-------------|
| initial_gas_price | string | Gas price when block gas average is 0 |
| max_gas_price_multiplier | string | Multiplier for max gas price |
| max_discount | string | Maximum discount on gas price |
| escalation_start_fraction | string | Fraction where escalation starts |
| max_block_gas | int64 | Maximum block gas capacity |
| short_ema_block_length | uint32 | Short EMA block length |
| long_ema_block_length | uint32 | Long EMA block length |

### QueryRecommendedGasPriceResponse

| Field | Type | Description |
|-------|------|-------------|
| low | DecCoin | Low gas price recommendation |
| med | DecCoin | Medium gas price recommendation |
| high | DecCoin | High gas price recommendation |

### EventGas

| Field | Type | Description |
|-------|------|-------------|
| msgURL | string | Message URL |
| realGas | uint64 | Actual gas used |
| deterministicGas | uint64 | Deterministic gas estimate |
