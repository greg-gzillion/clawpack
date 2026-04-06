# Coreum Asset NFT - Protobuf Documentation

## Service: Msg

| Method | Request | Response | Description |
|--------|---------|----------|-------------|
| IssueClass | MsgIssueClass | EmptyResponse | Create new NFT class |
| Mint | MsgMint | EmptyResponse | Mint new NFT |
| UpdateData | MsgUpdateData | EmptyResponse | Update NFT data |
| Burn | MsgBurn | EmptyResponse | Burn NFT |
| Freeze | MsgFreeze | EmptyResponse | Freeze NFT |
| Unfreeze | MsgUnfreeze | EmptyResponse | Unfreeze NFT |
| AddToWhitelist | MsgAddToWhitelist | EmptyResponse | Add to NFT whitelist |
| RemoveFromWhitelist | MsgRemoveFromWhitelist | EmptyResponse | Remove from NFT whitelist |
| AddToClassWhitelist | MsgAddToClassWhitelist | EmptyResponse | Add to class whitelist |
| RemoveFromClassWhitelist | MsgRemoveFromClassWhitelist | EmptyResponse | Remove from class whitelist |
| ClassFreeze | MsgClassFreeze | EmptyResponse | Freeze all NFTs in class |
| ClassUnfreeze | MsgClassUnfreeze | EmptyResponse | Unfreeze class |
| UpdateParams | MsgUpdateParams | EmptyResponse | Update module parameters |

## Service: Query

| Method | Request | Response | HTTP Endpoint |
|--------|---------|----------|---------------|
| Params | QueryParamsRequest | QueryParamsResponse | `/coreum/asset/nft/v1/params` |
| Class | QueryClassRequest | QueryClassResponse | `/coreum/asset/nft/v1/classes/{id}` |
| Classes | QueryClassesRequest | QueryClassesResponse | `/coreum/asset/nft/v1/classes` |
| Frozen | QueryFrozenRequest | QueryFrozenResponse | `/coreum/asset/nft/v1/classes/{class_id}/nfts/{id}/frozen` |
| ClassFrozen | QueryClassFrozenRequest | QueryClassFrozenResponse | `/coreum/asset/nft/v1/classes/{class_id}/frozen/{account}` |
| ClassFrozenAccounts | QueryClassFrozenAccountsRequest | QueryClassFrozenAccountsResponse | `/coreum/asset/nft/v1/classes/{class_id}/frozen` |
| Whitelisted | QueryWhitelistedRequest | QueryWhitelistedResponse | `/coreum/asset/nft/v1/classes/{class_id}/nfts/{id}/whitelisted/{account}` |
| WhitelistedAccountsForNFT | QueryWhitelistedAccountsForNFTRequest | QueryWhitelistedAccountsForNFTResponse | `/coreum/asset/nft/v1/classes/{class_id}/nfts/{id}/whitelisted` |
| ClassWhitelistedAccounts | QueryClassWhitelistedAccountsRequest | QueryClassWhitelistedAccountsResponse | `/coreum/asset/nft/v1/classes/{class_id}/whitelisted` |
| BurntNFT | QueryBurntNFTRequest | QueryBurntNFTResponse | `/coreum/asset/nft/v1/classes/{class_id}/burnt/{nft_id}` |
| BurntNFTsInClass | QueryBurntNFTsInClassRequest | QueryBurntNFTsInClassResponse | `/coreum/asset/nft/v1/classes/{class_id}/burnt` |

## Types

### Class

| Field | Type | Description |
|-------|------|-------------|
| id | string | Class unique identifier |
| issuer | string | Issuer address |
| name | string | Class name |
| symbol | string | Class symbol |
| description | string | Description |
| uri | string | Metadata URI |
| uri_hash | string | URI hash |
| data | google.protobuf.Any | Custom data |
| features | ClassFeature[] | Enabled features |
| royalty_rate | string | Royalty rate (0-1) |

### ClassFeature (Enum)

| Name | Number | Description |
|------|--------|-------------|
| burning | 0 | Can burn NFTs |
| freezing | 1 | Can freeze NFTs |
| whitelisting | 2 | Whitelist feature |
| disable_sending | 3 | Disable transfers |
| soulbound | 4 | Cannot be transferred |

### MsgIssueClass

| Field | Type | Description |
|-------|------|-------------|
| issuer | string | Issuer address |
| symbol | string | Class symbol |
| name | string | Class name |
| description | string | Description |
| uri | string | Metadata URI |
| uri_hash | string | URI hash |
| data | google.protobuf.Any | Custom data |
| features | ClassFeature[] | Enabled features |
| royalty_rate | string | Royalty rate |

### DataDynamic

| Field | Type | Description |
|-------|------|-------------|
| items | DataDynamicItem[] | Dynamic data items |

### DataDynamicItem

| Field | Type | Description |
|-------|------|-------------|
| editors | DataEditor[] | Allowed editors |
| data | bytes | Dynamic data |

### DataEditor (Enum)

| Name | Number | Description |
|------|--------|-------------|
| admin | 0 | Admin can edit |
| owner | 1 | Owner can edit |

### Events

| Event | Description |
|-------|-------------|
| EventClassIssued | New NFT class created |
| EventFrozen | NFT frozen |
| EventUnfrozen | NFT unfrozen |
| EventClassFrozen | Class frozen for account |
| EventClassUnfrozen | Class unfrozen for account |
| EventAddedToWhitelist | Added to NFT whitelist |
| EventRemovedFromWhitelist | Removed from NFT whitelist |
| EventAddedToClassWhitelist | Added to class whitelist |
| EventRemovedFromClassWhitelist | Removed from class whitelist |
