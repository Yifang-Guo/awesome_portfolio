import os
os.environ['TESTING'] = 'true'
import unittest
from app import app

# Ensure the app runs in testing mode and uses a temporary database

class TestPortfolioApp(unittest.TestCase):
    """
    Test suite for the main Flask portfolio application.
    Covers homepage rendering, timeline API, and input validation.
    """
    def setUp(self):
        # Create a test client for the Flask app
        self.client = app.test_client()

    # --- Homepage Tests ---
    def test_homepage_renders_correctly(self):
        """Check that the homepage loads and contains key sections."""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        html = resp.get_data(as_text=True)
        # Check for expected HTML elements and sections
        self.assertIn("<title>MLH Fellow</title>", html)
        self.assertIn('<header class="navbar', html)
        self.assertIn('<div class="profile">', html)
        self.assertIn('<section id="about"', html)
        self.assertIn('id="education"', html)
        self.assertIn('id="experience-section"', html)
        self.assertIn('id="map"', html)

    # --- Timeline API Tests ---
    def test_timeline_api_crud(self):
        """Test timeline API: empty state, post creation, and retrieval."""
        # Should start empty
        resp = self.client.get("/api/timeline_post")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        # Accept both list or dict with 'timeline_posts'
        if isinstance(data, list):
            self.assertEqual(len(data), 0)
        elif isinstance(data, dict):
            self.assertIn('timeline_posts', data)
            self.assertEqual(len(data['timeline_posts']), 0)

        # Add a valid post
        post_data = {
            "name": "Test User",
            "email": "test@example.com",
            "content": "This is a test post."
        }
        resp = self.client.post("/api/timeline_post", data=post_data)
        self.assertIn(resp.status_code, (200, 201))
        post = resp.get_json()
        self.assertEqual(post["name"], post_data["name"])
        self.assertEqual(post["email"], post_data["email"])
        self.assertEqual(post["content"], post_data["content"])

        # Confirm the post is now present
        resp = self.client.get("/api/timeline_post")
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        if isinstance(data, list):
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["name"], post_data["name"])
        elif isinstance(data, dict):
            self.assertIn('timeline_posts', data)
            self.assertEqual(len(data['timeline_posts']), 1)
            self.assertEqual(data['timeline_posts'][0]["name"], post_data["name"])

    def test_timeline_api_missing_fields(self):
        """Test posting with missing or invalid fields returns errors."""
        # Missing email
        resp = self.client.post("/api/timeline_post", data={
            "name": "Incomplete User",
            "email": "",
            "content": "Missing email"
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.get_json())

        # Missing name
        resp = self.client.post("/api/timeline_post", data={
            "name": "",
            "email": "test@example.com",
            "content": "Missing name"
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.get_json())

        # Missing content
        resp = self.client.post("/api/timeline_post", data={
            "name": "Test",
            "email": "test@example.com",
            "content": ""
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn("error", resp.get_json())

    # --- Malformed Input Tests ---
    def test_timeline_api_malformed_input(self):
        """Test that malformed input is rejected with clear errors."""
        # No name
        resp = self.client.post("/api/timeline_post", data={
            "email": "john@example.com",
            "content": "Hello world, I'm John!"
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Invalid name", resp.get_data(as_text=True))

        # Empty content
        resp = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "john@example.com",
            "content": ""
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Invalid content", resp.get_data(as_text=True))

        # Bad email
        resp = self.client.post("/api/timeline_post", data={
            "name": "John Doe",
            "email": "not-an-email",
            "content": "Hello world, I'm John!"
        })
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Invalid email", resp.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main() 