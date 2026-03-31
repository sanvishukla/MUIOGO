import unittest
import sys
import os
from pathlib import Path

# Add project root to sys.path to allow importing API.app
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "API"))

class SmokeTest(unittest.TestCase):
    def setUp(self):
        """Initialize the Flask test client."""
        try:
            from app import app
            app.config['TESTING'] = True
            app.config['DEBUG'] = False
            self.app = app.test_client()
        except ImportError as e:
            self.fail(f"Failed to import API.app: {e}")
        except Exception as e:
            self.fail(f"Failed to initialize Flask app: {e}")

    def test_app_import(self):
        """Basic check if the app module can be imported."""
        import app
        self.assertIsNotNone(app.app)

    def test_index_route(self):
        """Check if the home route returns 200."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_session_route(self):
        """Check if /getSession returns 200 (even if session is empty)."""
        response = self.app.get('/getSession')
        self.assertEqual(response.status_code, 200)
        self.assertIn('session', response.get_json())

    def test_get_cases_route(self):
        """Check if /getCases returns 200 or 404 (handled error)."""
        response = self.app.get('/getCases')
        # /getCases returns 200 with list or 404 if directory error
        self.assertIn(response.status_code, [200, 404])

    def test_config_validity(self):
        """Verify that the Config class resolves paths correctly."""
        from Classes.Base import Config
        self.assertTrue(Config.BASE_DIR.exists())
        self.assertTrue(Config.WEBAPP_PATH.exists())
        # Note: We don't check for writability here as per 'read-only' constraint,
        # but we check if the paths are resolved to the correct absolute locations.
        self.assertIn("MUIOGO", str(Config.BASE_DIR))

if __name__ == '__main__':
    unittest.main()
