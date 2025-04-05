import requests

BASE_URL = "http://localhost:8000"

# Создание корзины
response = requests.post(f"{BASE_URL}/cart")
cart_id = response.json()["id"]
print(f"Created cart with ID: {cart_id}")

# Получение информации о товарах
response = requests.get(f"{BASE_URL}/item")
items = response.json()
print(f"Available items: {items}")

# Добавление товара в корзину
if items:  # Check there are items
    first_item_id = items[0]["id"]
    response = requests.post(f"{BASE_URL}/cart/{cart_id}/add/{first_item_id}")
    print(f"Added item to cart: {response.json()}")

# Получение информации о корзине
response = requests.get(f"{BASE_URL}/cart/{cart_id}")
cart = response.json()
print(f"Cart details: {cart}")

# Создание нового товара
new_item_data = {"name": "Хлеб", "price": 30.0}
headers = {"Content-type": "application/json"}  # Add the header
response = requests.post(f"{BASE_URL}/item", json=new_item_data, headers=headers)
new_item = response.json()
print(f"Created new item: {new_item}")
