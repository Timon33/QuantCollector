import logging

import config
import save_handler
import secret

# this script is called by crwonjob or similar util
# uses api and config scripts

# change this to your api key


def download_option_data(api_key: str):
    symbol_list = config.symbol_list()["list"]

    for i, symbol in enumerate(symbol_list):
        print(f"{i}/{len(symbol_list)} ({i / len(symbol_list)}%) downloading data for {symbol}...", end="", flush=True)
        save_handler.save_contract_list(api_key, symbol)
        save_handler.save_all_option_chains(api_key, symbol)
        print(" complet")


def main():
    if not save_handler.was_market_open(secret.TRADIER_API_KEY):
        download_option_data(secret.TRADIER_API_KEY)
    else:
        print("market wasn't open")


if __name__ == "__main__":
    main()