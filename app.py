from flask import Flask, abort, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
    {"id": 2, "title": "1984", "author": "George Orwell"},
] + [
    {"id": book_id, "title": f"Test Book {book_id}", "author": f"Author {book_id}"}
    for book_id in range(3, 103)
]


def find_book_by_id(book_id):
    """Return the book with book_id, or None if it does not exist."""
    return next((book for book in books if book['id'] == book_id), None)


def validate_book_data(data):
    """Return whether data contains the fields required for a book."""
    return isinstance(data, dict) and "title" in data and "author" in data


@app.errorhandler(404)
def not_found_error(_error):
    return jsonify({"error": "Not Found"}), 404


@app.errorhandler(405)
def method_not_allowed_error(_error):
    return jsonify({"error": "Method Not Allowed"}), 405


@app.route('/api/books', methods=['GET', 'POST'])
def handle_books():
    if request.method == 'POST':
        new_book = request.get_json(silent=True)
        if not validate_book_data(new_book):
            return jsonify({"error": "Invalid book data"}), 400

        new_id = max(book['id'] for book in books) + 1
        new_book['id'] = new_id
        books.append(new_book)
        return jsonify(new_book), 201

    author = request.args.get('author')
    filtered_books = books
    if author:
        filtered_books = [book for book in books if book.get('author') == author]

    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except ValueError:
        return jsonify({"error": "page and limit must be integers"}), 400

    if page < 1 or limit < 1:
        return jsonify({"error": "page and limit must be positive"}), 400

    start_index = (page - 1) * limit
    end_index = start_index + limit
    return jsonify(filtered_books[start_index:end_index])


@app.route('/api/books/<int:id>', methods=['PUT'])
def handle_book(id):
    book = find_book_by_id(id)
    if book is None:
        abort(404)

    new_data = request.get_json()
    book.update(new_data)
    return jsonify(book)


@app.route('/api/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = find_book_by_id(id)
    if book is None:
        abort(404)

    books.remove(book)
    return jsonify(book)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
