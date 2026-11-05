# PROYECTO-FINAL-MUSK

Carga datos desde un JSON (clientes) y un CSV (ventas), los cruza, calcula 10 metricas y genera un reporte final en JSON.

## Tecnologias
- Programacion orientada a objetos (Client, Sale, ClientCollection, SalesCollection)
- Programacion funcional (filter, map, reduce)
- Pandas (cruce de ventas y clientes)
- GitHub Actions y tests automaticos con pytest

## Estructura
- src/: codigo fuente
- data/: clients.json y sales.csv
- tests/: tests automaticos
- final_report.json: reporte generado

## Instalacion (Windows)
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt

## Uso
Desde la raiz del proyecto:

    python -m src.analyze

El resultado se guarda en final_report.json.

## Las 10 metricas
1. Total de clientes
2. Total de ventas
3. Total gastado por cliente
4. Numero de ventas por cliente
5. Promedio de gasto por venta y cliente
6. Mejor cliente por pais
7. Ventas por categoria
8. Cliente con mas compras en Electronics
9. Clientes de alto gasto (mas de 500)
10. Ventas por mes

## Tests
    python -m pytest -q

## Validacion automatica
Cada push ejecuta GitHub Actions y lanza los tests.