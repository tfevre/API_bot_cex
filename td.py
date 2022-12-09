import requests, os, dotenv, sqlite3, hmac, time
from urllib.parse import urlencode
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

URL = "https://api.binance.com"

API_KEY = os.getenv('BINANCE_API_KEY')
API_SECRET = os.getenv('BINANCE_API_SECRET')


def getRequest(endpoint, params):

    headers  = {"Accept": "application/json"}

    resp = requests.get(URL + "/api/v3/"+endpoint, headers = headers, params=params)

    if resp.status_code != 200:
        print('error: ' + str(resp.status_code))
        print('error: ' + str(resp.text))
    else:
        return resp.json()

#   SLIDE 1 ###############################################
def allAvailableCrypto(): 
    data = getRequest('exchangeInfo', {})
    for d in data:
        if d == 'symbols':
            for token in data[d]:
                print(token['symbol'])

def getDepth(direction='asks', pair='BTCBUSD'):
    data = getRequest('depth', {"symbol": pair})
    if direction == 'asks':
        print('first : ', data['asks'][0])
        print('last : ',data['asks'][-1])
    else :
        print('first : ', data['bids'][0])
        print('last : ', data['bids'][-1])

def getOrderBook(pair='BTCBUSD'):
    data = getRequest('depth', {"symbol": pair})
    print('Ask : ', data['asks'][0])
    print('Bid : ', data['bids'][0])

#   SLIDE 2 ###############################################
def refreshDataCandle(pair='BTCBUSD', duration='5m'):
    data = getRequest('klines', {"symbol": pair, 'interval':duration})
    _date=str(data[0][0])
    _open=str(data[0][1])
    _high=str(data[0][2])
    _low=str(data[0][3])
    _close=str(data[0][4])
    _volume=str(data[0][5])
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * from temp WHERE last_check = "'+_date+'" AND trading_pair = "'+pair+'" AND duration = "'+duration+'"')
    last_date = cursorObj.fetchall()[0][-1]
    if last_date != _date:
        cursorObj.execute("INSERT INTO data_candles VALUES(null, "+_date+", "+_high+", "+_low+", "+_open+", "+_close+", "+_volume+")")
        cursorObj.execute("INSERT INTO temp VALUES(null, 'BINANCE', '"+pair+"', '"+duration+"', 'data_candles', "+_date+")")
        con.commit()

def refreshFulldata(pair='BTCBUSD'):
    data = getRequest('trades', {"symbol": pair})
    
    _id=str(data[0]['id'])
    _price=str(data[0]['price'])
    _qty=str(data[0]['qty'])
    _side=str(data[0]['isBuyerMaker'])
    _date=str(data[0]['time'])
   
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()
    cursorObj.execute('SELECT * from data_full WHERE uuid = "'+_id+'"')
    last_id = cursorObj.fetchall()
    if last_id != _id:
        cursorObj.execute("INSERT INTO data_full VALUES(null, '"+_id+"', '"+pair+"', "+_price+", "+_date+", '"+_qty+"', '"+_side+"')" )
        con.commit()

#   API ##################################################
def getRequestAPI(endpoint, params):

    headers  = {"Accept": "application/json", 'X-MBX-APIKEY': API_KEY}

    params['timestamp']= int(time.time() * 1000) - 3000
    signature_payload = urlencode(params)
    signature = hmac.new(API_SECRET.encode(), signature_payload.encode(), 'sha256').hexdigest()
    params['signature'] = signature
    resp = requests.get(URL + "/api/v3/"+endpoint, headers = headers, params=params)

    if resp.status_code != 200:
        print('error: ' + str(resp.status_code))
        print('error: ' + str(resp.text))
    else:
        return resp.json()

# data = getRequestAPI('openOrders', {"symbol": 'EURBUSD'})
# print(data)

def postRequest(endpoint, params):

    headers  = {"Accept": "application/json", 'X-MBX-APIKEY': API_KEY}

    params['timestamp']= int(time.time() * 1000) - 3000
    signature_payload = urlencode(params)
    signature = hmac.new(API_SECRET.encode(), signature_payload.encode(), 'sha256').hexdigest()
    params['signature'] = signature
    resp = requests.post(URL + "/api/v3/"+endpoint, headers = headers, params=params)

    if resp.status_code != 200:
        print('error: ' + str(resp.status_code))
        print('error: ' + str(resp.text))
    else:
        return resp.json()

def deleteRequest(endpoint, params):

    headers  = {"Accept": "application/json", 'X-MBX-APIKEY': API_KEY}

    params['timestamp']= int(time.time() * 1000) - 3000
    signature_payload = urlencode(params)
    signature = hmac.new(API_SECRET.encode(), signature_payload.encode(), 'sha256').hexdigest()
    params['signature'] = signature
    resp = requests.delete(URL + "/api/v3/"+endpoint, headers = headers, params=params)

    if resp.status_code != 200:
        print('error: ' + str(resp.status_code))
        print('error: ' + str(resp.text))
    else:
        return resp.json()


def createOrder(pair, side, _type, qty, price):
    # "/test" is added to avoid any unwanted orders
    data = postRequest('order/test', {"symbol": pair, 'side':side, 'type':_type, 'quantity':qty, 'price':price})
    print(data)

# createOrder('EURBUSD', 'BUY', 'MARKET', '10')

def cancelOrder(pair, orderID):
    # "/test" is added to avoid any unwanted orders
    data = deleteRequest('order', {"symbol": pair, 'orderId': orderID})
    print(data)


# cancelOrder('EURBUSD', '4')




