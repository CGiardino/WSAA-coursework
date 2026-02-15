# Find average book price
# Author: Carmine Giardino

import requests
url = "http://andrewbeatty1.pythonanywhere.com/books"

def get_average_price():
    response = requests.get(url)
    if response.status_code == 200:
        books = response.json()
        total_price = 0
        for book in books:
            if book['price'] is None:
                book['price'] = 0
            total_price += book['price']
        average_price = total_price / len(books) if books else 0
        return average_price
    else:
        print(f"Failed to retrieve books. Status code: {response.status_code}")
        return None
    
if __name__ == "__main__":
    print(f"The average price of all books is: {get_average_price():.2f} euro")
