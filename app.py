from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/api/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        books_list = [
            {"id": 1, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"},
            {"id": 2, "title": "1984", "author": "George Orwell"},
        ]
        return jsonify(books_list)

    new_book = request.get_json()
    return jsonify(new_book), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
