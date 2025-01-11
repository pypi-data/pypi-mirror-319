#standard imports
import asyncio
import pandas as pd
from datetime import datetime, timedelta, timezone
import pytz
from collections import deque

from discord_webhook import AsyncDiscordWebhook, DiscordEmbed
from tabulate import tabulate

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sb


#helpers
from apis.helpers import save_df_as_image, traverse_and_extract, traverse_tree, format_large_numbers_in_dataframe2, nth_weekday_of_month, next_trading_day, calculate_percent_decrease, calculate_candlestick,calculate_countdown,calculate_days_to_expiry,calculate_price_to_strike,calculate_setup,calculate_td9_series,camel_to_snake_case,check_macd_sentiment,chunk_data,chunks,clean_html,convert_datetime_list,convert_str_to_datetime,convert_timestamp_to_human_readable,convert_to_datetime_or_str,convert_to_eastern_time,convert_to_est,convert_to_et,convert_to_ns_datetime,convert_to_yymmdd,count_itm_otm,create_option_symbol,csv_to_dict,current_time_to_unix,is_current_candle_td9,describe_color,paginate_concurrent,lowercase_columns,decimal_to_color,format_large_number,flatten_list_of_dicts,flatten_dict,flatten_object
from apis.all_helpers import chunk_string


headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "access_token": "dc_us_tech1.193f1ba4ca7-5bd586952af0445ea4e4883003c577b1",
    "app": "global",
    "app-group": "broker",
    "appid": "wb_web_app",
    "device-type": "Web",
    "did": "w35fbki4nv4n4i6fjbgjca63niqpo_22",
    "hl": "en",
    "origin": "https://app.webull.com",
    "os": "web",
    "osv": "i9zh",
    "platform": "web",
    "priority": "u=1, i",
    "referer": "https://app.webull.com/",
    "reqid": "h15qdhcy99l2sidi00t2sox8y748h_35",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "tz": "America/Chicago",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "ver": "5.2.1",
    "x-s": "9ad7d1393ca5c705bfe6469622b6805384a53b27c86fcaf5966061737c602747",
    "x-sv": "xodp2vg9"
}


#webull
from apis.webull.webull_trading import WebullTrading
from apis.webull.webull_markets import WebullMarkets
from apis.webull.webull_options.webull_options import WebullOptions
from apis.webull.webull_ta import WebullTA

#polygon
from apis.polygonio.async_polygon_sdk import Polygon
from apis.polygonio.polygon_options import PolygonOptions

#database
from apis.polygonio.polygon_database import PolygonDatabase




#DISCORD = DiscordSDK()


WBMMARKETS = WebullMarkets()
WBTRADING = WebullTrading() #optional ETF list CSV file.. this file is provided with package in FUDSTOP.zip
WBTA = WebullTA()
WBOPTIONS = WebullOptions() #defaults the port - will change this in future

#SEC = SECSDK()

POLY = Polygon()
POLY_OPTS = PolygonOptions()
DB = PolygonDatabase() #or connection string




from apis.markets.list_sets.ticker_lists import all_tickers, most_active_tickers
from apis.markets.list_sets.dicts import hex_color_dict


# Shared queue for Producer/Consumer
queue = deque()
