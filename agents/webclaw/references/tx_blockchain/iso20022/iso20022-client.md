# ISO 20022 Client

The ISO 20022 Client is an application that enables financial institutions to send and receive secure ISO 20022 messages using TX Blockchain's smart tokenization.

## Networks

| Network | Chain ID | gRPC URL | Contract Address (Example) |
|---------|----------|----------|---------------------------|
| **Devnet** | `txchain-devnet-1` | `https://grpc.devnet.tx.dev:443` | `devcore1...` |
| **Testnet** | `txchain-testnet-1` | `https://grpc.testnet.tx.dev:443` | `testcore1eyky8vfdyz77zkh50zkrdw3mc9guyrfy45pd5ak9jpqgtgwgfvfqd8lkmc` |
| **Mainnet** | `txchain-mainnet-1` | `https://grpc.tx.org:443` | `core1...` |

## Definitions

| Term | Definition |
|------|------------|
| **ISO 20022** | A single standardization approach (methodology, process, repository) used by all financial standards initiatives |
| **ISO 20022 Messaging System** | A decentralized messenger connecting financial institutions to pass ISO 20022 messages securely, like SWIFT for traditional banks. Consists of a smart token deployed on blockchain and a client application |
| **ISO 20022 Client** | Application running on financial institutions' infrastructure that abstracts blockchain complexities and acts as an HTTP server |
| **ISO 20022 Message** | XML file generated using ISO 20022 standard describing financial operations (credit transfers, statements, etc.) |

## How It Works

### Sending Process (5 Steps)
┌─────────────────────────────────────────────────────────────────────────────┐
│ SENDING ISO 20022 MESSAGE │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Step 1 │───▶│ Step 2 │───▶│ Step 3 │───▶│ Step 4 │ │
│ │ Read & │ │ Find │ │ Compress & │ │ Mint NFT │ │
│ │ Parse XML │ │ Recipient │ │ Encrypt │ │ │ │
│ └─────────────┘ │ Address │ │ (Diffie- │ └─────────────┘ │
│ └─────────────┘ │ Hellman) │ │ │
│ └─────────────┘ ▼ │
│ │ ┌─────────────┐ │
│ ▼ │ Step 5 │ │
│ ┌─────────────┐ │ Send to │ │
│ │ Symmetric │ │ Smart │ │
│ │ Key Gen │────▶│ Contract │ │
│ └─────────────┘ └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

text

1. **Read & Parse XML** - Extract Financial Institution Identity of recipient from message
2. **Find Recipient** - Look up wallet address and public key from address book
3. **Compress & Encrypt** - Compress XML and encrypt using symmetric key generated via Diffie-Hellman key exchange (using receiver's public key + sender's private key)
4. **Mint NFT** - Create NFT from encrypted data
5. **Send to Smart Contract** - Store NFT with sender and recipient addresses

### Receiving Process (7 Steps)
┌─────────────────────────────────────────────────────────────────────────────┐
│ RECEIVING ISO 20022 MESSAGE │
├─────────────────────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Step 1 │───▶│ Step 2 │───▶│ Step 3 │───▶│ Step 4 │ │
│ │ Query New │ │ Query NFT │ │ Decrypt & │ │ Parse XML │ │
│ │ Messages │ │ Data │ │ Decompress │ │ │ │
│ └─────────────┘ └─────────────┘ │ (Diffie- │ └─────────────┘ │
│ │ │ │ Hellman) │ │ │
│ │ │ └─────────────┘ ▼ │
│ │ │ │ ┌─────────────┐ │
│ │ │ ▼ │ Step 5 │ │
│ │ │ ┌─────────────┐ │ Find │ │
│ │ │ │ Symmetric │ │ Sender │ │
│ │ │ │ Key Gen │────▶│ Address │ │
│ │ │ └─────────────┘ └─────────────┘ │
│ │ │ │ │
│ │ │ ▼ │
│ │ │ ┌─────────────┐ │
│ │ │ │ Step 6 │ │
│ │ │ │ Verify │ │
│ │ │ │ Sender │ │
│ │ │ └─────────────┘ │
│ │ │ │ │
│ │ │ ▼ │
│ │ │ ┌─────────────┐ │
│ │ └────────────────────────────────▶│ Step 7 │ │
│ │ │ Write XML │ │
│ │ │ to File │ │
│ │ └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘

text

1. **Query New Messages** - Periodically check for new messages
2. **Query NFT Data** - Retrieve NFT information for received message
3. **Decrypt & Decompress** - Decrypt NFT data using symmetric key (sender's public key + recipient's private key via Diffie-Hellman)
4. **Parse XML** - Extract Financial Institution Identity of sender
5. **Find Sender** - Look up wallet address from address book
6. **Verify Sender** - Confirm message sender matches ISO 20022 sender
7. **Write XML** - Save message to file for processing

