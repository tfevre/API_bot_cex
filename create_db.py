import sqlite3

#   DATABASE ##############################################
con = sqlite3.connect('mydatabase.db')
cursorObj = con.cursor()
# cursorObj.execute("DROP table if exists data_full")
cursorObj.execute("CREATE TABLE if not exists data_candles(id integer PRIMARY KEY AUTOINCREMENT, date integer, high real, low real, open real, close real, volume real)")
cursorObj.execute("CREATE TABLE if not exists data_full(id integer PRIMARY KEY AUTOINCREMENT, uuid text, traded_crypto text, price real, created_at integer, qty text, side text)")
cursorObj.execute("CREATE TABLE if not exists temp(id integer PRIMARY KEY AUTOINCREMENT, cex text, trading_pair text, duration text, table_name text, last_check integer)")
con.commit()