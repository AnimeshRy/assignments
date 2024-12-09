# Agrichain Assign

Input:
Implement the code for a supermarket checkout process that calculates the total
price of items added in the cart by the customer. In our store, we’ll use individual
letters of the alphabet (A, B, C, and so on) to represent items. Products can be
purchased at their individual pricing or at a discounted price when purchased in
groups as listed below: For example, item ‘A’ might cost 50 cents individually, but
this week we have a special offer: buy three ‘A’s and they’ll cost you $1.30. Product
pricing for this week is as below::

Our checkout accepts items in any order, so that if we scan product B, then product
A, and then another product B, we’ll recognize the two B’s and price them at a
discounted price of Rs 45 instead of individual pricing of Rs 30, which brings the
Total order pricing to Rs 95.
Examples:

INPUT OUTPUT
“” 0
“A” 50
“AB” 80
“CDBA” 115
“AA” 100
“AAA” 130
“AAAA” 180
“AAAAA” 230
“AAAAAA” 260
“AAAB” 160
“AAABB” 175
“AAABBD” 190
“DABABA” 190


### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/AnimeshRy/assignments.git
cd assignments/agrichain
```

2. Make sure you have Python 3.9 or higher installed:
```bash
python --version
```

3. Run the application:
```bash
python main.py
```

4. Run the tests:
```bash
python -m unittest test_cart.py -v
```

### Docker Setup

1. Build the Docker image:
```bash
docker build -t cart-app .
```
2. Run the containerized application:
```bash
docker run -it cart-app
```
