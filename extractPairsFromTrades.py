import json



# import symbolName data
symbolNamesInAddr = 'data/symbolNames.json'

with open(symbolNamesInAddr, 'r') as r:
	symbolNames = json.load(r)

# import kraken data
sortedTradesInAddr = 'data/trades3.json'

with open(sortedTradesInAddr, 'r') as r:
	tradeData = json.load(r)



def standardizeSymbols(symbol):
	if symbol.upper() == 'XETHZ':	symbol = 'ETH'
	#if symbol.upper() == 'DAI':	symbol = 'USD'
	if symbol.upper() == 'XBT':	symbol = 'BTC'
	if symbol.upper() == 'XXBTZ':	symbol = 'BTC'
	if symbol.upper() == 'XXMRZ':	symbol = 'XMR'
	return symbol



def pairExtractFunc(tradeData):

	tradePairs, tradeQuotes, tradeBases = [], [], []

	for trade in tradeData:

		tradeBase = trade['base']
		tradeQuote = trade['quote']
		tradePair = [tradeQuote, tradeBase]
		if tradePair not in tradePairs:
			tradePairs.append(tradePair)
		if tradeBase not in tradeBases:
			tradeBases.append(tradeBase)
		if tradeQuote not in tradeQuotes:
			tradeQuotes.append(tradeQuote)
		tradePairData = {'pairs': tradePairs, 'quotes': tradeQuotes, 'bases': tradeBases}
	return tradePairData



def symbolToNameFunc(tokenSymbol):
	symbolName = symbolNames[tokenSymbol]
	return symbolName





pairExtraction = pairExtractFunc(tradeData)

#pairExtraction.sort(reverse=False)

pairQuotes = pairExtraction['quotes']
pairBases = pairExtraction['bases']

def quoteNameFunc(pairSymbolList):	
	quoteNames = []
	for quoteSymbol in pairSymbolList:
		symbolName = symbolToNameFunc(quoteSymbol.capitalize())
		quoteNames.append(symbolName)
	return quoteNames

quoteNameList = quoteNameFunc(pairQuotes)
print(quoteNameList)