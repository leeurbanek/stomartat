"""src/pkg/chart_srv/scraper/my_requests.py\n
Use urllib3 to get charts with the saved chart_url in the
chart_cfg.ini file then save to work directory. The Pillow
module is used to convert byte data to a png image.
"""
import logging, logging.config

import colorlog


logging.config.fileConfig(fname='src/logger.ini')
logging.getLogger('PIL').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = colorlog.getLogger(__name__)


class WebScraper:
    """Fetch and save SharpCharts from stockcharts.com"""
    def __init__(self, ctx):
        import urllib3
        self.chart_dir = f"{ctx['default']['work_dir']}/chart"
        self.chart_skin = ctx['chart_service']['chart_skin']
        self.ctx = ctx
        self.debug = ctx['default']['debug']
        self.period = ctx['interface']['opt_trans']
        self.symbol = ctx['interface']['arguments']
        self.http = urllib3.PoolManager()
        if self.chart_skin == 'dark':
            self.chart_url = ctx.obj['chart_service']['chart_dark']
        else:
            self.chart_url = ctx.obj['chart_service']['chart_light']

    def __repr__(self):
        return f'{self.__class__.__name__}(ctx={self.ctx})'

    def webscraper(self):
        """Main entry point to Webscraper class. Directs workflow
        of webscraper.
        """
        if self.debug: logger.debug(f'webscraper(self={self})')
        self._get_img_src_convert_bytes_to_png_and_save(chart_url=self.chart_url)


    def _get_img_src_convert_bytes_to_png_and_save(self, chart_url: str):
        """For each period in the `ctx interface opt_trans` dictionary
        get the chart for each symbol in the `ctx interface arguments`
        list. Convert the bytes to a .png image then save to the chart
        work directory.
        """
        import io, os
        from PIL import Image

        if self.debug: logger.debug(f'_get_img_src_convert_bytes_to_png_and_save(chart_url {type(chart_url)})')

        for symbol in self.symbol:  # Update the default url with our symbol and period
            for period in self.period:
                new_url = self._replace_period_symbol_in_chart_url(chart_url, period, symbol)
                # Get the chart image source convert to .png and save
                image_src = self.http.request('GET', new_url, headers={'User-agent': 'Mozilla/5.0'})
                image = Image.open(io.BytesIO(image_src.data)).convert('RGB')
                image.save(os.path.join(self.chart_dir, f'{symbol}_{period[:1].lower()}.png'), 'PNG', quality=80)

    def _replace_period_symbol_in_chart_url(self, chart_url: str, period: str, symbol: str):
        """"""
        import time

        if self.debug: logger.debug(f'_replace_period_symbol_in_chart_url({new_url}, {period}, {symbol})')
        if period != 'Daily':
            chart_url = chart_url.replace('p=D', 'p=W').replace('yr=1', 'yr=5')
        new_url = chart_url.replace('AAPL', symbol)
        # Return new_url with current epoch time parsed in.
        return new_url[:-13]+str(round(time.time() * 1000))


if __name__ == '__main__':
    from test import data

    start = WebScraper(ctx=data.ctx_default)
    start.webscraper()

    start = WebScraper(ctx=data.ctx_custom)
    start.webscraper()
