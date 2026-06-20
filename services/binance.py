# import httpx

# # BINANCE_URL = "https://api.binance.com/api/v3/exchangeInfo"

# BINANCE_URL = "https://fapi.binance.com/fapi/v1/exchangeInfo" #Futures URL

# async def get_usdt_pairs():
#     async with httpx.AsyncClient(timeout=20) as client:
#         res = await client.get(BINANCE_URL)
#         res.raise_for_status()

#         data = res.json()

#         return [
#             {
#                 "symbol": s["symbol"],
#                 "base": s["baseAsset"],
#                 "quote": s["quoteAsset"]
#             }
#             for s in data["symbols"]
#             if s["quoteAsset"] == "USDT"
#             and s["status"] == "TRADING"
#         ]

import httpx

BinanceUrl="https://fapi.binance.com/fapi/v1/exchangeInfo"

async def get_coins():
   
    async with httpx.AsyncClient(timeout=20) as client:
        coins=[]
        res = await client.get(BinanceUrl) #call to futures api
        res.raise_for_status() 
        data = res.json() #conversion of response into json
       
#Loop to iterate over all the data to clean and save into the list
        for i in data["symbols"]:
           # I put this condition to filter USDT pairs and active trading pairs on futures 
            if i["quoteAsset"] == "USDT" and i["status"] == "TRADING":
                print(i["symbol"],i["baseAsset"],i["underlyingType"],i["underlyingSubType"])
                # Saving each coin in dictionary first
                coin = {
                "symbol": i["symbol"],
                "base_asset": i["baseAsset"],
                "underlying_type": i["underlyingType"],
                "underlying_sub_type": i["underlyingSubType"]
            }
                #Then i am appending the each coin dict. into list 
                coins.append(coin)

        print("There are "+ str(len(data["symbols"]))+ " coins in USDT pairs in Futures")
        return coins
