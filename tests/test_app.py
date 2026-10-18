"""Application tests, including a real local HTTP endpoint check."""
import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from app.info import format_student_info, get_student_info
from app.main import StudentHandler


class StudentInfoTests(unittest.TestCase):
    def test_student_info_from_config(self):
        info = get_student_info(environ={})
        self.assertTrue(all(info.values()))
        self.assertIn("student_id", info)

    def test_environment_overrides(self):
        info = get_student_info(environ={
            "STUDENT_NAME": "DockerUser", "STUDENT_GROUP": "SE-0000"})
        self.assertEqual(info["name"], "DockerUser")
        self.assertEqual(info["group"], "SE-0000")

    def test_formatted_information(self):
        info = get_student_info(environ={})
        output = format_student_info(info)
        self.assertIn(info["surname"], output)
        self.assertIn("Application is running successfully!", output)


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), StudentHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=3)

    def test_health_endpoint(self):
        with urllib.request.urlopen(self.base_url + "/health") as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(json.loads(response.read()), {"status": "ok"})

    def test_student_info_endpoint(self):
        with urllib.request.urlopen(self.base_url + "/") as response:
            body = response.read().decode("utf-8")
        self.assertIn("Student ID:", body)
        self.assertIn(get_student_info()["name"], body)

    def test_unknown_path(self):
        with self.assertRaises(urllib.error.HTTPError) as error:
            urllib.request.urlopen(self.base_url + "/missing")
        self.assertEqual(error.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
