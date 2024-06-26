#!/usr/bin/env python

"""
  script to download aggTrades.
  set the absoluate path destination folder for STORE_DIRECTORY, and run

  e.g. STORE_DIRECTORY=/data/ ./download-aggTrade.py

"""

import sys
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError
from datetime import *
import pandas as pd
from enums import *
from utility import download_file, get_all_symbols, get_parser, get_start_end_date_objects, convert_to_date_object, \
    get_path

market_data_type = "bookTicker"

def download_monthly_bookTicker(trading_type, symbols, num_symbols, years, months, start_date, end_date, folder,
                               checksum):
    current = 0
    date_range = None

    if start_date and end_date:
        date_range = start_date + " " + end_date

    if not start_date:
        start_date = START_DATE
    else:
        start_date = convert_to_date_object(start_date)

    if not end_date:
        end_date = END_DATE
    else:
        end_date = convert_to_date_object(end_date)

    print("Found {} symbols".format(num_symbols))

    for symbol in symbols:
        print("[{}/{}] - start download monthly {} {} ".format(current + 1, num_symbols, symbol, market_data_type))
        for year in years:
            for month in months:
                current_date = convert_to_date_object('{}-{}-01'.format(year, month))
                if current_date >= start_date and current_date <= end_date:
                    path = get_path(trading_type, market_data_type, "monthly", symbol)
                    file_name = "{}-{}-{}-{}.zip".format(symbol.upper(), market_data_type, year, '{:02d}'.format(month))
                    download_file(path, file_name, date_range, folder)

                    if checksum == 1:
                        checksum_path = get_path(trading_type, market_data_type, "monthly", symbol)
                        checksum_file_name = "{}-{}-{}-{}.zip.CHECKSUM".format(symbol.upper(), market_data_type, year,
                                                                                      '{:02d}'.format(month))
                        download_file(checksum_path, checksum_file_name, date_range, folder)

        current += 1


def download_daily_bookTicker(trading_type, symbols, num_symbols, dates, start_date, end_date, folder, checksum):
    current = 0
    date_range = None

    if start_date and end_date:
        date_range = start_date + " " + end_date

    if not start_date:
        start_date = START_DATE
    else:
        start_date = convert_to_date_object(start_date)

    if not end_date:
        end_date = END_DATE
    else:
        end_date = convert_to_date_object(end_date)

    print("Found {} symbols".format(num_symbols))

    for symbol in symbols:
        print("[{}/{}] - start download daily {} {} ".format(current + 1, num_symbols, symbol, market_data_type))
        for date in dates:
            current_date = convert_to_date_object(date)
            if current_date >= start_date and current_date <= end_date:
                path = get_path(trading_type, market_data_type, "daily", symbol)
                file_name = "{}-{}-{}.zip".format(symbol.upper(), market_data_type, date)
                download_file(path, file_name, date_range, folder)

                if checksum == 1:
                    checksum_path = get_path(trading_type, market_data_type, "daily", symbol)
                    checksum_file_name = "{}-{}-{}.zip.CHECKSUM".format(symbol.upper(), market_data_type, date)
                    download_file(checksum_path, checksum_file_name, date_range, folder)

        current += 1


if __name__ == "__main__":
    parser = get_parser(market_data_type)
    args = parser.parse_args(sys.argv[1:])

    if not args.symbols:
        print("fetching all symbols from exchange")
        symbols = get_all_symbols(args.type)
        num_symbols = len(symbols)
    else:
        symbols = args.symbols
        num_symbols = len(symbols)
        print("fetching {} symbols from exchange".format(num_symbols))

    if args.dates:
        dates = args.dates
    else:
        period = convert_to_date_object(datetime.today().strftime('%Y-%m-%d')) - convert_to_date_object(
            PERIOD_START_DATE)
        dates = pd.date_range(end=datetime.today(), periods=period.days + 1).to_pydatetime().tolist()
        dates = [date.strftime("%Y-%m-%d") for date in dates]
        if args.skip_monthly == 0:
            download_monthly_bookTicker(args.type, symbols, num_symbols, args.years, args.months, args.startDate,
                                       args.endDate, args.folder, args.checksum)
    if args.skip_daily == 0:
        download_daily_bookTicker(args.type, symbols, num_symbols, dates, args.startDate, args.endDate, args.folder,
                                 args.checksum)

