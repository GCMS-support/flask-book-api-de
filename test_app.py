import copy
import unittest

from app import app, books, limiter


INITIAL_BOOKS = copy.deepcopy(books)


class BookApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        books[:] = copy.deepcopy(INITIAL_BOOKS)
        limiter.reset()
        self.client = app.test_client()

    def test_get_filter_and_pagination(self):
        response = self.client.get("/api/books?page=1&limit=3")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 3)

        filtered = self.client.get("/api/books?author=George%20Orwell")
        self.assertEqual(filtered.status_code, 200)
        self.assertEqual(filtered.get_json()[0]["title"], "1984")

    def test_post_validates_and_creates_book(self):
        invalid = self.client.post("/api/books", json={"title": "Incomplete"})
        self.assertEqual(invalid.status_code, 400)

        created = self.client.post(
            "/api/books",
            json={"title": "The Hobbit", "author": "J. R. R. Tolkien"},
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.get_json()["id"], 103)

    def test_put_updates_and_validates_book(self):
        updated = self.client.put(
            "/api/books/1",
            json={"title": "Updated", "author": "New Author"},
        )
        self.assertEqual(updated.status_code, 200)
        self.assertEqual(updated.get_json()["title"], "Updated")

        invalid = self.client.put("/api/books/1", json={"title": "Incomplete"})
        self.assertEqual(invalid.status_code, 400)

    def test_delete_removes_book(self):
        deleted = self.client.delete("/api/books/2")
        self.assertEqual(deleted.status_code, 200)
        self.assertIsNone(next((book for book in books if book["id"] == 2), None))
        self.assertEqual(self.client.delete("/api/books/2").status_code, 404)

    def test_errors_are_json(self):
        self.assertEqual(self.client.get("/missing").status_code, 404)
        self.assertEqual(self.client.post("/api/books/1").status_code, 405)

    def test_rate_limit(self):
        statuses = [self.client.get("/api/books").status_code for _ in range(11)]
        self.assertEqual(statuses[:10], [200] * 10)
        self.assertEqual(statuses[10], 429)
        self.assertEqual(
            self.client.get("/api/books").get_json()["error"],
            "Rate limit exceeded",
        )

    def test_logging(self):
        with self.assertLogs(app.logger, level="INFO") as captured:
            self.client.get("/api/books?limit=1")
        self.assertTrue(any("GET request received" in line for line in captured.output))


if __name__ == "__main__":
    unittest.main()
