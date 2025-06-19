"""
Wallet Tracer — отслеживает поток средств с адреса по цепочке транзакций.
"""

import requests
import argparse
from datetime import datetime

def fetch_address_transactions(address, limit=10):
    url = f"https://api.blockchair.com/bitcoin/dashboards/address/{address}?transaction_details=true"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception("❌ Ошибка получения данных.")
    data = r.json()["data"][address]["transactions"][:limit]
    return data

def fetch_transaction_details(txid):
    url = f"https://api.blockchair.com/bitcoin/raw/transaction/{txid}"
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()["data"][txid]["decoded_raw_transaction"]

def trace_wallet(address):
    print(f"🔍 Wallet Tracer: анализ адреса {address}")
    txids = fetch_address_transactions(address)
    for txid in txids:
        tx = fetch_transaction_details(txid)
        if not tx:
            continue
        time = tx.get("time", "unknown")
        dt = datetime.utcfromtimestamp(int(time)) if time != "unknown" else "???"
        print(f"📦 Транзакция {txid} ({dt})")

        outputs = tx.get("vout", [])
        for out in outputs:
            value = out.get("value", 0)
            script = out.get("script_pub_key", {})
            out_addr = script.get("address", "неизвестен")
            print(f"    → {out_addr}: {value} BTC")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wallet Tracer — отслеживание вывода средств с адреса.")
    parser.add_argument("address", help="Bitcoin-адрес")
    args = parser.parse_args()
    trace_wallet(args.address)
