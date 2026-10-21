class SalesCollection:
    def __init__(self, sales):
        self.sales = sales

    def sales_by_client(self, client_id):
        resultado = []
        for sale in self.sales:
            if sale.client_id == client_id:
                resultado.append(sale)
        return resultado
    
    def total_amount_by_client(self, client_id):
        total = 0
        for sale in self.sales_by_client(client_id):
            total += sale.amount
        return total

    def total_amount_by_category(self, category):
        total = 0
        for sale in self.sales:
            if sale.category == category:
                total += sale.amount 
        return total 

    def average_sale_by_client(self, client_id):
        ventas = self.sales_by_client(client_id)
        if len(ventas) == 0:
            return 0
        return self.total_amount_by_client(client_id) / len(ventas)

    