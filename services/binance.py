import httpx
from datetime import datetime
import asyncio

BinanceUrl="https://fapi.binance.com/fapi/v1/exchangeInfo"
PriceUrl="https://fapi.binance.com/fapi/v2/ticker/price"

async def getCoins():
   
    async with httpx.AsyncClient(timeout=20) as client:
        coins=[]
        res = await client.get(BinanceUrl) #call to futures api
        res.raise_for_status() 
        data = res.json() #conversion of response into json
#Loop to iterate over all the data to clean and save into the list
        for i in data["symbols"]:
           # I put this condition to filter USDT pairs and active trading pairs on futures 
            if i["quoteAsset"] == "USDT" and i["status"] == "TRADING":
                print(i["symbol"],i["baseAsset"],i["underlyingType"],i["underlyingSubType"],datetime.fromtimestamp(i["onboardDate"]/1000,tz=None))
                # Saving each coin in dictionary first
                coin = {
                "symbol": i["symbol"],
                "base_asset": i["baseAsset"],
                "underlying_type": i["underlyingType"],
                "underlying_sub_type": i["underlyingSubType"],
                "onboardDate": datetime.fromtimestamp(i["onboardDate"]/1000,tz=None)
            }
                #Then i am appending the each coin dict. into list 
                coins.append(coin)

        print("There are "+ str(len(data["symbols"]))+ " coins in USDT pairs in Futures")
        return coins


async def getCurrentPrice():
    prices=[]
    

    async with httpx.AsyncClient(timeout=20) as client:
        prices=[]
        res = await client.get(PriceUrl)
        res.raise_for_status()
        data = res.json()
        for i in data:
            if i["symbol"].endswith("USDT"):
                price={
                    'symbol': i["symbol"],
                    'price':  i["price"],
                    'time':   datetime.fromtimestamp(i["time"]/1000,tz=None)

                }
                prices.append(price)
                
        # print(data)
        print(len(prices))
        return prices    
 
        

async def cleanData():
    coins, prices = await asyncio.gather(
        getCoins(),
        getCurrentPrice()
    )

    # Convert prices list into dictionary
    price_map = {p["symbol"]: p for p in prices}

    merged = []

    for coin in coins:
        symbol = coin["symbol"]

        if symbol in price_map:
            merged_coin = {
                **coin,   # all coin data
                "price": price_map[symbol]["price"],
                "time": price_map[symbol]["time"],

            }
            merged.append(merged_coin)
        


    print(f"Total merged: {len(merged)}")
    return coins,merged




# key for coingecko CG-en4jNGLUAFBzhUAWUR1DZiJU