from flask import Flask
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/books", methods=["GET"])
def getAll():
    return (
        "all books"
    )

@app.route("/books", methods=["POST"])
def create():
    book = request.get_json()
    return(
        f"created book with json{book}"
    )

@app.route("/books/<int:book_id>", methods=["GET"])
def findById(book_id):
    return (
        f"book with id {book_id}"
    )

@app.route("/books/<int:book_id>", methods=["PUT"])
def update(book_id):
    book = request.get_json()
    return( f"updated book with id {book_id} with json{book}" )

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete(book_id):
    return( f"deleted book with id {book_id}" )


if __name__ == "__main__":
    app.run(debug=True)