#!/usr/bin/python3

import json

# import kraken data
sortedTradesInAddr = 'data/pricedTrades.json'

with open(sortedTradesInAddr, 'r') as r:
	tradeData = json.load(r)


buyTrades, sellTrades = tradeData['buy'], tradeData['sell']

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
	
	#if missingData != False:
		#print('\n' + str(histPrices))
		#print("There is missing data: " + str(missingData))
	return missingData

#for trade in buyTrades[-20:]:

# metrics for how complete trade data is


for trade in buyTrades:
	missingData = testData(trade)
	if missingData == None:
		print('\n')
		print(trade)


for trade in sellTrades:
	missingData = testData(trade)
	if missingData == None:
		print('\n')
		print(trade)




def missingDataStats():
	buyTests, sellTests = [], []
	for trade in buyTrades:
		testTradeData = testData(trade)
		buyTests.append(testTradeData)

	for trade in sellTrades:
		testTradeData = testData(trade)
		sellTests.append(testTradeData)


	missingBuy, missingSell = buyTests.count(None), sellTests.count(None)
	print("\nBuy Trade Errors: " + str(missingBuy) + " out of: " + str(len(buyTrades)))
	print("Sell Trade Errors: " + str(missingSell) + " out of: " + str(len(sellTrades)) + "\n")

testTrades = missingDataStats()
