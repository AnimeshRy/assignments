from collections import Counter


class Product:
    def __init__(self, name, regular_price, discount_qty=None, discount_price=None):
        self.name = name
        self.regular_price = regular_price
        self.discount_qty = discount_qty
        self.discount_price = discount_price

    def calculate_price(self, quantity):
        """
        Calculate price of product on qty and apply discount if reqd.
        """
        if self.discount_qty and quantity >= self.discount_qty:
            discount_units = quantity // self.discount_qty
            remaining_units = quantity % self.discount_qty
            return discount_units * self.discount_price + remaining_units * self.regular_price
        else:
            return quantity * self.regular_price


class Cart:
    def __init__(self):
        self.products = {}

    def add_product(self, name, regular_price, discount_qty=None, discount_price=None):
        self.products[name] = Product(name, regular_price, discount_qty, discount_price)

    def calculate_total_from_input(self, input_string):
        """
        Calculate the total price of the cart based on the input string.
        Ignores invalid product characters.
        """
        input_counts = Counter(input_string)

        total_price = 0
        for product_name, quantity in input_counts.items():
            if product_name in self.products:
                product = self.products[product_name]
                total_price += product.calculate_price(quantity)
            else:
                print(f"Warning: '{product_name}' is not a valid product and will be ignored.")

        return total_price


def main():
    cart = Cart()
    cart.add_product('A', 50, 3, 130)
    cart.add_product('B', 30, 2, 45)
    cart.add_product('C', 20, 3, 50)
    cart.add_product('D', 15, 2, 25)

    print("Enter the product sequence (e.g., DABABA):")
    input_string = input().strip()

    total_price = cart.calculate_total_from_input(input_string)
    print(f"Total Price: {total_price}")


if __name__ == "__main__":
    main()
