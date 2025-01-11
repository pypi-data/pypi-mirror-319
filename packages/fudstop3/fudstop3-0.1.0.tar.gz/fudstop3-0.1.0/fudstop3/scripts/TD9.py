import sys
from pathlib import Path



project_dir = str(Path(__file__).resolve().parents[1])
if project_dir not in sys.path:
    sys.path.append(project_dir)

import asyncio
import pandas as pd

# Imports from your existing code / environment
from apis.polygonio.polygon_database import PolygonDatabase
from apis.webull.webull_ta import WebullTA
from apis.markets.list_sets.ticker_lists import most_active_tickers
from apis.helpers import is_current_candle_td9  # If you need it
from scripts.imps import *  # If you need it

# Initialize your DB + TA objects
db = PolygonDatabase()
ta = WebullTA()


def td_sequential_setup(df, price_col="close", time_col="timestamp"):
    """
    Build the 'setup' count portion of TD Sequential:
      - Positive counts (1..9) => potential buy setup
      - Negative counts (-1..-9) => potential sell setup
      - 0 => no active setup at that bar

    Officially:
      - A "buy setup" starts at bar #1 if (close[i] < close[i-4]).
      - Each consecutive bar is #2..#9 if (close[i] < close[i-4]).
      - A "sell setup" starts at bar #1 if (close[i] > close[i-4]).
      - Each consecutive bar is #2..#9 if (close[i] > close[i-4]).

    IMPORTANT CHANGE:
      - Once the count reaches ±9, we STOP counting and reset.
        (No bars with values beyond ±9.)
    """
    df = df.sort_values(by=time_col).reset_index(drop=True)

    setup_counts = [0] * len(df)
    direction = None  # 'buy' or 'sell'
    count = 0

    for i in range(len(df)):
        if i < 4:
            # We need at least 4 prior bars to compare
            setup_counts[i] = 0
            continue

        close_now = df.loc[i, price_col]
        close_4ago = df.loc[i - 4, price_col]

        if direction is None or count == 0:
            # Attempt to start a new sequence
            if close_now < close_4ago:
                direction = "buy"
                count = 1
                setup_counts[i] = count
            elif close_now > close_4ago:
                direction = "sell"
                count = 1
                setup_counts[i] = -count
            else:
                direction = None
                count = 0
                setup_counts[i] = 0

        else:
            # We already have an active setup in progress
            if direction == "buy":
                if close_now < close_4ago:
                    count += 1
                    # Cap at 9, then reset
                    if count > 9:
                        count = 9
                        direction = None
                    setup_counts[i] = count
                else:
                    # Flip or break
                    if close_now > close_4ago:
                        direction = "sell"
                        count = 1
                        setup_counts[i] = -count
                    else:
                        direction = None
                        count = 0
                        setup_counts[i] = 0

            elif direction == "sell":
                if close_now > close_4ago:
                    count += 1
                    # Cap at 9, then reset
                    if count > 9:
                        count = 9
                        direction = None
                    setup_counts[i] = -count
                else:
                    # Flip or break
                    if close_now < close_4ago:
                        direction = "buy"
                        count = 1
                        setup_counts[i] = count
                    else:
                        direction = None
                        count = 0
                        setup_counts[i] = 0

    df["td_setup_count"] = setup_counts
    return df


def check_td9(df, price_col="close", time_col="timestamp"):
    """
    Check if the last bar is exactly bar #9 (positive or negative).
      - +9 => "CURRENT TD9 BUY"
      - -9 => "CURRENT TD9 SELL"
      - otherwise => None
    """
    df_with_counts = td_sequential_setup(df, price_col, time_col)
    last_count = df_with_counts.iloc[-1]["td_setup_count"]

    if last_count == 9:
        return "CURRENT TD9 BUY"
    elif last_count == -9:
        return "CURRENT TD9 SELL"
    else:
        return None


async def check_candles_for_pretd9(ticker, timespan):
    """
    1) Pull the latest 14 candles for the given ticker/timespan.
    2) Check if the final bar is #9 (buy or sell).
    3) If so, upsert the result into table "td9_pre".
    """
    try:
        df = await WBTA.get_candle_data(ticker, interval=timespan, headers=headers, count='800')
        df = df.rename(columns={'Close': 'close', 'Avg': 'avg', 'Low': 'low', 'High': 'high', 'Open': 'open', 'Volume': 'volume', 'Vwap': 'vwap', 'Timestamp': 'timestamp'})
        df.sort_values(by='timestamp', inplace=True)

        # Check if last bar is #9
        potential_signal = check_td9(df, price_col='close', time_col='timestamp')
        if potential_signal is not None:
            final_ts = df['timestamp'].iloc[-1]
            final_setup_count = td_sequential_setup(df, 'close', 'timestamp').iloc[-1]['td_setup_count']

            row_to_store = pd.DataFrame([{
                'ticker': ticker,
                'timespan': timespan,
                'timestamp': final_ts,
                'td_setup_count': final_setup_count,
                'td_signal': potential_signal
            }])

            # Upsert to table "td9_pre" (adjust table name / columns if needed)
            await db.batch_upsert_dataframe(
                row_to_store,
                table_name='live_td9',
                unique_columns=['ticker', 'timespan', 'timestamp']
            )
        print(potential_signal)
        return potential_signal
    except Exception as e:
        print(e)


def chunk_list(data, chunk_size):
    """
    Helper to chunk a list into consecutive pieces.
    """
    for i in range(0, len(data), chunk_size):
        yield data[i : i + chunk_size]


async def run_main():
    """
    Main loop:
      1) Chunk the tickers to avoid hitting them all at once.
      2) For each chunk, create tasks to check TD9 signals on multiple timespans.
      3) Print results if found, then sleep for 60s.
    """
    await db.connect()
    timespans = ['m1', 'm60', 'd', 'w', 'm5', 'm30', 'm120', 'm240', 'm']
    chunk_size = 10

    while True:
        for chunk in chunk_list(most_active_tickers, chunk_size):
            tasks = [
                check_candles_for_pretd9(ticker, tspan)
                for ticker in chunk
                for tspan in timespans
            ]
            # As tasks complete, report results if any
            for completed_task in asyncio.as_completed(tasks):
                result = await completed_task
                if result:
                    print(f"Got TD9 signal: {result}")

        print("Sleeping 60 seconds before next scan...")
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(run_main())