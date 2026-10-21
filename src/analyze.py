import csv
import json
from functools import reduce
from pathlib import Path

import pandas as pd

from src.client import Client
from src.sale import Sale
from src.sales_collection import SalesCollection
from src.client_collection import ClientCollection
from src.functional_utils import (
    filter_sales_by_category,
    filter_sales_by_month,
    filter_sales_by_day,
    filter_sales_by_client,
    get_amounts,
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"




#  ------------- CARGA DE DATOS ----------------------


def load_clients():
    with open(DATA_DIR / "clients.json", encoding="utf-8") as f:
        return [Client(**item) for item in json.load(f)]


def load_sales():
    with open(DATA_DIR / "sales.csv", encoding="utf-8", newline="") as f:
        return [
            Sale(r["sale_id"], int(r["client_id"]), r["product"],
                 r["category"], float(r["amount"]), r["date"])
            for r in csv.DictReader(f)
        ]

def sum_amounts(sales):
    return reduce(lambda a, b: a + b, get_amounts(sales), 0)



# ---------- Cálculos 1 al 5 ----------



def calc_total_clients(client):
    return len(client)

def calc_total_sales(sales):
    return len(sales)

def total_ventas_client(sales, client_id):
    client_sales = filter_sales_by_client(sales, client_id)
    return sum_amounts(client_sales)

def num_ventas_client(sales, client_id):
    return len(SalesCollection(sales).sales_by_client(client_id))

def promedio_ventas_client(sales, client_id):
    total = total_ventas_client(sales, client_id)
    count = num_ventas_client(sales, client_id)
    if count == 0:
        return 0
    return round(total / count, 2)

def calc_client_stats(clients, sales):
    stats = []
    for client in clients:
        stats.append({
            "client_id": client.client_id,
            "name": client.name,
            "country": client.country,
            "total_spend": total_ventas_client(sales, client.client_id),
            "sale_count": num_ventas_client(sales.client, client.client_id),
        })
    return stats

# ----------------------- calculos del 6 al 10 ------------------------------


def calc_top_client_by_country(clients, sales):
    client_country = ClientCollection(clients)
    result = {}
    for country in sorted(set(map(lambda c: c.country, clients))):
        group = client_country.clients_by_country(country)
        best = max(group, key=lambda c: total_ventas_client(sales,c.client_id))
        result[country] = best.name
    return result