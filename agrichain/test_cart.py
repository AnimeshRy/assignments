import unittest
from main import Cart, Product

class TestCart(unittest.TestCase):
    def setUp(self):
        """Set up a cart with test products before each test"""
        self.cart = Cart()
        self.cart.add_product('A', 50, 3, 130)  # 3 for 130
        self.cart.add_product('B', 30, 2, 45)   # 2 for 45
        self.cart.add_product('C', 20, 3, 50)   # 3 for 50
        self.cart.add_product('D', 15, 2, 25)   # 2 for 25

    def test_single_product_no_discount(self):
        """Test buying single products without triggering discounts"""
        total = self.cart.calculate_total_from_input("A")
        self.assertEqual(total, 50)

        total = self.cart.calculate_total_from_input("B")
        self.assertEqual(total, 30)

    def test_multiple_products_no_discount(self):
        """Test buying multiple products without triggering discounts"""
        total = self.cart.calculate_total_from_input("AB")
        self.assertEqual(total, 80)  # A(50) + B(30)

    def test_single_product_with_discount(self):
        """Test buying products with quantity discount"""
        total = self.cart.calculate_total_from_input("AAA")  # 3 A's
        self.assertEqual(total, 130)

        total = self.cart.calculate_total_from_input("BB")  # 2 B's
        self.assertEqual(total, 45)

    def test_multiple_products_with_discount(self):
        """Test buying multiple products with some qualifying for discount"""
        total = self.cart.calculate_total_from_input("AAABB")  # 3A's(130) + 2B's(45)
        self.assertEqual(total, 175)

    def test_products_exceeding_discount_quantity(self):
        """Test buying more items than the discount quantity"""
        total = self.cart.calculate_total_from_input("AAAA")  # 3A's(130) + 1A(50)
        self.assertEqual(total, 180)

    def test_invalid_products(self):
        """Test that invalid product codes are ignored"""
        total = self.cart.calculate_total_from_input("AX")  # X is invalid
        self.assertEqual(total, 50)  # Only 'A' should be counted

    def test_empty_input(self):
        """Test empty input string"""
        total = self.cart.calculate_total_from_input("")
        self.assertEqual(total, 0)

    def test_mixed_case_scenario(self):
        """Test a complex scenario with multiple products and discounts"""
        total = self.cart.calculate_total_from_input("AAABBBCCCDDD")
        self.assertEqual(total, 295)

if __name__ == '__main__':
    unittest.main()
