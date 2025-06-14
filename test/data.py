"""data/data.py\n
ctx_alphavantage: dict,\n
ctx_tiingo: dict,\n
ctx_yfinance: dict,\n
raw_alphavantage: list[dict],\n
raw_tiingo: list[dict],\n
raw_yfinance: dict,\n
parsed_alphavantage: dict,\n
parsed_tiingo: dict,\n
parsed_yfinance: dict,\n
"""

ctx_alphavantage = {
    'default': {'debug': True, 'work_dir': '/home/la/dev/stomartat/temp/', 'cfg_chart': '/home/la/dev/stomartat/src/pkg/chart_srv/cfg_chart.ini', 'cfg_data': '/home/la/dev/stomartat/src/pkg/data_srv/cfg_data.ini', 'cfg_main': '/home/la/dev/stomartat/src/config.ini'},
    'interface': {'command': 'data', 'data_line': ['CLOP', 'CLV', 'CWAP', 'HILO', 'VOLUME'], 'target_data': ['LQD'], 'arguments': ['EEM', 'IWM'], 'database': 'default.db', 'index': 0},
    'chart_service': {'adblock': '', 'chart_list': 'AFK ASEA', 'heatmap_list': '1W 1M 3M 6M', 'url_stockchart': 'https://stockcharts.com/sc3/ui/?s=AAPL', 'url_heatmap': 'https://stockanalysis.com/markets/heatmap/', 'webdriver': 'geckodriver'},
    'data_service': {'data_frequency': 'daily', 'data_line': 'CLOP CLV CWAP HILO VOLUME', 'data_list': 'EEM IWM', 'data_lookback': '7', 'data_provider': 'alphavantage', 'target_data': 'LQD', 'url_alphavantage': 'https://www.alphavantage.co', 'url_tiingo': 'https://api.tiingo.com/tiingo', 'url_yfinance': ''}
}
ctx_tiingo = {
    'default': {'debug': True, 'work_dir': '/home/la/dev/stomartat/temp/', 'cfg_chart': '/home/la/dev/stomartat/src/pkg/chart_srv/cfg_chart.ini', 'cfg_data': '/home/la/dev/stomartat/src/pkg/data_srv/cfg_data.ini', 'cfg_main': '/home/la/dev/stomartat/src/config.ini'},
    'interface': {'command': 'data', 'data_line': ['CLOP', 'CLV', 'CWAP', 'HILO', 'VOLUME'], 'target_data': ['LQD'], 'arguments': ['EEM', 'IWM'], 'database': 'default.db', 'index': 0},
    'chart_service': {'adblock': '', 'chart_list': 'AFK ASEA', 'heatmap_list': '1W 1M 3M 6M', 'url_stockchart': 'https://stockcharts.com/sc3/ui/?s=AAPL', 'url_heatmap': 'https://stockanalysis.com/markets/heatmap/', 'webdriver': 'geckodriver'},
    'data_service': {'data_frequency': 'daily', 'data_line': 'CLOP CLV CWAP HILO VOLUME', 'data_list': 'EEM IWM', 'data_lookback': '7', 'data_provider': 'tiingo', 'target_data': 'LQD', 'url_alphavantage': 'https://www.alphavantage.co', 'url_tiingo': 'https://api.tiingo.com/tiingo', 'url_yfinance': ''}
}
ctx_yfinance = {
    'default': {'debug': True, 'work_dir': '/home/la/dev/stomartat/temp/', 'cfg_chart': '/home/la/dev/stomartat/src/pkg/chart_srv/cfg_chart.ini', 'cfg_data': '/home/la/dev/stomartat/src/pkg/data_srv/cfg_data.ini', 'cfg_main': '/home/la/dev/stomartat/src/config.ini'},
    'interface': {'command': 'data', 'data_line': ['CLOP', 'CLV', 'CWAP', 'HILO', 'VOLUME'], 'target_data': ['LQD'], 'arguments': ['EEM', 'IWM'], 'database': 'default.db', 'index': 0},
    'chart_service': {'adblock': '', 'chart_list': 'AFK ASEA', 'heatmap_list': '1W 1M 3M 6M', 'url_stockchart': 'https://stockcharts.com/sc3/ui/?s=AAPL', 'url_heatmap': 'https://stockanalysis.com/markets/heatmap/', 'webdriver': 'geckodriver'},
    'data_service': {'data_frequency': 'daily', 'data_line': 'CLOP CLV CWAP HILO VOLUME', 'data_list': 'EEM IWM', 'data_lookback': '7', 'data_provider': 'yfinance', 'target_data': 'LQD', 'url_alphavantage': 'https://www.alphavantage.co', 'url_tiingo': 'https://api.tiingo.com/tiingo', 'url_yfinance': ''}
}
raw_alphavantage = {
    'Meta Data': {'1. Information': 'Daily Prices (open, high, low, close) and Volumes', '2. Symbol': 'IWM', '3. Last Refreshed': '2025-05-27', '4. Output Size': 'Compact', '5. Time Zone': 'US/Eastern'},
    'Time Series (Daily)': {
        '2025-05-23': {'1. open': '199.7800', '2. high': '203.2550', '3. low': '199.6500', '4. close': '202.5600', '5. volume': '29114602'},
        '2025-05-22': {'1. open': '202.2900', '2. high': '204.3700', '3. low': '201.5300', '4. close': '203.2000', '5. volume': '31831347'},
        '2025-05-21': {'1. open': '206.6300', '2. high': '207.6100', '3. low': '202.8400', '4. close': '203.2100', '5. volume': '36704354'},
        '2025-05-20': {'1. open': '208.6600', '2. high': '209.7550', '3. low': '207.9600', '4. close': '209.0800', '5. volume': '22053136'}
    }
}
raw_tiingo = [
    {'date': '2025-05-21T00:00:00.000Z', 'close': 203.21, 'high': 207.61, 'low': 202.84, 'open': 206.63, 'volume': 36704354, 'adjClose': 203.21, 'adjHigh': 207.61, 'adjLow': 202.84, 'adjOpen': 206.63, 'adjVolume': 36704354, 'divCash': 0.0, 'splitFactor': 1.0},
    {'date': '2025-05-22T00:00:00.000Z', 'close': 203.2, 'high': 204.37, 'low': 201.53, 'open': 202.29, 'volume': 31831347, 'adjClose': 203.2, 'adjHigh': 204.37, 'adjLow': 201.53, 'adjOpen': 202.29, 'adjVolume': 31831347, 'divCash': 0.0, 'splitFactor': 1.0},
    {'date': '2025-05-23T00:00:00.000Z', 'close': 202.56, 'high': 203.255, 'low': 199.65, 'open': 199.78, 'volume': 29114602, 'adjClose': 202.56, 'adjHigh': 203.255, 'adjLow': 199.65, 'adjOpen': 199.78, 'adjVolume': 29114602, 'divCash': 0.0, 'splitFactor': 1.0}
]
raw_yfinance = {
    "1747800000000":{"Open":206.6300048828,"High":207.6100006104,"Low":202.8399963379,"Close":203.2100067139,"Volume":36704400,"Dividends":0.0,"Stock Splits":0.0,"Capital Gains":0.0},
    "1747886400000":{"Open":202.2899932861,"High":204.3699951172,"Low":201.5299987793,"Close":203.1999969482,"Volume":31831300,"Dividends":0.0,"Stock Splits":0.0,"Capital Gains":0.0},
    "1747972800000":{"Open":199.7799987793,"High":203.2599945068,"Low":199.6499938965,"Close":202.5599975586,"Volume":29099500,"Dividends":0.0,"Stock Splits":0.0,"Capital Gains":0.0}
}
parsed_alphavantage = {
    1747800000: [20663, 20761, 20284, 20321, 36704354],
    1747886400: [20229, 20437, 20153, 20320, 31831347],
    1747972800: [19978, 20326, 19965, 20256, 29114602]
}
parsed_tiingo = {
    1747800000: [20663, 20761, 20284, 20321, 36704354],
    1747886400: [20229, 20437, 20153, 20320, 31831347],
    1747972800: [19978, 20326, 19965, 20256, 29114602]
    }
parsed_yfinance = {
    1747800000: [20663, 20761, 20284, 20321, 36704400],
    1747886400: [20229, 20437, 20153, 20320, 31831300],
    1747972800: [19978, 20326, 19965, 20256, 29099500]
}
