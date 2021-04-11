import yfinance as yf

# TODO: use yfinance to look up historical data and other shit for a ticker in question 
# can probably check tickers based on industry + whatever stuff was found in the ticker analytics excel file
# maybe apply some indicators detailed here https://www.visualcapitalist.com/12-types-technical-indicators-stocks/ 
    # trend (overbought vs oversold -- breakout vs return to normal)
    # momentum (direction + strength of current price trend) e.g. RSI
    # volatility 
    # volume (relationship b/w price + volume -- good for adv forecasting?)
    # e.g. RSI + OBV + ichimoku cloud / bollinger bands (5 day chart? above band correct, below band rally)
# some rules
    # find currency in up/down trend
    # currency must fall back (from uptrend) and touch / almost touch bottom band
    # once price hits lower band, look @ RSI -- want b/w 30 - 50 and rising
    # make entry when you see strong bullish candle + consec reversal candles
    # create stop loss (30 - 50 pip) / take profit to target