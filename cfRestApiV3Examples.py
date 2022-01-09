# Crypto Facilities Ltd REST API V3

# Copyright (c) 2018 Crypto Facilities

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
# IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import cfRestApiV3 as cfApi
import datetime
import json

# accessible on your Account page under Settings -> API Keys
apiPublicKey = "8FguqWVfWBjF8gHVQqmSaTdf87KyRbmZmTMI0UUBS+p2hKd9nxgrI8bq"
# accessible on your Account page under Settings -> API Keys
apiPrivateKey = "6DbvgeXIRndiNmSW0JrxGuPNwJNPBuq9QOk02n6z0jsiBDG4w9qxQ3DGBh7S4TcZ6AiohhLqcvKdm7ITsWPO5eBd"

# use "api.cryptofacilities.com" if your IP is whitelisted (Settings -> API Keys -> IP Whitelist)
apiPath = "https://demo-futures.kraken.com"
timeout = 20
checkCertificate = True  # when using the test environment, this must be set to "False"
useNonce = False  # nonce is optional

cfPublic = cfApi.cfApiMethods(
    apiPath, timeout=timeout, checkCertificate=checkCertificate)
cfPrivate = cfApi.cfApiMethods(apiPath, timeout=timeout, apiPublicKey=apiPublicKey,
                               apiPrivateKey=apiPrivateKey, checkCertificate=checkCertificate, useNonce=useNonce)


def my_print(header, resp = None, is_index = False):
    line = header
    
    if not (resp is None):
        try:
            line += json.dumps(json.loads(resp), indent = 1)
        except TypeError:
            if (line != ''): 
                if is_index:
                    print(header, end = '')
                else:
                    print(header)
                    
            line = ''
            if type(resp) == list:
                for ind in range(len(resp)):
                    print(str(ind) + ' : ', resp[ind], is_index = True)
            else:
                line += str(resp)
        except json.JSONDecodeError:
            line += resp
    
    print(line)


