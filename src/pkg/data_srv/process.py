"""src/pkg/data_srv/process.py\n
class DataProcessor\n
df_to_list_of_tuples()
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
        if DEBUG: logger.debug(f"{type(self)}")

        # add columns to df for price, volume, etc.
        for l, line in enumerate(self.line):
            eval(f"self._add_{line.lower()}_series({l})")

        return self.df


    def _add_clop_series(self, loc):
        """difference between the close and open price"""
        clop = (self.data['close'] - self.data['open']).astype(int)
        if DEBUG: logger.debug(f"_add_clop_series()-> {type(clop)}")

        self.df.insert(
            loc=loc, column='clop', value=clop, allow_duplicates=True
        )

    def _add_clv_series(self, loc):
        """close location value, relative to the high-low range"""
        clv = round(
            ((2 * self.data['close'] - self.data['low'] - self.data['high'])
             / (self.data['high'] - self.data['low'])) * 100).astype(int)
        if DEBUG: logger.debug(f"_add_clv_series()-> {type(clv)}")

        self.df.insert(
            loc=loc, column='clv', value=clv, allow_duplicates=True
        )

    def _add_cwap_series(self, loc):
        """close weighted average price not including open price"""
        cwap = round(
            (self.data['high'] + self.data['low'] + self.data['close'] * 2) / 4
        ).astype(int)
        if DEBUG: logger.debug(f"_add_price_series()-> {type(cwap)}")

        self.df.insert(
            loc=loc, column='cwap', value=cwap, allow_duplicates=True
        )

    def _add_hilo_series(self, loc):
        """difference between the high and low price"""
        hilo = (self.data['high'] - self.data['low']).astype(int)
        if DEBUG: logger.debug(f"_add_hilo_series()-> {type(hilo)}")

        self.df.insert(
            loc=loc, column='hilo', value=hilo, allow_duplicates=True
        )

    def _add_volume_series(self, loc):
        """number of shares traded"""
        volume = self.data['volume']
        if DEBUG: logger.debug(f"_add_volume_series()-> {type(volume)}")

        self.df.insert(
            loc=loc, column='volume', value=volume, allow_duplicates=True
        )


def df_to_list_of_tuples(symbol:str, df:pd.DataFrame)->list[tuple]:
    """"""
    if DEBUG: logger.debug(f"df_to_list_of_tuples(df={type(df)})")

    return list(df.itertuples(index=True, name=symbol))

# DataFrame.itertuples(index=True, name='Pandas')
# list_of_tuples = list(df.itertuples(index=False, name=None))
# print(list_of_tuples)
