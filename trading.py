import MetaTrader5 as mt5

if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()

symbol = "AAPL"
lot = 0.1
point = mt5.symbol_info(symbol).point
price = mt5.symbol_info_tick(symbol).ask
deviation = 20
request = {
    "action": mt5.TRADE_ACTION_DEAL,
    "symbol": symbol,
    "volume": lot,
    "type": mt5.ORDER_TYPE_BUY,
    "price": price,
    "sl": price - 10 * point,
    "tp": price + 10 * point,
    "deviation": deviation,
    "magic": 123456,
    "comment": "test buy",
    "type_time": mt5.ORDER_TIME_GTC,
    "type_filling": mt5.ORDER_FILLING_IOC,
}

result = mt5.order_send(request)

if result.retcode != mt5.TRADE_RETCODE_DONE:
    print("Order failed, retcode={}".format(result.retcode))
else:
    print("Order executed, order ID={}".format(result.order))

mt5.shutdown()