def APITester():
    ##### public endpoints #####

    # get instruments
    result = cfPublic.get_instruments()
    my_print("get_instruments:\n", result)

    # get tickers
    result = cfPublic.get_tickers()
    my_print("get_tickers:\n", result)

    # get order book
    symbol = "PI_XBTUSD"
    result = cfPublic.get_orderbook(symbol)
    my_print("get_orderbook:\n", result)

    # get history
    symbol = "PI_XBTUSD"  # "PI_XBTUSD", "cf-bpi", "cf-hbpi"
    lastTime = datetime.datetime.strptime(
        "2016-01-20", "%Y-%m-%d").isoformat() + ".000Z"
    result = cfPublic.get_history(symbol, lastTime=lastTime)
    my_print("get_history:\n", result)

    # get prices
    result = cfPublic.get_market_price(symbol)
    my_print("get_market_price:\n", "%s elements" % len(result))

    ##### private endpoints #####

    # get account
    result = cfPrivate.get_accounts()
    my_print("get_accounts:\n", result)

    # send limit order
    limit_order = {
        "orderType": "lmt",
        "symbol": "PI_XBTUSD",
        "side": "buy",
        "size": 1,
        "limitPrice": 1.00,
        "reduceOnly": "false"
    }
    result = cfPrivate.send_order_1(limit_order)
    my_print("send_order (limit):\n", result)

    # send stop reduce-only order
    stop_order = {
        "orderType": "stp",
        "symbol": "PI_XBTUSD",
        "side": "buy",
        "size": 1,
        "limitPrice": 1.00,
        "stopPrice": 2.00,
        "cliOrdId": "my_stop_client_id"
    }
    result = cfPrivate.send_order_1(stop_order)
    my_print("send_order (stop):\n", result)

    edit = {
        "cliOrdId": "my_stop_client_id",
        "size": 2,
        "limitPrice": 1.50,
        "stopPrice": 2.50,
    }
    result = cfPrivate.edit_order(edit)
    my_print("edit_order (stop):\n", result)

    # cancel order
    order_id = "e35d61dd-8a30-4d5f-a574-b5593ef0c050"
    result = cfPrivate.cancel_order(order_id)
    my_print("cancel_order:\n", result)

    # cancel all orders of a margin account
    result = cfPrivate.cancel_all_orders(symbol="fi_xbtusd")
    my_print("cancel_all_orders:\n", result)

    # cancel all orders after a minute
    timeout_in_seconds = 60
    result = cfPrivate.cancel_all_orders_after(timeout_in_seconds)
    my_print("cancel_all_orders_after:\n", result)

    # batch order
    jsonElement = {
        "batchOrder":
            [
                {
                    "order": "send",
                    "order_tag": "1",
                    "orderType": "lmt",
                    "symbol": "PI_XBTUSD",
                    "side": "buy",
                    "size": 1,
                    "limitPrice": 1.00,
                    "cliOrdId": "my_another_client_id"
                },
                {
                    "order": "send",
                    "order_tag": "2",
                    "orderType": "stp",
                    "symbol": "PI_XBTUSD",
                    "side": "buy",
                    "size": 1,
                    "limitPrice": 2.00,
                    "stopPrice": 3.00,
                },
                {
                    "order": "cancel",
                    "order_id": "e35d61dd-8a30-4d5f-a574-b5593ef0c050",
                },
                {
                    "order": "cancel",
                    "cliOrdId": "my_client_id",
                },
            ],
    }
    result = cfPrivate.send_batchorder(jsonElement)
    my_print("send_batchorder:\n", result)

    # get open orders
    result = cfPrivate.get_openorders()
    my_print("get_openorders:\n", result)

    # get fills
    lastFillTime = datetime.datetime.strptime(
        "2016-02-01", "%Y-%m-%d").isoformat() + ".000Z"
    result = cfPrivate.get_fills(lastFillTime=lastFillTime)
    my_print("get_fills:\n", result)

    # get open positions
    result = cfPrivate.get_openpositions()
    my_print("get_openpositions:\n", result)

    # get historical orders since start of the year
    since = datetime.datetime(2021, 1, 1).timestamp()
    since = int(since) * 1000
    result = cfPrivate.get_orders(since=since, sort="asc", limit=10000)
    my_print("get_orders(since=%d, sort=\"asc\", limit=10000):\n" % since, "%s elements" % len(result))

    # get recent orders
    result = cfPrivate.get_orders()
    my_print("get_orders:\n", "%s elements" % len(result))

    # get historical executions since start of the year
    since = datetime.datetime(2021, 1, 1).timestamp()
    since = int(since) * 1000
    result = cfPrivate.get_executions(since=since, sort="asc", limit=10000)
    my_print("get_executions(since=%d, sort=\"asc\", limit=10000):\n" % since, "%s elements" % len(result))

    # get recent executions
    result = cfPrivate.get_executions()
    my_print("get_executions:\n", "%s elements" % len(result))

    # get historical executions since start of the year
    since = datetime.datetime(2021, 1, 1).timestamp()
    since = int(since) * 1000
    # result = cfPrivate.get_historical_executions(since=since)
    result = cfPrivate.get_executions(since=since)
    my_print("get_historical_executions:\n", "%s elements" % len(result))

    # get recent executions
    # result = cfPrivate.get_recent_executions()
    result = cfPrivate.get_executions()
    my_print("get_recent_executions:\n", "%s elements" % len(result))

    # send xbt withdrawal request
    targetAddress = "xxxxxxxxxx"
    currency = "xbt"
    amount = 0.12345678
    result = cfPrivate.send_withdrawal(targetAddress, currency, amount)
    my_print("send_withdrawal:\n", result)

    # get xbt transfers
    lastTransferTime = datetime.datetime.strptime(
        "2016-02-01", "%Y-%m-%d").isoformat() + ".000Z"
    result = cfPrivate.get_transfers(lastTransferTime=lastTransferTime)
    my_print("get_transfers:\n", result)

    # transfer
    fromAccount = "fi_ethusd"
    toAccount = "cash"
    unit = "eth"
    amount = 0.1
    result = cfPrivate.transfer(fromAccount, toAccount, unit, amount)
    my_print("transfer:\n", result)


APITester()
