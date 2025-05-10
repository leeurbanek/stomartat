"""data/data.py\n
ctx: dict,\n
dict_list_eem: ,\n
dict_list_iwm: ,\n
parse_dict_eem: ,\n
parse_dict_iwm: ,\n
df_tuple_eem: ,\n
df_tuple_iwm:
"""

ctx = {
    'default': {
        'debug': True,
        'work_dir': '/home/la/dev/stomartat/temp/',
        'cfg_chart': '/home/la/dev/stomartat/src/pkg/chart_srv/cfg_chart.ini',
        'cfg_data': '/home/la/dev/stomartat/src/pkg/data_srv/cfg_data.ini',
        'cfg_main': '/home/la/dev/stomartat/src/config.ini'
    },
    'interface': {
        'command': 'data',
        'arguments': ['EEM', 'IWM'],
        'database': 'default.db'
    },
    'chart_service': {
        'adblock': '',
        'chart_list': 'EEM FXI IWM DBC HYG SPY IAU LQD MOO TIP IYR IYZ XLB XLE XLF XLI XLK XLP XLU XLV XLY BOTZ GBTC LIT XAR',
        'heatmap_list': '1W 1M 3M 6M',
        'url_stockchart': 'https://stockcharts.com/sc3/ui/?s=AAPL',
        'url_heatmap': 'https://stockanalysis.com/markets/heatmap/',
        'webdriver': 'geckodriver'
    },
    'data_service': {
        'data_list': 'EEM IWM',
        'data_lookback': '14',
        'data_frequency': 'daily',
        'data_provider': 'tiingo',
        'url_alphavantage': '',
        'url_tiingo': 'https://api.tiingo.com/tiingo',
        'url_yahoo': ''
    }
}

dict_list_eem = [
    {'date': '2025-04-21T00:00:00.000Z', 'close': 41.91, 'high': 42.215, 'low': 41.6112, 'open': 42.17, 'volume': 16440713, 'adjClose': 41.91, 'adjHigh': 42.215, 'adjLow': 41.6112, 'adjOpen': 42.17, 'adjVolume': 16440713, 'divCash': 0.0, 'splitFactor': 1.0},
    {'date': '2025-04-22T00:00:00.000Z', 'close': 42.54, 'high': 42.825, 'low': 42.3401, 'open': 42.375, 'volume': 25716059, 'adjClose': 42.54, 'adjHigh': 42.825, 'adjLow': 42.3401, 'adjOpen': 42.375, 'adjVolume': 25716059, 'divCash': 0.0, 'splitFactor': 1.0},
    {'date': '2025-04-23T00:00:00.000Z', 'close': 43.03, 'high': 43.52, 'low': 42.98, 'open': 43.29, 'volume': 24787365, 'adjClose': 43.03, 'adjHigh': 43.52, 'adjLow': 42.98, 'adjOpen': 43.29, 'adjVolume': 24787365, 'divCash': 0.0, 'splitFactor': 1.0},
    {'date': '2025-04-24T00:00:00.000Z', 'close': 43.53, 'high': 43.58, 'low': 43.1, 'open': 43.15, 'volume': 28843537, 'adjClose': 43.53, 'adjHigh': 43.58, 'adjLow': 43.1, 'adjOpen': 43.15, 'adjVolume': 28843537, 'divCash': 0.0, 'splitFactor': 1.0},
    {'date': '2025-04-25T00:00:00.000Z', 'close': 43.45, 'high': 43.45, 'low': 43.135, 'open': 43.22, 'volume': 18363715, 'adjClose': 43.45, 'adjHigh': 43.45, 'adjLow': 43.135, 'adjOpen': 43.22, 'adjVolume': 18363715, 'divCash': 0.0, 'splitFactor': 1.0}
]

dict_list_iwm = [
    {'date': '2025-04-21T00:00:00.000Z', 'close': 182.74, 'high': 185.29, 'low': 180.765, 'open': 185.0, 'volume': 26018999, 'adjClose': 182.74, 'adjHigh': 185.29, 'adjLow': 180.765, 'adjOpen': 185.0, 'adjVolume': 26018999, 'divCash': 0.0, 'splitFactor': 1.0},
    {'date': '2025-04-22T00:00:00.000Z', 'close': 187.47, 'high': 188.1, 'low': 184.55, 'open': 185.15, 'volume': 34477053, 'adjClose': 187.47, 'adjHigh': 188.1, 'adjLow': 184.55, 'adjOpen': 185.15, 'adjVolume': 34477053, 'divCash': 0.0, 'splitFactor': 1.0},
    {'date': '2025-04-23T00:00:00.000Z', 'close': 190.25, 'high': 195.51, 'low': 189.84, 'open': 192.92, 'volume': 44866133, 'adjClose': 190.25, 'adjHigh': 195.51, 'adjLow': 189.84, 'adjOpen': 192.92, 'adjVolume': 44866133, 'divCash': 0.0, 'splitFactor': 1.0},
    {'date': '2025-04-24T00:00:00.000Z', 'close': 194.06, 'high': 194.37, 'low': 189.89, 'open': 190.76, 'volume': 29820132, 'adjClose': 194.06, 'adjHigh': 194.37, 'adjLow': 189.89, 'adjOpen': 190.76, 'adjVolume': 29820132, 'divCash': 0.0, 'splitFactor': 1.0},
    {'date': '2025-04-25T00:00:00.000Z', 'close': 194.12, 'high': 194.26, 'low': 191.55, 'open': 192.72, 'volume': 25028968, 'adjClose': 194.12, 'adjHigh': 194.26, 'adjLow': 191.55, 'adjOpen': 192.72, 'adjVolume': 25028968, 'divCash': 0.0, 'splitFactor': 1.0}
]

parse_dict_eem = {
    739362: [4217, 4222, 4161, 4191, 16440713],
    739363: [4238, 4282, 4234, 4254, 25716059],
    739364: [4329, 4352, 4298, 4303, 24787365],
    739365: [4315, 4358, 4310, 4353, 28843537],
    739366: [4322, 4345, 4314, 4345, 18363715]
}

parse_dict_iwm = {
    739362: [18500, 18529, 18076, 18274, 26018999],
    739363: [18515, 18810, 18455, 18747, 34477053],
    739364: [19292, 19551, 18984, 19025, 44866133],
    739365: [19076, 19437, 18989, 19406, 29820132],
    739366: [19272, 19426, 19155, 19412, 25028968]
}

# df_tuple_eem = ('EEM',         open  high   low  close    volume
# date
# 739362  4217  4222  4161   4191  16440713
# 739363  4238  4282  4234   4254  25716059
# 739364  4329  4352  4298   4303  24787365
# 739365  4315  4358  4310   4353  28843537
# 739366  4322  4345  4314   4345  18363715
# 739369  4351  4358  4332   4353  11002235
# 739370  4359  4376  4356   4365  12809121
# 739371  4359  4383  4340   4376  20928833
# 739372  4393  4396  4370   4375  14740506
# 739373  4515  4517  4484   4500  33945930)

# df_tuple_iwm = ('IWM',          open   high    low  close    volume
# date
# 739362  18500  18529  18076  18274  26018999
# 739363  18515  18810  18455  18747  34477053
# 739364  19292  19551  18984  19025  44866133
# 739365  19076  19437  18989  19406  29820132
# 739366  19272  19426  19155  19412  25028968
# 739369  19450  19615  19253  19494  22482254
# 739370  19447  19686  19301  19609  20118155
# 739371  19314  19548  19072  19486  29046138
# 739372  19571  19767  19374  19607  33169717
# 739373  19833  20121  19818  20048  30201787)
