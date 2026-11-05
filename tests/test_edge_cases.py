from src.analyze import (
    promedio_ventas_client,
    total_ventas_client,
    calc_sales_by_category,
    calc_high_spending_clients,
    calc_monthly_sales,
)
from src.client import Client
from src.sale import Sale


def _sales():
    return [
        Sale("S1", 1, "Laptop", "Electronics", 600.0, "2023-07-01"),
        Sale("S2", 1, "Mouse", "Accessories", 20.0, "2023-08-02"),
    ]


def test_client_without_sales_average_is_zero():
    assert promedio_ventas_client(_sales(), 99) == 0


def test_client_without_sales_total_is_zero():
    assert total_ventas_client(_sales(), 99) == 0


def test_sales_by_category_only_existing():
    assert set(calc_sales_by_category(_sales())) == {"Electronics", "Accessories"}


def test_high_spending_limit():
    clients = [
        Client(1, "Ana", "Spain", "2022-01-01"),
        Client(2, "Luis", "Spain", "2022-01-01"),
    ]
    assert calc_high_spending_clients(clients, _sales()) == ["Ana"]


def test_monthly_sales_two_months():
    assert calc_monthly_sales(_sales()) == {"2023-07": 600.0, "2023-08": 20.0}