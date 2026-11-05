"""
analyze.py
Carga clientes (JSON) y ventas (CSV), calcula 10 métricas y genera
el reporte final en final_report.json.

Se ejecuta desde la raíz del proyecto:  python -m src.analyze
"""

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
    filter_sales_by_client,
    get_amounts,
)

# Rutas: la carpeta data/ y el archivo de salida están en la raíz del proyecto
ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
REPORT_FILE = ROOT_DIR / "final_report.json"


# ------------------------------------------------------------------
# CARGA DE DATOS
# ------------------------------------------------------------------

def load_clients():
    """Lee data/clients.json y devuelve una lista de objetos Client."""
    with open(DATA_DIR / "clients.json", encoding="utf-8") as f:
        return [Client(**item) for item in json.load(f)]


def load_sales():
    """Lee data/sales.csv y devuelve una lista de objetos Sale."""
    with open(DATA_DIR / "sales.csv", encoding="utf-8", newline="") as f:
        return [
            Sale(r["sale_id"], int(r["client_id"]), r["product"],
                 r["category"], float(r["amount"]), r["date"])
            for r in csv.DictReader(f)
        ]


def sum_amounts(sales):
    """Suma los importes de una lista de ventas (programación funcional)."""
    return reduce(lambda a, b: a + b, get_amounts(sales), 0)


# ------------------------------------------------------------------
# CÁLCULOS 1 AL 5
# ------------------------------------------------------------------

def calc_total_clients(clients):
    """Cálculo 1: número total de clientes."""
    return len(clients)


def calc_total_sales(sales):
    """Cálculo 2: número total de ventas."""
    return len(sales)


def total_ventas_client(sales, client_id):
    """Cálculo 3: total gastado por un cliente."""
    client_sales = filter_sales_by_client(sales, client_id)
    return sum_amounts(client_sales)


def num_ventas_client(sales, client_id):
    """Cálculo 4: número de ventas de un cliente (usa la clase POO)."""
    return len(SalesCollection(sales).sales_by_client(client_id))


def promedio_ventas_client(sales, client_id):
    """Cálculo 5: gasto medio por venta de un cliente (2 decimales)."""
    total = total_ventas_client(sales, client_id)
    count = num_ventas_client(sales, client_id)
    if count == 0:
        return 0
    return round(total / count, 2)


def calc_client_stats(clients, sales):
    """Agrupa los cálculos 3, 4 y 5 en un diccionario por cliente."""
    stats = []
    for client in clients:
        stats.append({
            "client_id": client.client_id,
            "name": client.name,
            "country": client.country,
            "total_spent": total_ventas_client(sales, client.client_id),
            "sale_count": num_ventas_client(sales, client.client_id),
            "average_sale": promedio_ventas_client(sales, client.client_id),
        })
    return stats


# ------------------------------------------------------------------
# CÁLCULOS 6 AL 10
# ------------------------------------------------------------------

def calc_top_client_by_country(clients, sales):
    """Cálculo 6: cliente que más gasta en cada país."""
    client_country = ClientCollection(clients)
    result = {}
    for country in sorted(set(map(lambda c: c.country, clients))):
        group = client_country.clients_by_country(country)
        best = max(group, key=lambda c: total_ventas_client(sales, c.client_id))
        result[country] = best.name
    return result


def calc_sales_by_category(sales):
    """Cálculo 7: total vendido por categoría."""
    categories = sorted(set(map(lambda s: s.category, sales)))
    return {
        cat: round(sum_amounts(filter_sales_by_category(sales, cat)), 2)
        for cat in categories
    }


def calc_top_client_by_category_count(clients, sales, category="Electronics"):
    """Cálculo 8: cliente con más compras en una categoría."""
    cat_sales = filter_sales_by_category(sales, category)
    best = max(
        clients,
        key=lambda c: len(filter_sales_by_client(cat_sales, c.client_id)),
    )
    return best.name


def calc_high_spending_clients(clients, sales, limit=500):
    """Cálculo 9: nombres de los clientes que gastan más de `limit`."""
    return [
        c.name for c in clients
        if total_ventas_client(sales, c.client_id) > limit
    ]


def calc_monthly_sales(sales):
    """Cálculo 10: total vendido por mes (formato 'AAAA-MM')."""
    months = sorted(set(map(lambda s: s.date[:7], sales)))
    return {
        month: round(sum_amounts(filter_sales_by_month(sales, month)), 2)
        for month in months
    }


# ------------------------------------------------------------------
# PANDAS: cruce de ventas y clientes
# ------------------------------------------------------------------

def build_sales_detail(clients, sales):
    """Cruza ventas y clientes con pandas y devuelve el detalle por venta."""
    df_sales = pd.DataFrame([s.to_dict() for s in sales])
    df_clients = pd.DataFrame(
        [{"client_id": c.client_id, "client_name": c.name, "country": c.country}
         for c in clients]
    )
    merged = df_sales.merge(df_clients, on="client_id", how="left")
    return merged[["sale_id", "client_name", "country", "product",
                   "category", "amount", "date"]].to_dict(orient="records")


# ------------------------------------------------------------------
# REPORTE FINAL
# ------------------------------------------------------------------

def generate_report():
    """Carga los datos, calcula las 10 métricas y devuelve el reporte."""
    clients = load_clients()
    sales = load_sales()

    return {
        "summary": {
            "total_clients": calc_total_clients(clients),
            "total_sales": calc_total_sales(sales),
            "total_revenue": round(sum_amounts(sales), 2),
        },
        "clients": calc_client_stats(clients, sales),
        "top_client_by_country": calc_top_client_by_country(clients, sales),
        "sales_by_category": calc_sales_by_category(sales),
        "top_client_electronics": calc_top_client_by_category_count(clients, sales),
        "high_spending_clients": calc_high_spending_clients(clients, sales),
        "monthly_sales": calc_monthly_sales(sales),
        "sales_detail": build_sales_detail(clients, sales),
    }


def save_report(report, path=REPORT_FILE):
    """Guarda el reporte en un archivo JSON y devuelve la ruta."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
    return path


if __name__ == "__main__":
    print(f"Reporte guardado en: {save_report(generate_report())}")