# Test books APIs
# Author: Carmine Giardino
import requests
url = "http://andrewbeatty1.pythonanywhere.com/books"

def read_books():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        books = response.json()  # Parse the JSON response
        return books
    except requests.exceptions.RequestException as e:
        print(f"An error while reading books occurred: {e}")
        return None

def read_book(book_id):
    try:
        response = requests.get(f"{url}/{book_id}")
        response.raise_for_status()  # Check if the request was successful
        book = response.json()  # Parse the JSON response
        return book
    except requests.exceptions.RequestException as e:
        print(f"An error while read book occurred: {e}")
        return None

def create_book(book: dict) :
    try:
        response = requests.post(url, json=book)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error while creating book occurred: {e}")
        return None

def update_book(book_id: str, book: dict) :
    try:
        response = requests.put(f"{url}/{book_id}", json=book)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error while updating book occurred: {e}")
        return None
    
def delete_book(book_id: str) :
    try:
        response = requests.delete(f"{url}/{book_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error while deleting book occurred: {e}")
        return None
    
if __name__ == "__main__":
    #print(read_books())
    #print(read_book("1643"))
    #book = {"title": "The Great Gatsby 2", "author": "Carmine Giardino", "price": 124}
    #print(create_book(book))
    #book = {"title": "The Great Gatsby 3", "author": "Carmine Giardino", "price": 124}
    #print(update_book("1645", book))
    #print(delete_book("1645"))
    print(read_books())
    