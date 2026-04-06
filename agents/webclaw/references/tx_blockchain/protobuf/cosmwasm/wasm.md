# CosmWasm - Protobuf Documentation

## Service: Msg

| Method | Request | Response | Description |
|--------|---------|----------|-------------|
| StoreCode | MsgStoreCode | MsgStoreCodeResponse | Upload Wasm code |
| InstantiateContract | MsgInstantiateContract | MsgInstantiateContractResponse | Create contract instance |
| InstantiateContract2 | MsgInstantiateContract2 | MsgInstantiateContract2Response | Create contract with predictable address |
| ExecuteContract | MsgExecuteContract | MsgExecuteContractResponse | Execute contract |
| MigrateContract | MsgMigrateContract | MsgMigrateContractResponse | Migrate contract to new code |
| UpdateAdmin | MsgUpdateAdmin | MsgUpdateAdminResponse | Update contract admin |
| ClearAdmin | MsgClearAdmin | MsgClearAdminResponse | Remove contract admin |
| UpdateInstantiateConfig | MsgUpdateInstantiateConfig | MsgUpdateInstantiateConfigResponse | Update instantiate config |
| UpdateParams | MsgUpdateParams | MsgUpdateParamsResponse | Update module params |
| SudoContract | MsgSudoContract | MsgSudoContractResponse | Sudo call (governance) |
| PinCodes | MsgPinCodes | MsgPinCodesResponse | Pin codes to cache |
| UnpinCodes | MsgUnpinCodes | MsgUnpinCodesResponse | Unpin codes from cache |
| StoreAndInstantiateContract | MsgStoreAndInstantiateContract | MsgStoreAndInstantiateContractResponse | Store and instantiate |
| UpdateContractLabel | MsgUpdateContractLabel | MsgUpdateContractLabelResponse | Update contract label |

## Service: Query

| Method | Request | Response | HTTP Endpoint |
|--------|---------|----------|---------------|
| ContractInfo | QueryContractInfoRequest | QueryContractInfoResponse | `/cosmwasm/wasm/v1/contract/{address}` |
| ContractHistory | QueryContractHistoryRequest | QueryContractHistoryResponse | `/cosmwasm/wasm/v1/contract/{address}/history` |
| ContractsByCode | QueryContractsByCodeRequest | QueryContractsByCodeResponse | `/cosmwasm/wasm/v1/code/{code_id}/contracts` |
| AllContractState | QueryAllContractStateRequest | QueryAllContractStateResponse | `/cosmwasm/wasm/v1/contract/{address}/state` |
| RawContractState | QueryRawContractStateRequest | QueryRawContractStateResponse | `/cosmwasm/wasm/v1/contract/{address}/raw/{query_data}` |
| SmartContractState | QuerySmartContractStateRequest | QuerySmartContractStateResponse | `/cosmwasm/wasm/v1/contract/{address}/smart/{query_data}` |
| Code | QueryCodeRequest | QueryCodeResponse | `/cosmwasm/wasm/v1/code/{code_id}` |
| Codes | QueryCodesRequest | QueryCodesResponse | `/cosmwasm/wasm/v1/code` |
| Params | QueryParamsRequest | QueryParamsResponse | `/cosmwasm/wasm/v1/codes/params` |
| PinnedCodes | QueryPinnedCodesRequest | QueryPinnedCodesResponse | `/cosmwasm/wasm/v1/codes/pinned` |
| ContractsByCreator | QueryContractsByCreatorRequest | QueryContractsByCreatorResponse | `/cosmwasm/wasm/v1/contracts/creator/{creator_address}` |

## Types

### AccessType (Enum)

| Name | Number | Description |
|------|--------|-------------|
| ACCESS_TYPE_UNSPECIFIED | 0 | Unspecified |
| ACCESS_TYPE_NOBODY | 1 | Forbidden |
| ACCESS_TYPE_EVERYBODY | 3 | Unrestricted |
| ACCESS_TYPE_ANY_OF_ADDRESSES | 4 | Allow specific addresses |

### AccessConfig

| Field | Type | Description |
|-------|------|-------------|
| permission | AccessType | Access type |
| addresses | string[] | Allowed addresses |

### ContractInfo

| Field | Type | Description |
|-------|------|-------------|
| code_id | uint64 | Reference to Wasm code |
| creator | string | Creator address |
| admin | string | Admin address (can migrate) |
| label | string | Metadata label |
| created | AbsoluteTxPosition | Creation position |
| ibc_port_id | string | IBC port ID |

### MsgStoreCode

| Field | Type | Description |
|-------|------|-------------|
| sender | string | Sender address |
| wasm_byte_code | bytes | Wasm code (raw or gzip) |
| instantiate_permission | AccessConfig | Permission for instantiation |

### MsgInstantiateContract

| Field | Type | Description |
|-------|------|-------------|
| sender | string | Sender address |
| admin | string | Optional admin address |
| code_id | uint64 | Code ID reference |
| label | string | Contract label |
| msg | bytes | JSON instantiate message |
| funds | Coin[] | Initial funds |

### MsgExecuteContract

| Field | Type | Description |
|-------|------|-------------|
| sender | string | Sender address |
| contract | string | Contract address |
| msg | bytes | JSON execute message |
| funds | Coin[] | Funds to transfer |

### IBC Messages

| Message | Description |
|---------|-------------|
| MsgIBCSend | Send IBC packet from contract |
| MsgIBCCloseChannel | Close IBC channel |
| MsgIBCWriteAcknowledgementResponse | Write IBC acknowledgement |

### Authz for Wasm

| Type | Description |
|------|-------------|
| ContractExecutionAuthorization | Execute contract on behalf |
| ContractMigrationAuthorization | Migrate contract on behalf |
| StoreCodeAuthorization | Upload code on behalf |
| AcceptedMessageKeysFilter | Filter by message keys |
| AcceptedMessagesFilter | Filter by raw messages |
| AllowAllMessagesFilter | Allow all messages |
| MaxCallsLimit | Limit number of calls |
| MaxFundsLimit | Limit funds transferable |
| CombinedLimit | Combined call + funds limit |
