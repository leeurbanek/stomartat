"""test/data.py"""


ctx_custom = {
    'default': {
        'debug': True,
        'work_dir': '/home/la/dev/stomartat/temp/',
        'cfg_chart': '/home/la/dev/stomartat/src/pkg/chart_srv/cfg_chart.ini',
        'cfg_main': '/home/la/dev/stomartat/src/config.ini'
    },
    'interface': {
        'opt_trans': ['Daily', 'Weekly'],
        'arguments': ['SPY']
    }, 'chart_service': {
        'adblock': '',
        'base_url': 'https://stockcharts.com/sc3/ui/?s=AAPL',
        'driver': 'chromedriver',
        'scraper': 'requests',
        'chart_list': 'EEM IWM LQD'
    }
}

ctx_default = {
    'default': {
        'debug': True,
        'work_dir': '/home/la/dev/stomartat/temp/',
        'cfg_chart': '/home/la/dev/stomartat/src/pkg/chart_srv/cfg_chart.ini',
        'cfg_main': '/home/la/dev/stomartat/src/config.ini'
    },
    'interface': {
        'opt_trans': ['Daily'],
        'arguments': ['EEM', 'IWM', 'LQD']
    },
    'chart_service': {
        'adblock': '',
        'base_url': 'https://stockcharts.com/sc3/ui/?s=AAPL',
        'driver': 'chromedriver',
        'scraper': 'requests',
        'chart_list': 'EEM IWM LQD'
    }
}
