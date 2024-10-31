from typing import Dict, List
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: int
    stock:int 

    def update_stock(self, quantity: int) -> None:
        if(quantity > self.stock):
            raise NotEnoughStock('Not enough product in stock')
        
        self.stock = self.stock - quantity
        
    def __hash__(self):
        return hash(self.name) 
        

class Order(BaseModel):
    products: Dict[Product, int] = dict()

    def add_product(self, product: Product, quantity: int) -> None:

        try:
            product.update_stock(quantity)
        except NotEnoughStock as error:
            print(error)

        if(self.products.get(product) == None):
            self.products[product] = quantity
        else:
            self.products[product] = quantity + self.products.get(product)


    def remove_product(self, product: Product, quantity: int) -> None:
    
        if(self.products.get(product) - quantity == 0):
            self.products.pop(product)
        else:
            self.products[product] = self.products.get(product) - quantity

    def return_product(self, product: Product, quantity: int) -> None:
        if(self.products.get(product) - quantity < 1):
            self.products.pop(product)
        else:
            self.products[product] = self.products.get(product) - quantity
        
        try:
            product.update_stock(quantity= quantity * -1)
        except NotEnoughStock as error:
            print(error)

        

    def calculate_total(self) -> int:
        summ = 0
        for product in self.products:
            summ = summ + product.price * self.products.get(product)
        return summ

        


class Store(BaseModel):
    products: List[Product] = list()

    def add_product(self, product: Product):
        self.products.append(product)

    def list_products(self):
        print(self.products)    

    def create_order(self) -> Order:
        a = Order()
        return a

class NotEnoughStock(Exception):
    pass


store = Store()

product1 = Product(name= "Ноутбук", price= 1000, stock= 5)
product2 = Product(name= "Смартфон", price=  500, stock=  10)
print(product1)


store.add_product(product= product1)
store.add_product(product= product2)
store.list_products()

order = store.create_order()
order.add_product(product= product1, quantity= 2)
order.add_product(product= product2, quantity= 3)

print(order)

total = order.calculate_total()
print(f"Общая стоимость заказа: {total}")

store.list_products()

order.remove_product(product= product1, quantity= 1)

store.list_products()

print(order)

order.return_product(product= product1, quantity= 1)
print(order)
store.list_products()