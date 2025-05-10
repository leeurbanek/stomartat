"""src/pkg/data_srv/process.py\n
"""
import logging

import pandas as pd

from pkg import DEBUG


logger = logging.getLogger(__name__)


class DataProcessor:
    """"""
    def __init__(self, data:tuple):
        self.symbol = data[0]
        self.data = data[1]
        self.df = pd.DataFrame(index=data[1].index)


    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"symbol={self.symbol}, "
            f"data={self.data}), "
            f"df={self.df}"
            )

    def process_dataframe(self):
        """"""
        if DEBUG: logger.debug(f"process_dataframe(self={self})")

        # add columns to df for price, volume, etc.
        self._add_close_weighted_price()
        self._add_volume_series()

        return self.df


    def _add_close_location_value(self):
        """"""
        if DEBUG: logger.debug(f"_add_close_location_value(df={self.df})")

# TODO set series data type int
    def _add_close_weighted_price(self):
        """"""
        if DEBUG: logger.debug(f"_add_close_weighted_price(df={self.df})")

        price = round(
            (self.data['high'] + self.data['low'] + self.data['close'] * 2) / 4
        )
        self.df.insert(
            loc=0, column='price', value=price, allow_duplicates=True
        )

    def _add_volume_series(self):
        """"""
        if DEBUG: logger.debug(f"_add_volume_series(self={type(self)})")

        self.df.insert(
            loc=1, column='volume', value=self.data['volume'], allow_duplicates=True
        )


# def close_location_value(tuple_list):
#     """"""
#     if debug: logger.debug(f"close_location_value(tuple_list={tuple_list})")

#     CLV = namedtuple('CLV', ['symbol', 'date', 'clv'])
#     clv_list =[]

#     for item in tuple_list:
#         close_location_value = CLV(
#             item.symbol,
#             item.date,
#             round(((2 * item.close - item.low - item.high) / (item.high - item.low)) * 100)
#         )
#         clv_list.append(close_location_value)

#     if debug: logger.debug(f"close_location_value() -> clv_list:\n{clv_list})")
#     return clv_list

# def close_weighted_price(tuple_list):
#     """"""
#     if debug: logger.debug(f"close_weighted_price(tuple_list={tuple_list})")

#     Price = namedtuple('Price', ['symbol', 'date', 'price'])
#     price_list =[]

#     for item in tuple_list:
#         close_weighted_price = Price(
#             item.symbol,
#             item.date,
#             round((item.high + item.low + item.close * 2) / 4)
#         )
#         price_list.append(close_weighted_price)

#     if debug: logger.debug(f"close_weighted_price() -> price_list:\n{price_list})")
#     return price_list
