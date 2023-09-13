import MetaTrader5 as mt5
import asyncio

async def initializeMt5():
    # Verbindung mit MetaTrader 5 herstellen
    if not mt5.initialize():
        print("initialize() failed")
        mt5.shutdown()
    print("initialize() successful")
    await asyncio.sleep(1)


async def buy_now(tp_price, sl_price):
    tick_info = mt5.symbol_info_tick('XAUUSD')
    if tick_info is None:
        print(f"No info found for symbol 'XAUUSD'")
        return
    price = tick_info.ask

    print(f"Command: BUY NOW, Symbol: XAUUSD, TP: {tp_price}, SL: {sl_price}")
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": 'XAUUSD',
        "volume": 1.0,
        "type": mt5.ORDER_TYPE_BUY,
        "price": price,
        "sl": sl_price,
        "tp": tp_price,
        "magic": 234000,
        "comment": "buy now",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    print(result)

async def sell_limit(limit_price, tp_price, sl_price):
    print(f"Command: SELL LIMIT, Symbol: XAUUSD, Price: {limit_price}, TP: {tp_price}, SL: {sl_price}")
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": 'XAUUSD',
        "volume": 1.0,
        "type": mt5.ORDER_TYPE_SELL_LIMIT,
        "price": limit_price,
        "sl": sl_price,
        "tp": tp_price,
        "magic": 234000,
        "comment": "sell limit",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    print(result)

async def sell_stop(stop_price, tp_price, sl_price):
    print(f"Command: SELL STOP, Symbol: XAUUSD, Price: {stop_price}, TP: {tp_price}, SL: {sl_price}")
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": 'XAUUSD',
        "volume": 1.0,
        "type": mt5.ORDER_TYPE_SELL_STOP,
        "price": stop_price,
        "sl": sl_price,
        "tp": tp_price,
        "magic": 234000,
        "comment": "sell stop",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    print(result)

async def buy_stop(stop_price, tp_price, sl_price):
    print(f"Command: BUY STOP, Symbol: XAUUSD, Price: {stop_price}, TP: {tp_price}, SL: {sl_price}")
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": 'XAUUSD',
        "volume": 1.0,
        "type": mt5.ORDER_TYPE_BUY_STOP,
        "price": stop_price,
        "sl": sl_price,
        "tp": tp_price,
        "magic": 234000,
        "comment": "buy stop",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    print(result)

async def move_sl_to_be(new_sl_price):
    print(f"Command: MOVE SL TO B/E, New SL: {new_sl_price}")
    trades = mt5.positions_get()
    if trades:
        trade = trades[-1]  # Der letzte offene Trade
        ticket = trade.ticket

        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "position": ticket,
            "sl": new_sl_price,
            "tp": trade.tp,
            "magic": 234000,
            "comment": "move SL to B/E",
        }
        result = mt5.order_send(request)
        print(result)
    else:
        print("No open trades found.")

async def delete_buy_stops():
    print("Command: DELETE BUY STOPS")
    trades = mt5.orders_get()
    if trades:
        for trade in trades:
            if trade.type == mt5.ORDER_TYPE_BUY_STOP:
                request = {
                    "order": trade.ticket,
                    "action": mt5.TRADE_ACTION_REMOVE,
                }
                result = mt5.order_send(request)
                print(result)
    else:
        print("No BUY STOP orders found.")

async def close_trade(close_data):
    print(f"Command: CLOSE, Data: {close_data}")
    trades = mt5.positions_get()
    if trades:
        for trade in trades:
            if str(trade.ticket) in close_data:
                request = {
                    "action": mt5.TRADE_ACTION_DEAL,
                    "position": trade.ticket,
                    "volume": trade.volume,
                    "magic": 234000,
                    "comment": "close trade",
                    "type": mt5.ORDER_TYPE_SELL if trade.type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY,
                }
                result = mt5.order_send(request)
                print(result)
    else:
        print("No open trades found.")

# Nicht vergessen, die Verbindung am Ende zu schließen
mt5.shutdown()
