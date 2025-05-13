"""src/pkg/data_srv/process.py\n
"""
import logging

import pandas as pd

from pkg import DEBUG


logger = logging.getLogger(__name__)


class DataProcessor:
    """"""
    def __init__(self, ctx:dict, data:tuple):
        # self.line = sorted(list(ctx['data_service']['data_line'].split(' ')))
        self.line = ctx['interface']['data_line']
        self.symbol = data[0]
        self.data = data[1]
        self.df = pd.DataFrame(index=data[1].index)


    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"symbol={self.symbol}, "
            f"data={self.data}), "
            f"line={self.line}), "
            f"df={self.df}"
            )

    def process_dataframe(self):
        """"""
        if DEBUG: logger.debug(f"process_dataframe(self={self})")

        # add columns to df for price, volume, etc.
        for l, line in enumerate(self.line):
            eval(f"self._add_{line.lower()}_series({l})")

        return self.df


    def _add_clop_series(self, loc):
        """difference of close and open prices"""
        clop = (self.data['close'] - self.data['open']).astype(int)
        if DEBUG: logger.debug(f"clop:\n{clop}")

        self.df.insert(
            loc=loc, column='clop', value=clop, allow_duplicates=True
        )

    def _add_clv_series(self, loc):
        """measures location of the price in relation to the high-low range"""
        clv = round(
            ((2 * self.data['close'] - self.data['low'] - self.data['high'])
             / (self.data['high'] - self.data['low'])) * 100).astype(int)
        if DEBUG: logger.debug(f"clv:\n{clv}")

        self.df.insert(
            loc=loc, column='clv', value=clv, allow_duplicates=True
        )

    def _add_hilo_series(self, loc):
        """difference of high and low prices"""
        hilo = (self.data['high'] - self.data['low']).astype(int)
        if DEBUG: logger.debug(f"hilo:\n{hilo}")

        self.df.insert(
            loc=loc, column='hilo', value=hilo, allow_duplicates=True
        )

    def _add_price_series(self, loc):
        """average price with extra weight given to the closing price"""
        price = round(
            (self.data['high'] + self.data['low'] + self.data['close'] * 2) / 4
        ).astype(int)
        if DEBUG: logger.debug(f"price:\n{price}")

        self.df.insert(
            loc=loc, column='price', value=price, allow_duplicates=True
        )

    def _add_volume_series(self, loc):
        """period volume"""
        volume = self.data['volume']
        if DEBUG: logger.debug(f"volume:\n{volume}")

        self.df.insert(
            loc=loc, column='volume', value=volume, allow_duplicates=True
        )