## Example Flow: Credit Transfer
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│ Debtor │───▶│ Debtor │───▶│ ISO20022 │───▶│ Smart │───▶│ Creditor │
│ (Person) │ │ Agent │ │ Client │ │ Contract │ │ Agent │
│ │ │ (Bank A) │ │ (Bank A) │ │ (TX) │ │ (Bank B) │
└────────────┘ └────────────┘ └────────────┘ └────────────┘ └────────────┘
│ │ │ │ │
│ PAIN.001 │ │ │ │
│───────────────▶ │ │ │ │
│ │ │ │ │
│ │ PACS.008 │ │ │
│ │ (ISO 20022) │ │ │
│ │─────────────────▶│ │ │
│ │ │ │ │
│ │ │ Encrypt & Mint │ │
│ │ │─────────────────▶│ │
│ │ │ │ │
│ │ │ │ Periodically Poll │
│ │ │ │◁─────────────────│
│ │ │ │ │
│ │ │ │ NFT Data │
│ │ │ │─────────────────▶│
│ │ │ │ │
│ │ │ │ Decrypt & Process│
│ │ │ │ │
│ │ │ │ CAMT.053 │
│ │ │ │─────────────────▶│
│ │ │ │ │
│ │ │ │ Creditor
│ │ │ │ (Person)

text

**Message Types:**
- **PAIN.001** - CustomerCreditTransferInitiation (Payment Initiation)
- **PACS.008** - FIToFICustomerCreditTransfer (Payments Clearing & Settlement)
- **CAMT.053** - BankToCustomerStatement (Cash Management)

## Real-Time Gross Settlement (RTGS)

When a party sends a PACS.008 message with settlement method `CLRG` and clearing system proprietary set to `TX`, the client application handles RTGS:

