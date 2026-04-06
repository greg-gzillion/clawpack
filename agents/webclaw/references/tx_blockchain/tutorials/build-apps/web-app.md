# Web Application for TX Blockchain

Build a web application for TX Blockchain using TypeScript, React, Next.js, and CosmJS libraries. This application can be used as a starter for larger projects with extended TX integration.

## Overview

This tutorial creates a complete web app with:
- Keplr wallet integration
- NFT class creation and minting
- Token sending functionality
- Chain configuration management
- Custom transaction signing

## Prerequisites

```bash
# Install yarn package manager
npm install -g yarn

# Verify installations
yarn --version
node --version
Technologies Used
Tool/Framework	Purpose
Next.js	React-based framework for web applications
React	Component rendering
CosmJS	TX Blockchain interaction
DaisyUI	UI styles and components
Keplr	Wallet for transaction signing
Source Code
bash
# Clone tutorials and extract web app
git clone https://github.com/tokenize-x/tx-tutorials.git coreum-tutorials
cp -r coreum-tutorials/ts/web-app my-webapp
rm -rf coreum-tutorials

# Navigate to web app
cd my-webapp

# Install dependencies
yarn install

# Run development server
yarn dev
Chain Configuration
Create .env.development file:

env
PORT=3000
NEXT_PUBLIC_CHAIN_ID=txchain-testnet-1
NEXT_PUBLIC_CHAIN_NAME=TX Testnet
NEXT_PUBLIC_CHAIN_BECH32_PREFIX=testcore
NEXT_PUBLIC_CHAIN_RPC_ENDPOINT=https://rpc.testnet.tx.dev:443/
NEXT_PUBLIC_CHAIN_REST_ENDPOINT=https://rest.testnet.tx.dev:443/
NEXT_PUBLIC_CHAIN_EXPLORER=https://explorer.testnet.tx.dev/
NEXT_PUBLIC_STAKING_DENOM=utestcore
NEXT_PUBLIC_CHAIN_COIN_TYPE=990
NEXT_PUBLIC_SITE_TITLE=TX starter
NEXT_PUBLIC_SITE_ICON_URL="/coreum.svg"
NEXT_PUBLIC_GAS_PRICE=0.0625utestcore
Root Components
pages/_document.tsx
typescript
import Document, { Head, Html, Main, NextScript } from 'next/document'
import daisyuiThemes from 'styles/daisyui-themes.json'

const themes = Object.keys(daisyuiThemes) || ['']
export const defaultTheme = themes[0]

class MyDocument extends Document {
    static async getInitialProps(ctx: any) {
        const initialProps = await Document.getInitialProps(ctx)
        return { ...initialProps }
    }

    render() {
        return (
            <Html data-theme={defaultTheme}>
                <Head />
                <body>
                    <Main />
                    <NextScript />
                </body>
            </Html>
        )
    }
}

export default MyDocument
pages/_app.tsx
typescript
import 'styles/globals.css'
import type { AppProps } from 'next/app'
import Layout from 'components/Layout'
import { SigningClientProvider } from 'contexts/client'

function MyApp({ Component, pageProps }: AppProps) {
    return (
        <SigningClientProvider>
            <Layout>
                <Component {...pageProps} />
            </Layout>
        </SigningClientProvider>
    )
}

export default MyApp
Signing Client Provider
contexts/client.tsx
typescript
import React, { useState, createContext, useContext } from 'react'
import { SigningCosmWasmClient } from '@cosmjs/cosmwasm-stargate'
import { Tendermint34Client } from '@cosmjs/tendermint-rpc'
import { QueryClient } from '@cosmjs/stargate'
import { GasPrice } from '@cosmjs/stargate'
import { Registry, GeneratedType } from '@cosmjs/proto-signing'
import { defaultRegistryTypes } from '@cosmjs/stargate'
import { createProtobufRpcClient } from '@cosmjs/stargate'
import { connectKeplr } from 'services/keplr'
import { coreumRegistryTypes } from 'coreum/tx'
import { QueryClient as CoreumQueryClient } from 'coreum/query'

export interface IClientContext {
    walletAddress: string
    signingClient: SigningCosmWasmClient | null
    coreumQueryClient: CoreumQueryClient | null
    loading: boolean
    error: any
    connectWallet: any
    disconnect: Function
}

const PUBLIC_RPC_ENDPOINT = process.env.NEXT_PUBLIC_CHAIN_RPC_ENDPOINT || ''
const PUBLIC_CHAIN_ID = process.env.NEXT_PUBLIC_CHAIN_ID
const GAS_PRICE = process.env.NEXT_PUBLIC_GAS_PRICE || ''

const ClientContext = createContext<IClientContext>({} as IClientContext)

export const SigningClientProvider = ({ children }: { children: React.ReactNode }) => {
    const client = useClientContext()
    return <ClientContext.Provider value={client}>{children}</ClientContext.Provider>
}

export const useSigningClient = () => useContext(ClientContext)

export const useClientContext = (): IClientContext => {
    const [walletAddress, setWalletAddress] = useState('')
    const [signingClient, setSigningClient] = useState<SigningCosmWasmClient | null>(null)
    const [tmClient, setTmClient] = useState<Tendermint34Client | null>(null)
    const [coreumQueryClient, setCoreumQueryClient] = useState<CoreumQueryClient | null>(null)
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)

    const connectWallet = async () => {
        setLoading(true)

        try {
            await connectKeplr()

            // Enable website to access Keplr
            await (window as any).keplr.enable(PUBLIC_CHAIN_ID)

            // Get offline signer for signing txs
            const offlineSigner = await (window as any).getOfflineSigner(PUBLIC_CHAIN_ID)

            // Register default and custom messages
            let registryTypes: ReadonlyArray<[string, GeneratedType]> = [
                ...defaultRegistryTypes,
                ...coreumRegistryTypes,
            ]
            const registry = new Registry(registryTypes)

            // Signing client
            const client = await SigningCosmWasmClient.connectWithSigner(
                PUBLIC_RPC_ENDPOINT,
                offlineSigner,
                {
                    registry: registry,
                    gasPrice: GasPrice.fromString(GAS_PRICE),
                },
            )
            setSigningClient(client)

            // RPC client
            const tendermintClient = await Tendermint34Client.connect(PUBLIC_RPC_ENDPOINT)
            setTmClient(tendermintClient)
            const queryClient = new QueryClient(tendermintClient)
            setCoreumQueryClient(new CoreumQueryClient(createProtobufRpcClient(queryClient)))

            // Get user address
            const [{ address }] = await offlineSigner.getAccounts()
            setWalletAddress(address)
            setLoading(false)
        } catch (error: any) {
            console.error(error)
            setError(error)
        }
    }

    const disconnect = () => {
        if (signingClient) {
            signingClient.disconnect()
        }
        if (tmClient) {
            tmClient.disconnect()
        }
        setWalletAddress('')
        setSigningClient(null)
        setLoading(false)
    }

    return {
        walletAddress,
        signingClient,
        coreumQueryClient: coreumQueryClient,
        loading,
        error,
        connectWallet,
        disconnect,
    }
}
Keplr Integration
services/keplr.tsx
typescript
export const connectKeplr = async () => {
    if (!window.getOfflineSigner || !window.keplr) {
        alert('Please install Keplr extension')
    } else {
        if (window.keplr.experimentalSuggestChain) {
            const stakingDenom = convertFromMicroDenom(
                process.env.NEXT_PUBLIC_STAKING_DENOM || ''
            )
            const gasPrice = Number((process.env.NEXT_PUBLIC_GAS_PRICE || '')
                .replace(process.env.NEXT_PUBLIC_STAKING_DENOM || '', ''));

            try {
                await window.keplr.experimentalSuggestChain({
                    chainId: process.env.NEXT_PUBLIC_CHAIN_ID,
                    chainName: process.env.NEXT_PUBLIC_CHAIN_NAME,
                    rpc: process.env.NEXT_PUBLIC_CHAIN_RPC_ENDPOINT,
                    rest: process.env.NEXT_PUBLIC_CHAIN_REST_ENDPOINT,
                    stakeCurrency: {
                        coinDenom: stakingDenom,
                        coinMinimalDenom: process.env.NEXT_PUBLIC_STAKING_DENOM,
                        coinDecimals: 6,
                    },
                    bip44: {
                        coinType: Number(process.env.NEXT_PUBLIC_CHAIN_COIN_TYPE),
                    },
                    bech32Config: {
                        bech32PrefixAccAddr: process.env.NEXT_PUBLIC_CHAIN_BECH32_PREFIX,
                        bech32PrefixAccPub: `${process.env.NEXT_PUBLIC_CHAIN_BECH32_PREFIX}pub`,
                        bech32PrefixValAddr: `${process.env.NEXT_PUBLIC_CHAIN_BECH32_PREFIX}valoper`,
                        bech32PrefixValPub: `${process.env.NEXT_PUBLIC_CHAIN_BECH32_PREFIX}valoperpub`,
                        bech32PrefixConsAddr: `${process.env.NEXT_PUBLIC_CHAIN_BECH32_PREFIX}valcons`,
                        bech32PrefixConsPub: `${process.env.NEXT_PUBLIC_CHAIN_BECH32_PREFIX}valconspub`,
                    },
                    currencies: [{
                        coinDenom: stakingDenom,
                        coinMinimalDenom: process.env.NEXT_PUBLIC_STAKING_DENOM,
                        coinDecimals: 6,
                    }],
                    feeCurrencies: [{
                        coinDenom: stakingDenom,
                        coinMinimalDenom: process.env.NEXT_PUBLIC_STAKING_DENOM,
                        coinDecimals: 6,
                    }],
                    coinType: Number(process.env.NEXT_PUBLIC_CHAIN_COIN_TYPE),
                    gasPriceStep: {
                        low: gasPrice,
                        average: gasPrice,
                        high: gasPrice,
                    },
                })
            } catch {
                alert('Failed to suggest the chain')
            }
        } else {
            alert('Please use the recent version of Keplr extension')
        }
    }
}

function convertFromMicroDenom(denom: string): string {
    return denom.replace(/^u/, '')
}
Custom Transactions Registry
coreum/tx.ts
typescript
import {
    DeepPartial,
    Exact,
    MsgIssueClass as AssetNFTMsgIssueClass,
    MsgMint as AssetNFTMsgMint,
} from "./proto-ts/coreum/asset/nft/v1/tx";
import { MsgSend as NFTMsgSend } from "./proto-ts/coreum/nft/v1beta1/tx";
import { GeneratedType } from "@cosmjs/proto-signing";

export const coreumRegistryTypes: ReadonlyArray<[string, GeneratedType]> = [
    ["/coreum.asset.nft.v1.MsgIssueClass", AssetNFTMsgIssueClass],
    ["/coreum.asset.nft.v1.MsgMint", AssetNFTMsgMint],
    ["/coreum.nft.v1beta1.MsgSend", NFTMsgSend],
];

export namespace AssetNFT {
    export const MsgIssueClass = function <I extends Exact<DeepPartial<AssetNFTMsgIssueClass>, I>>(object: I) {
        return {
            typeUrl: "/coreum.asset.nft.v1.MsgIssueClass",
            value: AssetNFTMsgIssueClass.fromPartial(object),
        };
    };

    export const MsgMint = function <I extends Exact<DeepPartial<AssetNFTMsgMint>, I>>(object: I) {
        return {
            typeUrl: "/coreum.asset.nft.v1.MsgMint",
            value: AssetNFTMsgMint.fromPartial(object),
        };
    };
}

export namespace NFT {
    export const MsgSend = function <I extends Exact<DeepPartial<NFTMsgSend>, I>>(object: I) {
        return {
            typeUrl: "/coreum.nft.v1beta1.MsgSend",
            value: NFTMsgSend.fromPartial(object),
        };
    };
}
coreum/query.ts
typescript
import { QueryClientImpl as NFTQueryClient } from "./proto-ts/coreum/nft/v1beta1/query";

interface Rpc {
    request(service: string, method: string, data: Uint8Array): Promise<Uint8Array>;
}

export class QueryClient {
    private readonly nftClient: NFTQueryClient;

    constructor(rpc: Rpc) {
        this.nftClient = new NFTQueryClient(rpc)
    }

    public NFTClient(): NFTQueryClient {
        return this.nftClient
    }
}
Navigation Component
components/Nav.tsx
typescript
import { useSigningClient } from 'contexts/client'
import Link from 'next/link'
import Image from 'next/image'
import Router from 'next/router'

function Nav() {
    const { walletAddress, connectWallet, disconnect } = useSigningClient()
    
    const handleConnect = () => {
        if (walletAddress.length === 0) {
            connectWallet()
        } else {
            disconnect()
            Router.push('/')
        }
    }

    const PUBLIC_SITE_ICON_URL = process.env.NEXT_PUBLIC_SITE_ICON_URL || ''

    return (
        <div className="border-b w-screen px-2 md:px-16">
            <nav className="flex flex-wrap text-center md:text-left md:flex flex-row w-full justify-between items-center py-4">
                <div className="flex items-center">
                    <Link href="/">
                        <a>
                            {PUBLIC_SITE_ICON_URL.length > 0 ? (
                                <Image src={PUBLIC_SITE_ICON_URL} height={32} width={32} alt="Logo" />
                            ) : (
                                <span className="text-2xl">⚛️</span>
                            )}
                        </a>
                    </Link>
                    <Link href="/">
                        <a className="ml-1 md:ml-2 link link-hover font-semibold text-xl md:text-2xl align-top">
                            {process.env.NEXT_PUBLIC_SITE_TITLE}
                        </a>
                    </Link>
                </div>
                <div className="flex flex-grow lg:flex-grow-0 max-w-full">
                    <button
                        className="block btn btn-outline btn-primary w-full max-w-full truncate"
                        onClick={handleConnect}
                    >
                        {walletAddress || 'Connect Wallet'}
                    </button>
                </div>
            </nav>
        </div>
    )
}

export default Nav
Wallet Loader Component
components/WalletLoader.tsx
typescript
import { ReactNode } from 'react'
import { useSigningClient } from 'contexts/client'
import Loader from './Loader'

function WalletLoader({
    children,
    loading = false,
}: {
    children: ReactNode
    loading?: boolean
}) {
    const {
        walletAddress,
        loading: clientLoading,
        error,
        connectWallet,
    } = useSigningClient()

    if (loading || clientLoading) {
        return (
            <div className="justify-center">
                <Loader />
            </div>
        )
    }

    if (walletAddress === '') {
        return (
            <div className="max-w-full">
                <h1 className="text-6xl font-bold gap-2">
                    Welcome to
                    <a target="_blank" className="link link-primary link-hover" href="https://tx.org/">
                        TX!
                    </a>
                </h1>

                <p className="mt-3 text-2xl">
                    Get started by installing{' '}
                    <a className="pl-1 link link-primary link-hover" href="https://keplr.app/">
                        Keplr wallet
                    </a>
                </p>

                <div className="flex flex-wrap items-center justify-around md:max-w-4xl mt-6 sm:w-full">
                    <button
                        className="p-6 mt-6 text-left border border-secondary hover:border-primary w-96 rounded-xl hover:text-primary focus:text-primary-focus"
                        onClick={connectWallet}
                    >
                        <h3 className="text-2xl font-bold">Connect your wallet &rarr;</h3>
                        <p className="mt-4 text-xl">
                            Get your Keplr wallet connected now and start using it.
                        </p>
                    </button>
                </div>
            </div>
        )
    }

    if (error) {
        return <code>{JSON.stringify(error)}</code>
    }

    return <>{children}</>
}

export default WalletLoader
Home Page
pages/index.tsx
typescript
import type { NextPage } from 'next'
import Link from 'next/link'
import WalletLoader from 'components/WalletLoader'
import { useSigningClient } from 'contexts/client'

const Home: NextPage = () => {
    const { walletAddress } = useSigningClient()

    return (
        <WalletLoader>
            <h1 className="text-6xl font-bold">
                Welcome to {process.env.NEXT_PUBLIC_CHAIN_NAME}!
            </h1>

            <div className="mt-3 text-2xl">
                Your wallet address is:{' '}
                <Link href={process.env.NEXT_PUBLIC_CHAIN_EXPLORER + "accounts/" + walletAddress} passHref>
                    <a target="_blank" rel="noreferrer"
                       className="font-mono break-all whitespace-pre-wrap link link-primary">
                        {walletAddress}
                    </a>
                </Link>
            </div>

            <div className="flex flex-wrap items-center justify-around max-w-4xl mt-6 max-w-full sm:w-full">
                <Link href="https://docs.tx.org/tools-ecosystem/faucet.html" passHref>
                    <a target="_blank" rel="noreferrer"
                       className="p-6 mt-6 text-left border border-secondary hover:border-primary w-96 rounded-xl hover:text-primary focus:text-primary-focus">
                        <h3 className="text-2xl font-bold">Fund wallet &rarr;</h3>
                        <p className="mt-4 text-xl">
                            Fund your wallet for {process.env.NEXT_PUBLIC_CHAIN_NAME}.
                        </p>
                    </a>
                </Link>
                <Link href="/send" passHref>
                    <a className="p-6 mt-6 text-left border border-secondary hover:border-primary w-96 rounded-xl hover:text-primary focus:text-primary-focus">
                        <h3 className="text-2xl font-bold">Send to wallet &rarr;</h3>
                        <p className="mt-4 text-xl">
                            Execute a transaction to send funds to a wallet address.
                        </p>
                    </a>
                </Link>
                <Link href="/nft" passHref>
                    <a className="p-6 mt-6 text-left border border-secondary hover:border-primary w-96 rounded-xl hover:text-primary focus:text-primary-focus">
                        <h3 className="text-2xl font-bold">NFT &rarr;</h3>
                        <p className="mt-4 text-xl">
                            Create your NFT class and mint NFTs for it.
                        </p>
                    </a>
                </Link>
            </div>
        </WalletLoader>
    )
}

export default Home
Send Tokens Page
pages/send.tsx
typescript
import { useEffect, useState } from 'react'
import type { NextPage } from 'next'
import { Coin } from '@cosmjs/amino'
import WalletLoader from 'components/WalletLoader'
import { useSigningClient } from 'contexts/client'
import { convertDenomToMicroDenom, convertFromMicroDenom, convertMicroDenomToDenom } from 'util/conversion'

const PUBLIC_CHAIN_NAME = process.env.NEXT_PUBLIC_CHAIN_NAME
const PUBLIC_STAKING_DENOM = process.env.NEXT_PUBLIC_STAKING_DENOM || ''

const Send: NextPage = () => {
    const { walletAddress, signingClient } = useSigningClient()
    const [balance, setBalance] = useState('')
    const [loadedAt, setLoadedAt] = useState(new Date())
    const [loading, setLoading] = useState(false)
    const [recipientAddress, setRecipientAddress] = useState('')
    const [sendAmount, setSendAmount] = useState('')
    const [success, setSuccess] = useState('')
    const [error, setError] = useState('')

    useEffect(() => {
        if (!signingClient || walletAddress.length === 0) {
            return
        }
        setError('')
        setSuccess('')

        signingClient
            .getBalance(walletAddress, PUBLIC_STAKING_DENOM)
            .then((response: any) => {
                const { amount, denom }: { amount: number; denom: string } = response
                setBalance(
                    `${convertMicroDenomToDenom(amount)} ${convertFromMicroDenom(denom)}`
                )
            })
            .catch((error) => {
                setError(`Error! ${error.message}`)
            })
    }, [signingClient, walletAddress, loadedAt])

    const handleSend = () => {
        setError('')
        setSuccess('')
        setLoading(true)
        const amount: Coin[] = [
            {
                amount: convertDenomToMicroDenom(sendAmount),
                denom: PUBLIC_STAKING_DENOM,
            },
        ]

        signingClient
            ?.sendTokens(walletAddress, recipientAddress, amount, 'auto')
            .then(() => {
                const message = `Success! Sent ${sendAmount} ${convertFromMicroDenom(
                    PUBLIC_STAKING_DENOM
                )} to ${recipientAddress}.`

                setLoadedAt(new Date())
                setLoading(false)
                setSendAmount('')
                setSuccess(message)
            })
            .catch((error) => {
                setLoading(false)
                setError(`Error! ${error.message}`)
            })
    }

    return (
        <WalletLoader loading={loading}>
            <p className="text-2xl">Your wallet has {balance}</p>

            <h1 className="text-5xl font-bold my-8">
                Send to {PUBLIC_CHAIN_NAME} recipient wallet address:
            </h1>
            <div className="flex w-full max-w-xl">
                <input
                    type="text"
                    id="recipient-address"
                    className="input input-bordered focus:input-primary input-lg rounded-full flex-grow font-mono text-center text-lg"
                    placeholder={`${PUBLIC_CHAIN_NAME} recipient wallet address...`}
                    onChange={(event) => setRecipientAddress(event.target.value)}
                    value={recipientAddress}
                />
            </div>
            <div className="flex flex-col md:flex-row mt-4 text-2xl w-full max-w-xl justify-between">
                <div className="relative rounded-full shadow-sm md:mr-2">
                    <input
                        type="number"
                        id="send-amount"
                        className="input input-bordered focus:input-primary input-lg w-full pr-24 rounded-full text-center font-mono text-lg"
                        placeholder="Amount..."
                        step="0.1"
                        onChange={(event) => setSendAmount(event.target.value)}
                        value={sendAmount}
                    />
                    <span className="absolute top-0 right-0 bottom-0 px-4 py-5 rounded-r-full bg-secondary text-base-100 text-sm">
                        {convertFromMicroDenom(PUBLIC_STAKING_DENOM)}
                    </span>
                </div>
                <button
                    className="mt-4 md:mt-0 btn btn-primary btn-lg font-semibold hover:text-base-100 text-2xl rounded-full flex-grow"
                    onClick={handleSend}
                >
                    SEND
                </button>
            </div>
            <div className="mt-4 flex flex-col w-full max-w-xl">
                {success.length > 0 && (
                    <div className="alert alert-success">
                        <div className="flex-1 items-center">
                            <label className="flex-grow break-all">{success}</label>
                        </div>
                    </div>
                )}
                {error.length > 0 && (
                    <div className="alert alert-error">
                        <div className="flex-1 items-center">
                            <label className="flex-grow break-all">{error}</label>
                        </div>
                    </div>
                )}
            </div>
        </WalletLoader>
    )
}

export default Send
NFT Management Page
pages/nft.tsx
typescript
import { useEffect, useState } from 'react'
import type { NextPage } from 'next'
import { sha256 } from 'js-sha256'

import WalletLoader from 'components/WalletLoader'
import { useSigningClient } from 'contexts/client'
import { QueryNFTsResponse } from "../coreum/proto-ts/coreum/nft/v1beta1/query";
import { AssetNFT as AssetNFTTx, NFT as NFTTx } from "../coreum/tx";
import { EncodeObject } from "@cosmjs/proto-signing";

const nftClassSymbol = `kittens${Date.now()}`

const generateKittenURL = () => {
    return `https://placekitten.com/${200 + Math.floor(Math.random() * 100)}/${200 + Math.floor(Math.random() * 100)}`
}

