from BinaryOptionsToolsV2 import RawPocketOption
import json

# This file contains all the async code for the PocketOption Module
class PocketOptionAsync:
    def __init__(self, ssid: str):
        self.client = RawPocketOption(ssid)
        
    
    async def buy(self, asset: str, amount: float, time: int, check_win: bool = False):
        """
        Takes the asset, and amount to place a buy trade that will expire in time (in seconds).
        If check_win is True then the function will return a tuple containing the trade id and a dictionary containing the trade data and the result of the trade ("win", "draw", "loss)
        If check_win is False then the function will return a tuple with the id of the trade and the trade as a dict
        """
        (trade_id, trade) = await self.client.buy(asset, amount, time)
        if check_win:
            return await self.check_win(trade_id)   
        else:
            trade = json.loads(trade)
            return trade_id, trade 
       
    async def sell(self, asset: str, amount: float, time: int, check_win: bool = False):
        """
        Takes the asset, and amount to place a sell trade that will expire in time (in seconds).
        If check_win is True then the function will return a tuple containing the trade id and a dictionary containing the trade data and the result of the trade ("win", "draw", "loss)
        If check_win is False then the function will return a tuple with the id of the trade and the trade as a dict
        """
        (trade_id, trade) = await self.client.sell(asset, amount, time)
        if check_win:
            return trade_id, await self.check_win(trade_id)   
        else:
            trade = json.loads(trade)
            return trade_id, trade 
 
    async def check_win(self, id: str):
        """Returns a dictionary containing the trade data and the result of the trade ("win", "draw", "loss)"""
        trade = await self.client.check_win(id)
        trade = json.loads(trade)
        win = trade["profit"]
        if win > 0:
            trade["result"] = "win"
        elif win == 0:
            trade["result"] = "draw"
        else:
            trade["result"] = "loss"
        return trade
        
    async def get_candles(self, asset: str, period: int, offset: int):  
        """
        Takes the asset you want to get the candles and return a list of raw candles in dictionary format
        Each candle contains:
            * time: using the iso format
            * open: open price
            * close: close price
            * high: highest price
            * low: lowest price
        """
        candles = await self.client.get_candles(asset, period, offset)
        return json.loads(candles)
    
    async def balance(self):
        "Returns the balance of the account"
        return json.loads(await self.client.balance())["balance"]
    
    async def opened_deals(self):
        "Returns a list of all the opened deals as dictionaries"
        return json.loads(await self.client.opened_deals())
    
    async def closed_deals(self):
        "Returns a list of all the closed deals as dictionaries"
        return json.loads(await self.client.closed_deals())
    
    async def clear_closed_deals(self):
        "Removes all the closed deals from memory, this function doesn't return anything"
        await self.client.clear_closed_deals()

    async def payout(self, asset: None | str | list[str] = None):
        "Returns a dict of asset : payout for each asset, if 'asset' is not None then it will return the payout of the asset or a list of the payouts for each asset it was passed"
        payout = json.loads(await self.client.payout())
        if isinstance(asset, str):
            return payout.get(asset)
        elif isinstance(asset, list):
            return [payout.get(ast) for ast in asset]
        return payout
    
    async def history(self, asset: str, period: int):
        "Returns a list of dictionaries containing the latest data available for the specified asset starting from 'period', the data is in the same format as the returned data of the 'get_candles' function."
        return json.loads(await self.client.history(asset, period))
    
    async def _subscribe_symbol_inner(self, asset: str):
        return await self.client.subscribe_symbol(asset)
    
    async def subscribe_symbol(self, asset: str):
        """Returns an async iterator over the associated asset, it will return real time raw candles and will return new candles while the 'PocketOptionAsync' class is loaded if the class is droped then the iterator will fail"""
        return AsyncSubscription(await self._subscribe_symbol_inner(asset))
        
class AsyncSubscription:
    def __init__(self, subscription):
        self.subscription = subscription
        
    def __aiter__(self):
        return self
        
    async def __anext__(self):
        return json.loads(await anext(self.subscription))