```xml
<SttlmInf>
    <SttlmMtd>CLRG</SttlmMtd>
    <ClrSys>
        <Prtry>TX</Prtry>
    </ClrSys>
</SttlmInf>
RTGS Flow with TX Settlement
text
┌──────────────┐                    ┌──────────────┐
│  Debtor      │                    │  Creditor    │
│  Agent       │                    │  Agent       │
│  (Bank A)    │                    │  (Bank B)    │
└──────┬───────┘                    └──────┬───────┘
       │                                    │
       │ 1. PACS.008 + Funds to Escrow      │
       │────────────────────────────────────▶│
       │                                    │
       │ 2. PACS.002 (Accept)               │
       │◁────────────────────────────────────│
       │                                    │
       │ 3. Funds released from Escrow      │
       │    to Creditor Agent               │
       │────────────────────────────────────▶│
       │                                    │
       │         OR (if rejected)           │
       │                                    │
       │ 2b. PACS.002 (Reject)              │
       │◁────────────────────────────────────│
       │                                    │
       │ 3b. Funds refunded to Debtor       │
       │    Agent                           │
Currency Support
ISO 20022 is designed for traditional banking and only supports ISO 4217 currencies (USD, EUR, etc.). To provide RTGS support while maintaining ISO 20022 compliance, TX defines 3 rules:

Rule	Description
1	IntrBkSttlmAmt amount set to 0
2	Currency (Ccy) set to USD
3	Actual cryptocurrency amount provided as SplmtryData
Supplementary Data Format
Using DTI (Digital Token Identifier):

xml
<SplmtryData>
    <PlcAndNm>CryptoCurrencyAndAmountInfo</PlcAndNm>
    <Envlp>
        <s:Document>
            <s:CryptoCurrencyAndAmount Dti="6G5C9N3LG">0.001</s:CryptoCurrencyAndAmount>
        </s:Document>
    </Envlp>
</SplmtryData>
Using Cccy (Alternative - Denom format):

xml
<SplmtryData>
    <PlcAndNm>CryptoCurrencyAndAmountInfo</PlcAndNm>
    <Envlp>
        <s:Document>
            <s:CryptoCurrencyAndAmount Cccy="utestcore">1000</s:CryptoCurrencyAndAmount>
        </s:Document>
    </Envlp>
</SplmtryData>
Supported Denom Formats
Format	Example	Network
Native token	ucore	Mainnet
Native token	utestcore	Testnet
Native token	udevcore	Devnet
Smart FT	SUBUNIT-testcore1adst6w4e79tddzhcgaru2l2gms8jjep6a4caa7	Testnet
IBC coin	ibc/927661F31AA9C5801D58104292A35053097B393CFFA0D9B6CB450A3D66D747FA	Any
Note: We are in process of allocating DTIs to our tokens. The DTIs used above are temporary. Please use Cccy as alternative until the process is complete.

Quick Start Guide
1. Download Binary
bash
# From releases page
wget https://github.com/tokenize-x/iso20022-client/releases/latest/iso20022-client-linux-amd64

# Or build from source
git clone https://github.com/tokenize-x/iso20022-client
cd iso20022-client
make build
2. Initialize
bash
# Default (mainnet)
iso20022-client init

# Testnet configuration
iso20022-client init \
    --chain-id=txchain-testnet-1 \
    --coreum-contract-address=testcore1eyky8vfdyz77zkh50zkrdw3mc9guyrfy45pd5ak9jpqgtgwgfvfqd8lkmc \
    --coreum-grpc-url=https://grpc.testnet.tx.dev:443

# Devnet configuration
iso20022-client init \
    --chain-id=txchain-devnet-1 \
    --coreum-contract-address=devcore1... \
    --coreum-grpc-url=https://grpc.devnet.tx.dev:443
3. Add Key
bash
# Recover existing wallet from mnemonic
iso20022-client keys add iso20022-client --recover

# Or generate new wallet
iso20022-client keys add iso20022-client
Example Output:

text
- address: core1tagmslrz9xqfyjdddt6nu3q97us3ejck6475n8
  name: iso20022-client
  pubkey: '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"AqV7ob5PTCKOaiOp6iD6tQvjGorS6xLJiGQaVRBvQzM+"}'
  type: local
4. Register Your Institution
Required information for registration:

Wallet address (from output above)

Public key (the key field from pubkey)

BIC (Business Identification Code from ISO 20022)

Submit this information to the address book maintainer.

5. Start Application
bash
# Default (port 2843)
iso20022-client start

# Custom port and key name
iso20022-client start \
    --server-addr=':2844' \
    --key-name=iso20022-client-2
6. Send Message
bash
# Via CLI
iso20022-client message send /path/to/request.xml

# With custom server
iso20022-client message send /path/to/request.xml --server-addr=':2843'
7. Receive Message
bash
# Via CLI (periodic polling)
iso20022-client message receive /path/to/response.xml
HTTP API
When running, the HTTP server provides Swagger documentation at:

text
http://127.0.0.1:2843/
API Endpoints
Method	Endpoint	Description
POST	/api/v1/messages/send	Send ISO 20022 message
GET	/api/v1/messages/receive	Receive pending messages
GET	/api/v1/health	Health check
GET	/api/v1/status	Node status
Complete PACS.008 Example with Supplementary Data
xml
<?xml version="1.0" encoding="UTF-8"?>
<Document xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.08">
  <FIToFICstmrCdtTrf>
    <GrpHdr>
      <MsgId>MSG202404020001</MsgId>
      <CreDtTm>2024-04-02T10:30:00Z</CreDtTm>
      <NbOfTxs>1</NbOfTxs>
      <SttlmInf>
        <SttlmMtd>CLRG</SttlmMtd>
        <ClrSys>
          <Prtry>TX</Prtry>
        </ClrSys>
        <SttlmAcct>
          <Id>
            <IBAN>TX12345678901234567890</IBAN>
          </Id>
        </SttlmAcct>
      </SttlmInf>
    </GrpHdr>
    
    <CdtTrfTxInf>
      <PmtId>
        <EndToEndId>E2E202404020001</EndToEndId>
        <TxId>TX202404020001</TxId>
      </PmtId>
      
      <Amt>
        <IntrBkSttlmAmt Ccy="USD">0</IntrBkSttlmAmt>
      </Amt>
      
      <Dbtr>
        <Nm>Institution A</Nm>
      </Dbtr>
      
      <CdtrAgt>
        <FinInstnId>
          <BIC>INSTBANKXXX</BIC>
        </FinInstnId>
      </CdtrAgt>
      
      <Cdtr>
        <Nm>Institution B</Nm>
      </Cdtr>
      
      <!-- Supplementary Data for Crypto Amount -->
      <SplmtryData>
        <PlcAndNm>CryptoCurrencyAndAmountInfo</PlcAndNm>
        <Envlp>
          <s:Document>
            <s:CryptoCurrencyAndAmount Dti="6G5C9N3LG">1000</s:CryptoCurrencyAndAmount>
          </s:Document>
        </Envlp>
      </SplmtryData>
    </CdtTrfTxInf>
  </FIToFICstmrCdtTrf>
</Document>
Configuration File
Location: ~/.iso20022-client/config.toml

toml
# Chain Configuration
chain_id = "txchain-testnet-1"
grpc_url = "https://grpc.testnet.tx.dev:443"
contract_address = "testcore1eyky8vfdyz77zkh50zkrdw3mc9guyrfy45pd5ak9jpqgtgwgfvfqd8lkmc"

# Client Configuration
key_name = "iso20022-client"
server_addr = ":2843"

# Polling Configuration
poll_interval_seconds = 30
max_messages_per_poll = 10

# Address Book
address_book_url = "https://addressbook.iso20022.tx.org"
Limitations (First PoC Version)
Only supported Business Area (BA) is Payments Clearing and Settlement (PACS)

TODO
Add new messages from ISO 20022 message definitions

Add old messages from ISO 20022 message archive

Resources
ISO 20022 Website

DTI Registry

ISO 20022 Message Definitions

TX Blockchain Documentation

text

---

Now update the ISO 20022 README:

```bash
nano ~/dev/TXdocumentation/iso20022/README.md
Add this section:

markdown
## ISO 20022 Client

### ISO 20022 Client Application

For a complete guide on installing, configuring, and using the ISO 20022 Client:

📖 **[ISO 20022 Client Documentation](./iso20022-client.md)**

This guide covers:
- Network configurations (Devnet, Testnet, Mainnet)
- 5-step sending process with Diffie-Hellman encryption
- 7-step receiving process
- Real-Time Gross Settlement (RTGS) integration
- Currency support with DTI and Cccy formats
- Quick start installation and configuration
- Complete PACS.008 example with supplementary data
- HTTP API endpoints
