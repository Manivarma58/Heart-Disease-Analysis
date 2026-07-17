import unittest
from app import create_app


class SmokeTestCase(unittest.TestCase):
    def test_index_loads(self):
        app = create_app()
        app.config["TESTING"] = True
        client = app.test_client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_visualizations_data(self):
        app = create_app()
        app.config["TESTING"] = True
        client = app.test_client()
        with client.session_transaction() as sess:
            sess["user"] = {
                "name": "Ramesh Iyer",
                "email": "ramesh@cardioviz.local",
                "role": "Health Official",
                "persona": "public_health"
            }
        response = client.get("/api/visualizations-data")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("gender_hd", data)
        self.assertIn("age_hd", data)
        self.assertIn("diabetic_stroke", data)
        self.assertIn("smoking_alcohol", data)
        self.assertIn("other_diseases", data)
        self.assertIn("race_hd", data)
        self.assertIn("gen_health_hd", data)
        self.assertIn("activity_hd", data)
        self.assertIn("age_bmi_diabetic", data)
        self.assertIn("stroke_overlap", data)


if __name__ == "__main__":
    unittest.main()
