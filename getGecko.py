#!/usr/bin/python3

import time
import datetime
import requests
import json



symbolNamesInAddr = 'data/symbolNames.json'

with open(symbolNamesInAddr, 'r') as r:
	symbolNames = json.load(r)



def unixToDatetime(epochTime):
	#localTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epochTime))

	localTime = time.strftime('%Y-%m-%d', time.localtime(epochTime))
	return localTime


def datetimeToUnix(ogDatetime):
	ogDatetime=datetime.datetime.strptime(ogDatetime, "%Y-%m-%d %H:%M:%S")
	epochTime = ogDatetime.strftime('%s')

	return epochTime


def oneYearAgo(ogDT):
	splitDT = ogDT.split("-")
	year = splitDT[0]
	
	restOfDt = str(splitDT[1]) +"-" + str(splitDT[2])
	yearMinusOne = int(year) - 1
	oneYearResult = str(yearMinusOne) + "-" + str(restOfDt)
	
	return oneYearResult


today = datetime.datetime.now()
today = str(today).split(".")
today = today[0]
oneYearAgo = oneYearAgo(today)

epochToday = datetimeToUnix(today)
epochOneYearAgo = datetimeToUnix(oneYearAgo)




def getCoinDict(coin, baseCurrency, fromTimeStamp, toTimestamp):
	from pycoingecko import CoinGeckoAPI
	cg = CoinGeckoAPI()

	coinApiRez = cg.get_coin_market_chart_range_by_id(id=coin, vs_currency=baseCurrency, from_timestamp=fromTimeStamp, to_timestamp=toTimestamp) # coin gecko coinApiRez
	coinRezPrices = coinApiRez['prices']
	priceDict = {}
	for price in coinRezPrices:
		
		unixTime = price[0]
		unixTime = int(str(unixTime)[:-3])
		price = price[1]
		localDT = unixToDatetime(unixTime)

		priceDict.update({localDT: price})

	returnDict = {"base": baseCurrency, "quote": coin, "data": priceDict}

	return returnDict



EthUsd, EthEur = getCoinDict('ethereum', 'usd', epochOneYearAgo, epochToday), getCoinDict('ethereum', 'eur', epochOneYearAgo, epochToday)
XmrUsd, XmrEur = getCoinDict('monero', 'usd', epochOneYearAgo, epochToday), getCoinDict('monero', 'eur', epochOneYearAgo, epochToday)
NanoUsd, NanoEur = getCoinDict('nano', 'usd', epochOneYearAgo, epochToday), getCoinDict('nano', 'eur', epochOneYearAgo, epochToday)
XtzUsd, XtzEur = getCoinDict('tezos', 'usd', epochOneYearAgo, epochToday), getCoinDict('tezos', 'eur', epochOneYearAgo, epochToday)
AlgoUsd, AlgoEur = getCoinDict('algorand', 'usd', epochOneYearAgo, epochToday), getCoinDict('algorand', 'eur', epochOneYearAgo, epochToday)
BtcUsd, BtcEur = getCoinDict('bitcoin', 'usd', epochOneYearAgo, epochToday), getCoinDict('bitcoin', 'eur', epochOneYearAgo, epochToday)
StorjUsd, StorjEur = getCoinDict('storj', 'usd', epochOneYearAgo, epochToday), getCoinDict('storj', 'eur', epochOneYearAgo, epochToday)
LskUsd, LskEur = getCoinDict('lisk', 'usd', epochOneYearAgo, epochToday), getCoinDict('lisk', 'eur', epochOneYearAgo, epochToday)
FilUsd, FilEur = getCoinDict('filecoin', 'usd', epochOneYearAgo, epochToday), getCoinDict('filecoin', 'eur', epochOneYearAgo, epochToday)
DotUsd, DotEur = getCoinDict('polkadot', 'usd', epochOneYearAgo, epochToday), getCoinDict('polkadot', 'eur', epochOneYearAgo, epochToday)
AdaUsd, AdaEur = getCoinDict('cardano', 'usd', epochOneYearAgo, epochToday), getCoinDict('cardano', 'eur', epochOneYearAgo, epochToday)
DaiEur = getCoinDict('dai', 'eur', epochOneYearAgo, epochToday)

#print(EthEur)




def symbolNameFunc(tokenSymbol):
	symbolName = symbolNames[tokenSymbol]
	return symbolName


def fetchTokenData(tokenSymbol):
	tokenName = symbolNameFunc(tokenSymbol)
	tokenUsd, tokenEur = getCoinDict(tokenName, 'usd', epochOneYearAgo, epochToday), getCoinDict(tokenName, 'eur', epochOneYearAgo, epochToday)
	tokenUsdEur = [tokenUsd, tokenEur]
	return tokenUsdEur






extractDict = {
	'BtcUsd': BtcUsd, 'BtcEur': BtcEur,
	'EthUsd': EthUsd, 'EthEur': EthEur,
	'NanoUsd': NanoUsd, 'NanoEur': NanoEur,
	'XmrUsd': XmrUsd, 'XmrEur': XmrEur,
	'XtzUsd': XtzUsd, 'XtzEur': XtzEur,
	'AlgoUsd': AlgoUsd, 'AlgoEur': AlgoEur,
	'StorjUsd': StorjUsd, 'StorjEur': StorjEur,
	'LskUsd': LskUsd, 'LskEur': LskEur,
	'FilUsd': FilUsd, 'FilEur': FilEur,
	'DotUsd': DotUsd, 'DotEur': DotEur,
	'XmrUsd': XmrUsd, 'XmrEur': XmrEur,
	'AdaUsd': AdaUsd, 'AdaEur': AdaEur,
	'DaiEur': DaiEur
}


jsonOutAddr = 'data/cryptoData' + '.json'
try:
	with open(jsonOutAddr, 'w') as fp1: json.dump(extractDict, fp1)

	print("\nSuccess Creating Crypto Json on/at: " + str(today))
except Exception as e:
	print(e)
