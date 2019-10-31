# bitcoin_analysis
Analytics on BTC price and other metrics.

# Data
Uses data from Bitfinex, collected with the [bitfinex-ohlc-import](https://github.com/nateGeorge/bitfinex_ohlc_import) repo.

# Analysis

## Mayer multiple
Trace Mayer's name has been used in the Mayer Multiple.  This is just the ratio of current price to a 200-day moving average of the price.  Trace says you should buy some when it's low (e.g. under 1) and sell some when high (e.g. over 3).  The `mayer_multiple.py` file looks into the mayer multiple, and where it currently is.