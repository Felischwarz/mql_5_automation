import MetaTrader5 as mt5

# Verbindung mit MetaTrader 5 herstellen
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

async def buy_now(item, tp_price, sl_price):
    print(f"Command: BUY NOW, Item: {item}, TP: {tp_price}, SL: {sl_price}")
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": item,
        "volume": 1.0,
        "type": mt5.ORDER_TYPE_BUY,
        "price": mt5.symbol_info_tick(item).ask,
        "sl": sl_price,
        "tp": tp_price,
        "magic": 234000,
        "comment": "buy now",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }
    result = mt5.order_send(request)
    print(result)

async def sell_limit(item, limit_price, tp_price, sl_price):
    print(f"Command: {item} SELL LIMIT, Price: {limit_price}, TP: {tp_price}, SL: {sl_price}")
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": item,
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

async def sell_stop(item, stop_price, tp_price, sl_price):
    print(f"Command: {item} SELL STOP, Price: {stop_price}, TP: {tp_price}, SL: {sl_price}")
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": item,
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

async def buy_stop(item, stop_price, tp_price, sl_price):
    print(f"Command: {item} BUY STOP, Price: {stop_price}, TP: {tp_price}, SL: {sl_price}")
    request = {
        "action": mt5.TRADE_ACTION_PENDING,
        "symbol": item,
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
        print("Keine offenen Trades gefunden.")

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
        print("Keine offenen Trades gefunden.")

async def close_trade(close_data):
    print(f"Command: CLOSE TRADE, Close Data: {close_data}")
    trades = mt5.positions_get()
    if trades:
        trade = trades[-1]  # Der letzte offene Trade
        ticket = trade.ticket

        volume = trade.volume
        if close_data.lower() != "full":
            volume = volume * (float(close_data.strip('%')) / 100)

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": ticket,
            "volume": volume,
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(trade.symbol).bid,
            "magic": 234000,
            "comment": "close trade",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        result = mt5.order_send(request)
        print(result)
    else:
        print("Keine offenen Trades gefunden.")

# Schließe die Verbindung zu MetaTrader 5, wenn das Script beendet wird
import atexit
atexit.register(mt5.shutdown)
