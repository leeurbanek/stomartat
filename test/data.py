"""test/data.py"""

ctx={
    'default': {
        'debug': True,
        'work_dir': '/home/la/dev/stomartat/temp/',
        'cfg_chart': '/home/la/dev/stomartat/src/pkg/chart_srv/cfg_chart.ini',
        'cfg_main': '/home/la/dev/stomartat/src/config.ini'
    },
    'interface': {},
    'chart_service': {
        'adblock': '',
        'base_url': 'https://stockcharts.com/sc3/ui/?s=AAPL',
        'driver': 'chromedriver',
        'scraper': 'selenium',
        'chart_list': 'EEM IWM LQD'
    }
}
