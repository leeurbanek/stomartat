import io
import logging
import os
from configparser import ConfigParser
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from PIL import Image
from requests_html import HTMLSession

from src import config_file
from src.ctx_mgr import SpinnerManager


conf_obj = ConfigParser()
conf_obj.read(config_file)

logging.getLogger('PIL').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

BASE_URL = conf_obj['Scraper']['base_url']
CHART_DIR = f"{conf_obj['Default']['work_dir']}/chart"


class WebScraper:
    """"""
    def __init__(self, debug, period, symbol) -> None:
        self.session = HTMLSession()
        self.debug = debug
        self.period = period
        self.symbol = symbol
        self.url = BASE_URL+symbol

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(debug={self.debug}, symbol={self.symbol}, period={self.period})"

    def webscraper(self):
        """"""
        if self.debug: logger.debug(f'webscraper({self.symbol}, {self.period})')
        if not self.debug: print(f'  fetching chart: {self.symbol}_{self.period.lower()}.png... ', end=' ')
        with SpinnerManager(debug=self.debug):
            form = self._get_all_forms()[2]
            details = self._get_form_details(form)
            soup = self._submit_form(details)
            self._get_img_src_save_imgage(soup)
            if not self.debug: print('\b done,')

    def _get_all_forms(self):
        """Returns all form tags found on a web page's `url` """
        if self.debug: logger.debug(f'_get_all_forms()[2]')
        res = self.session.get(self.url)
        # res.html.render()  # for javascript driven website
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.find_all("form")

    def _get_form_details(self, form=None):
        """Returns action, method, and form controls (inputs, etc)"""
        if self.debug: logger.debug(f'_get_form_details({type(form)})')
        details = {}
        # get the form action (requested URL)
        action = form.attrs.get("action")
        if action:
            action = action.lower()
        # get the form method (POST, GET, DELETE, etc)
        # if not specified, GET is the default in HTML
        method = form.attrs.get("method", "get").lower()
        # get all form inputs
        inputs = []
        for input_tag in form.find_all("input"):
            # get type of input form control
            input_type = input_tag.attrs.get("type", "text")
            # get name attribute
            input_name = input_tag.attrs.get("name")
            # get the default value of that input tag
            input_value =input_tag.attrs.get("value", "")
            # add everything to the list
            inputs.append({"type": input_type, "name": input_name, "value": input_value})
        for select in form.find_all("select"):
            # get the name attribute
            select_name = select.attrs.get("name")
            # set the type as select
            select_type = "select"
            select_options = []
            # the default select value
            select_default_value = ""
            # iterate over options and get the value of each
            for select_option in select.find_all("option"):
                # get the option value used to submit the form
                option_value = select_option.attrs.get("value")
                if option_value:
                    select_options.append(option_value)
                    if select_option.attrs.get("selected"):
                        # if 'selected' attribute is set, set this option as default
                        select_default_value = option_value
            if not select_default_value and select_options:
                # if the default is not set, and there are options, take the first option as default
                select_default_value = select_options[0]
            # add the select to the inputs list
            inputs.append({"type": select_type, "name": select_name, "values": select_options, "value": select_default_value})
        for textarea in form.find_all("textarea"):
            # get the name attribute
            textarea_name = textarea.attrs.get("name")
            # set the type as textarea
            textarea_type = "textarea"
            # get the textarea value
            textarea_value = textarea.attrs.get("value", "")
            # add the textarea to the inputs list
            inputs.append({"type": textarea_type, "name": textarea_name, "value": textarea_value})

        # put everything into the details dictionary
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        return details

    def _get_img_src_save_imgage(self, soup=None):
        """"""
        if self.debug: logger.debug(f'_get_img_src_save_imgage({type(soup)})')
        attr = soup.find('div', attrs={'class': "ChartNotesContainer"}).find('img')
        src = attr.get('src')

        src_content = self.session.get(f'{src}', headers={'User-agent': 'Mozilla/5.0'}).content

        image_file = io.BytesIO(src_content)
        image = Image.open(image_file).convert('RGB')
        image.save(os.path.join(CHART_DIR, f'{self.symbol}_{self.period.lower()}.png'), 'PNG', quality=80)

    def _submit_form(self, form_details=None):
        """"""
        if self.debug: logger.debug(f'_submit_form({type(form_details)})')

        year = 1  # for setting dataRange predef field
        if self.period == 'Weekly': year = 5

        data = {}

        for input_tag in form_details["inputs"]:
            if input_tag["type"] == "hidden":  # use the default value
                data[input_tag["name"]] = input_tag["value"]
            elif input_tag["type"] == "select":
                data[input_tag["name"]] = input_tag["value"]
                data['period'] = self.period  # set period
                data['predefChanged'] = 'true'
                data['dataRange'] = f'predef:{year}|0|0'  # set dataRange
                data['chartSize'] = 'Landscape'
                data['chartSkin'] = 'night'
                data['years'] = str(year)  # set years
                data['months'] = '0'
                data['overType_0'] = 'SMA'
                data['overArgs_0'] = '50'
                data['overType_1'] = 'SMA'
                data['overArgs_1'] = '200'
                data['overType_2'] = 'VOLHORIZ'
                data['indType_0'] = 'RSI'
                data['indArgs_0'] = '14'
                data['indLoc_0'] = 'above'
                data['indType_1'] = 'MACD'
                data['indArgs_1'] = '12,26,9'
                data['indLoc_1'] = 'below'
            elif input_tag["type"] != "submit":
                data[input_tag["name"]] = input_tag["value"]
                data['useInspector'] = 'false'
                data['fullQuote'] = 'false'
                data['priceLabels'] = 'false'
                data['solidCandles'] = 'false'
                data['zoomThumbnail'] = 'false'
                data['extendedHours'] = 'false'

        # join the url with the action (form request URL)
        url = urljoin(self.url, form_details["action"])
        if form_details["method"] == "post":
            res = self.session.post(url, data=data)
        elif form_details["method"] == "get":
            res = self.session.get(url, params=data)

        # the below code is for replacing relative URLs with absolute ones
        soup = BeautifulSoup(res.content, "html.parser")
        for link in soup.find_all("link"):
            try:
                link.attrs["href"] = urljoin(url, link.attrs["href"])
            except:
                pass
        for script in soup.find_all("script"):
            try:
                script.attrs["src"] = urljoin(url, script.attrs["src"])
            except:
                pass
        for img in soup.find_all("img"):
            try:
                img.attrs["src"] = urljoin(url, img.attrs["src"])
            except:
                pass
        for a in soup.find_all("a"):
            try:
                a.attrs["href"] = urljoin(url, a.attrs["href"])
            except:
                pass
        return soup


if __name__ == '__main__':
    print(f"{__name__}.my_requests_html.py")
