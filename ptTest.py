#!/usr/bin/python3

import json

# import kraken data
sortedTradesInAddr = 'data/pricedTrades.json'

with open(sortedTradesInAddr, 'r') as r:
	tradeData = json.load(r)


buyTrades = tradeData['buy']

def testData(trade):
	histQuote = trade['histQuote']
	quoteCurrency, baseCurrency = trade['quote'], trade['base']
	histBase = trade['histBase']
	histPrices = {'quote': quoteCurrency, 'base': baseCurrency, 'basePrice': histBase, 'quotePrice': histQuote}

	missingData = None

	# if currency is usd and there's a historical quote price 
	if trade['base'] == 'USD':
		if trade['histQuote'] != '' and trade['histQuote'] != 'histPrice error':
			missingData = False
	
	# if currency is non-usd and there are historical base and quote prices
	if trade['base'] != 'USD':
		if trade['histQuote'] != '' and trade['histQuote'] != 'histPrice error':
			if trade['histBase'] != '' and trade['histBase'] != 'histPrice error':
				missingData = False
	
	if missingData != False:
		print('\n' + str(histPrices))
		print("There is missing data: " + str(missingData))


#for trade in buyTrades[-20:]:
for trade in buyTrades:

	pass

	#testTradeData = testData(trade)