const NFT: NextPage = () => {
    const { walletAddress, signingClient, coreumQueryClient } = useSigningClient()
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState('')
    const [classCreated, setClassCreated] = useState(false)
    const [nftClassDescription, setNFTClassDescription] = useState('')
    const [nfts, setNfts] = useState<{ classId: string; id: string, uri: string, uriHash: string, owner: string }[]>([])
    const [kittenURI, setKittenURI] = useState(generateKittenURL())
    const [transferID, setTransferID] = useState("")
    const [recipientAddress, setRecipientAddress] = useState('')
    const nftClassID = `${nftClassSymbol}-${walletAddress}`

    useEffect(() => {
        if (!signingClient || walletAddress.length === 0) {
            return
        }
        setError('')
        setLoading(true)
        queryClass()
    }, [signingClient, walletAddress])

    const queryNFTs = () => {
        setLoading(true)
        coreumQueryClient?.NFTClient().NFTs({
            classId: nftClassID,
            owner: "",
        }).then(async (res: QueryNFTsResponse) => {
            const nfts = await Promise.all(
                res.nfts.map(async (nft) => {
                    const resOwner = await coreumQueryClient?.NFTClient().Owner({
                        classId: nft.classId,
                        id: nft.id
                    })
                    return {
                        classId: nft.classId,
                        id: nft.id,
                        uri: nft.uri,
                        uriHash: nft.uriHash,
                        owner: resOwner.owner,
                    }
                })
            )
            nfts.sort((a, b) => a.id.localeCompare(b.id))
            setNfts(nfts)
            setLoading(false)
        })
        .catch((error) => {
            setLoading(false)
            setError(`Error! ${error.message}`)
        })
    }

    const queryClass = () => {
        coreumQueryClient?.NFTClient().Class({ classId: nftClassID }).then(() => {
            queryNFTs()
            setClassCreated(true)
        }).catch((error) => {
            setLoading(false)
            if (error.message.includes("not found class")) {
                setClassCreated(false)
                return
            }
            setError(`Error! ${error.message}`)
        })
    }

    const createNFTClass = () => {
        setError('')
        setLoading(true)

        sendTx([AssetNFTTx.MsgIssueClass({
            issuer: walletAddress,
            symbol: nftClassSymbol,
            description: nftClassDescription,
        })]).then((passed) => {
            setClassCreated(passed)
        })
    }

    const changeKitten = () => {
        setKittenURI(generateKittenURL())
    }

    const mintKitten = () => {
        setError('')
        setLoading(true)
        sendTx([AssetNFTTx.MsgMint({
            sender: walletAddress,
            classId: nftClassID,
            id: `kitten-${Date.now()}`,
            uri: kittenURI,
            uriHash: sha256.create().update(kittenURI).hex()
        })]).then((passed) => {
            if (passed) {
                queryNFTs()
            }
        })
    }

    const cancelTransferOwnership = () => {
        setError('')
        setTransferID('')
        setRecipientAddress('')
    }

    const transferOwnership = () => {
        setError('')
        setLoading(true)
        sendTx([NFTTx.MsgSend({
            sender: walletAddress,
            classId: nftClassID,
            id: transferID,
            receiver: recipientAddress,
        })]).then((passed) => {
            if (passed) {
                cancelTransferOwnership()
                queryNFTs()
            }
        })
    }

    const sendTx = async (msgs: readonly EncodeObject[]) => {
        try {
            const resp = await signingClient?.signAndBroadcast(walletAddress, msgs, 'auto')
            console.log(`Tx hash: ${resp?.transactionHash}`)
            setLoading(false)
            return true
        } catch (error: any) {
            console.error(error)
            setLoading(false)
            setError(`Error! ${error}`)
            return false
        }
    }

    return (
        <WalletLoader loading={loading}>
            {error.length > 0 && (
                <div className="alert alert-error">
                    <label className="flex-grow break-all">{error}</label>
                </div>
            )}
            {transferID == "" && !classCreated && (
                <div>
                    <h1 className="text-3xl font-bold my-8">
                        Create your {nftClassSymbol} NFT class
                    </h1>
                    <div className="flex w-full max-w-xl">
                        <input
                            type="text"
                            id="description"
                            className="input input-bordered focus:input-primary input-lg rounded-full flex-grow font-mono text-center text-lg"
                            placeholder="Class description"
                            onChange={(event) => setNFTClassDescription(event.target.value)}
                            value={nftClassDescription}
                        />
                        <button
                            className="mt-4 md:mt-0 btn btn-primary btn-lg font-semibold hover:text-base-100 text-2xl rounded-full flex-grow"
                            onClick={createNFTClass}
                        >
                            Create
                        </button>
                    </div>
                </div>
            )}
            {transferID == "" && classCreated && (
                <div>
                    <h1 className="text-3xl font-bold py-4">
                        Welcome to your {nftClassSymbol} collection!
                    </h1>
                    <h1 className="text-m italic pb-4">
                        {nftClassDescription}
                    </h1>
                    <div className="grid grid-flow-col auto-cols-max">
                        <div>
                            <table className="table">
                                <thead>
                                    <tr>
                                        <th className="w-24">Image</th>
                                        <th className="w-40">ID</th>
                                        <th className="w-40">Owner</th>
                                        <th className="w-96">Hash</th>
                                        <th className="w-24"></th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {nfts.map((l, k) => (
                                        <tr key={k}>
                                            <td>
                                                <div className="flex items-center space-x-3 w-24">
                                                    <div className="avatar">
                                                        <div className="mask mask-squircle w-12 h-12">
                                                            <img src={l.uri} alt="Images" />
                                                        </div>
                                                    </div>
                                                </div>
                                            </td>
                                            <td className="font-bold">{l.id}</td>
                                            <td className="truncate w-40">{l.owner}</td>
                                            <td><p className="truncate w-96">{l.uriHash}</p></td>
                                            <td className="w-24">
                                                {walletAddress == l.owner && (
                                                    <button className="btn btn-primary rounded-full"
                                                            onClick={() => setTransferID(l.id)}>Transfer</button>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                        <div className="ml-8">
                            <img className="rounded-full object-cover h-48 w-48" src={kittenURI} alt="" />
                            <div className="py-8">
                                <button className="btn btn-primary float-left btn-accent rounded-full" onClick={changeKitten}>
                                    Change
                                </button>
                                <button className="btn btn-primary float-right rounded-full" onClick={mintKitten}>
                                    Mint
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}
            {transferID != "" && classCreated && (
                <div>
                    <h1 className="text-3xl font-bold py-4">
                        Transfer {transferID} NFT ownership.
                    </h1>
                    <div className="flex w-full max-w-xl">
                        <input
                            type="text"
                            id="recipient-address"
                            className="input input-bordered focus:input-primary input-lg rounded-full flex-grow font-mono text-center text-lg"
                            placeholder="Recipient address"
                            onChange={(event) => setRecipientAddress(event.target.value)}
                            value={recipientAddress}
                        />
                    </div>
                    <div>
                        <div className="flex flex-col md:flex-row mt-4 text-2xl w-full max-w-xl justify-between">
                            <button
                                className="mt-4 md:mt-0 btn btn-secondary btn-lg font-semibold hover:text-base-100 text-2xl rounded-full flex-grow"
                                onClick={cancelTransferOwnership}
                            >
                                Cancel
                            </button>
                            <button
                                className="mt-4 md:mt-0 btn btn-primary btn-lg font-semibold hover:text-base-100 text-2xl rounded-full flex-grow"
                                onClick={transferOwnership}
                            >
                                Transfer
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </WalletLoader>
    )
}

export default NFT
Utility Functions
util/conversion.ts
typescript
export const convertMicroDenomToDenom = (value: number | string): number => {
    if (typeof value === 'string') {
        value = Number(value)
    }
    return value / 1000000
}

export const convertDenomToMicroDenom = (value: number | string): string => {
    if (typeof value === 'string') {
        value = Number(value)
    }
    return String(value * 1000000)
}

export const convertFromMicroDenom = (denom: string): string => {
    return denom.replace(/^u/, '')
}

export const convertToMicroDenom = (denom: string): string => {
    return `u${denom}`
}
Project Structure
text
my-webapp/
├── components/
│   ├── Layout.tsx
│   ├── Loader.tsx
│   ├── Nav.tsx
│   └── WalletLoader.tsx
├── contexts/
│   └── client.tsx
├── coreum/
│   ├── proto-ts/
│   ├── query.ts
│   └── tx.ts
├── pages/
│   ├── _app.tsx
│   ├── _document.tsx
│   ├── index.tsx
│   ├── nft.tsx
│   └── send.tsx
├── services/
│   └── keplr.tsx
├── styles/
│   ├── globals.css
│   └── daisyui-themes.json
├── util/
│   └── conversion.ts
├── .env.development
├── package.json
└── tsconfig.json
Running the Application
bash
# Install dependencies
yarn install

# Run development server
yarn dev

# Build for production
yarn build

# Start production server
yarn start
Next Steps
Read TX Modules Specification

Read CosmJS Documentation

Check Keplr Wallet Documentation

Explore Next.js Documentation
