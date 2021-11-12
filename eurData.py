#!/usr/bin/python3

import json
from kFuncs import *

# import coinGecko data
jsonInAddr = 'data/cryptoData.json'

with open(jsonInAddr, 'r') as f:
	geckoData = json.load(f)

daiEurDict = geckoData['DaiEur']['data']


# import kraken data
sortedTradesInAddr = 'data/pricedTrades.json'

with open(sortedTradesInAddr, 'r') as r:
	tradeData = json.load(r)

buyTrades, sellTrades = tradeData['buy'], tradeData['sell']


def addEuroPricing(trade):
	baseCurrency = trade['base']
	tradeDate = trade['date']
	if baseCurrency == 'EUR':
		ymdTradeDate = mdyToYMD(tradeDate)
		histEuroPrice = daiEurDict[ymdTradeDate]
		trade['histBase'] = histEuroPrice	



for trade in buyTrades:
	addEuroPricingTest = addEuroPricing(trade)

for trade in sellTrades:
	addEuroPricingTest = addEuroPricing(trade)

exportDict = {'buy': buyTrades, 'sell': sellTrades}


jsonOutAddr = 'data/pricedTrades2.json'
try:
	with open(jsonOutAddr, 'w') as fp1: json.dump(exportDict, fp1)

	print("\nSuccess Adding Euro Data to Trade JSON file at: " + str(jsonOutAddr) + '\n')


except Exception as e: print(e)

