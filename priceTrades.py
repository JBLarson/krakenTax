#!/usr/bin/python3


import json
from kFuncs import *


# import kraken data
sortedTradesInAddr = 'data/sortedTrades.json'

with open(sortedTradesInAddr, 'r') as r:
	tradeData = json.load(r)



sortedSells, sortedBuys = tradeData['sell'], tradeData['buy']


# import coinGecko data
jsonInAddr = 'data/cryptoData.json'

with open(jsonInAddr, 'r') as f:
	geckoData = json.load(f)

gekkoKeys =geckoData.keys()


def gekkoPairFunc(gekkoKeys):
	gekkoDicts = []

	for key in gekkoKeys:
		gekkoDict = {}
		if 'Usd' in key:
			splitKey = key.split('Usd')
			keyQuote = splitKey[0]
			keyBase = 'Usd'
		if 'Eur' in key:
			splitKey = key.split('Eur')
			keyQuote = splitKey[0]
			keyBase = 'Eur'

		gekkoDict = {'pair': key, 'quote': keyQuote, 'base': keyBase}
		gekkoDicts.append(gekkoDict)

	return gekkoDicts

gekkoPairs = gekkoPairFunc(gekkoKeys)



def mdyToYMD(ogDate):
	if '/' in ogDate:
		ogDateSplit = ogDate.split("/")
	elif '-' in ogDate:
		ogDateSplit = ogDate.split('-')
	if ogDateSplit[0] == '2021' or ogDateSplit[0] == '2020':
		ymdOutput = ogDate
	else:
		print(ogDateSplit)
		if len(ogDateSplit[0]) == 1:	month = '0' + str(ogDateSplit[0])
		else:	month = ogDateSplit[0]
		if len(ogDateSplit[1]) == 1:	day = '0' + str(ogDateSplit[1])
		else:	day = ogDateSplit[1]
		if len(ogDateSplit[2]) == 2:	year = '20' + str(ogDateSplit[2])
		else:	year = ogDateSplit[2]


		ymdOutput = str(year) + '-' + str(month) + '-' + str(day)
	return ymdOutput




def getPairPrice(quote, base, targetDate):
	pair = str(quote.capitalize()) + str(base.capitalize())
	targetPrice = "Couldn't find date"

	pairData = geckoData[pair]
	pairData = pairData['data']
	for dailyData in pairData:
		dailyDateShort = dailyData[:10]
		if dailyDateShort != targetDate:
			pass
		elif dailyDateShort == targetDate:
			targetPrice = pairData[dailyData]
	return targetPrice












def priceTradeList(sortedTradeData):
	symbolList = []
	tradeKeys = sortedTradeData.keys()
	for key in tradeKeys:
		if key == "XETHZ":	key = "ETH"
		if key == "XXBTZ":	key = "BTC"
		if key == "XXMRZ":	key = "XMR"

		symbolList.append(key)
	return symbolList



gekkoPairValueList = []
for gekkoPair in gekkoPairs:
	gekkoPairValue = gekkoPair['pair']
	gekkoPairValueList.append(gekkoPairValue)



def getHistSymbolPrice(tradeSymbol, tradeDate):
	symbolUsdPair = str(tradeSymbol).capitalize() + str('Usd')
	try:
		histSymbol = geckoData[symbolUsdPair]['data'][tradeDate]

	except Exception as e:
		print("Error finding historical data for: " + str(tradeSymbol))
		print("Error msg: " + str(e))
		histSymbol = 'histPrice error'
	
	return histSymbol


# need to seperate histQuote and histBase functions
def sortingFunction(sortedTradeData):
	tradeList, symbolList = [], {}

	tradeKeys = sortedTradeData.keys()

	for key in tradeKeys:
		keyTradeData = sortedTradeData[key]
		#print("\n\nTrades for: " + str(key))
		for trade in keyTradeData:
			tradeDate = mdyToYMD(trade['date'])
			tradeDate = str(tradeDate)
			tradeBase = trade['base'].capitalize()
			tradeQuote = trade['quote'].capitalize()
			pair = trade['quote'].capitalize() + tradeBase
			

			if pair in gekkoPairValueList:

				currentHistData = geckoData[pair]
				currentTrade = currentHistData['data']
				currentHistQuote = currentTrade[tradeDate]
				trade['histQuote'] = currentHistQuote
				tradeList.append(trade)
			elif pair not in gekkoPairValueList:
				#print("Pair not in gekkoPairs: " +str(pair))
				tradeList.append(trade)



	return tradeList

		#currentTradeList = sortedTradeData[trade]

	#return currentTradeList


sortedBuyOrders = sortingFunction(sortedBuys)

sortedSellOrders = sortingFunction(sortedSells)




def quoteBaseFunc(sortedOrders):
	pricedSortedOrders = []
	for order in sortedOrders:
		

		orderBase = order['base']
		orderQuote = order['quote']
		orderDate = mdyToYMD(order['date'])
		orderHistQuote = order['histQuote']

		if orderBase == 'USD' or orderBase == 'DAI':
			order['histBase'] = 1

		elif orderBase != 'USD' and orderBase != 'EUR':

			histPrice = getHistSymbolPrice(orderBase, orderDate)
			order['histBase'] = histPrice

		if orderQuote == 'USD' or orderQuote == 'DAI':
			order['histQuote'] = 1

		elif orderHistQuote == '':

			histPrice = getHistSymbolPrice(orderQuote, orderDate)
			order['histQuote'] = histPrice


		pricedSortedOrders.append(order)
	return pricedSortedOrders





pricedSortedSells = quoteBaseFunc(sortedSellOrders)
pricedSortedBuys = quoteBaseFunc(sortedBuyOrders)



daiEurDict = geckoData['DaiEur']['data']


def addEuroPricing(trade):
	baseCurrency = trade['base']
	tradeDate = trade['date']
	if baseCurrency == 'EUR':
		ymdTradeDate = mdyToYMD(tradeDate)
		histEuroPrice = daiEurDict[ymdTradeDate]
		trade['histBase'] = histEuroPrice	



for trade in pricedSortedBuys:
	addEuroPricingTest = addEuroPricing(trade)

for trade in pricedSortedSells:
	addEuroPricingTest = addEuroPricing(trade)





"""
# uncomment to display trade data

print("\n\nBuy Trades")

for trade in pricedSortedBuys:
	print("\n\n")
	print(trade)

print("\n\nSell Trades")
for trade in pricedSortedSells:
	print("\n\n")
	print(trade)

"""



exportDict = {"buy": pricedSortedBuys, "sell": pricedSortedSells}



jsonOutAddr = 'data/pricedTrades.json'
try:
	with open(jsonOutAddr, 'w') as fp1: json.dump(exportDict, fp1)

	print("\nSuccess Creating Sorted Trade JSON file at: " + str(jsonOutAddr) + '\n')


except Exception as e: print(e)


