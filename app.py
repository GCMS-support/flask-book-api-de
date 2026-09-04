from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
]


def find_book_by_id(book_id):
    """Return the book with book_id, or None if it does not exist."""
    return next((book for book in books if book['id'] == book_id), None)


@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'POST':
        new_book = request.get_json()
        new_id = max(book['id'] for book in books) + 1
        new_book['id'] = new_id
        books.append(new_book)
        return jsonify(new_book), 201

    return jsonify(books)


@app.route('/api/books/<int:id>', methods=['PUT'])
def handle_book(id):
    book = find_book_by_id(id)
    if book is None:
        return '', 404

    new_data = request.get_json()
    book.update(new_data)
    return jsonify(book)


@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = find_book_by_id(id)
    if book is None:
        return '', 404

    books.remove(book)
    return jsonify(book)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
