import base64
import io
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient
from PIL import Image

from app.config import Settings
from app.main import create_app
from app.models.furniture import FURNITURE
from app.services.password_service import hash_password


def image_bytes(image_format="JPEG", color="beige"):
    image = Image.new("RGB", (32, 24), color=color)
    output = io.BytesIO()
    image.save(output, format=image_format)
    return output.getvalue()


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        root = Path(self.temporary_directory.name)
        self.admin_password_hash = hash_password("test-password")
        settings = replace(
            Settings.from_environment(),
            openai_api_key="test-key",
            mysql_host="localhost",
            mysql_port=3306,
            mysql_database="test_catalog",
            mysql_user="test_user",
            mysql_password="test_password",
            upload_directory=root / "uploads",
        )
        self.app = create_app(settings)
        self.seed_patch = patch("app.main.seed_database")
        self.seed_patch.start()
        self.client_context = TestClient(self.app)
        self.client = self.client_context.__enter__()

    def tearDown(self):
        self.client_context.__exit__(None, None, None)
        self.seed_patch.stop()
        self.temporary_directory.cleanup()

    def test_catalog_lists_seeded_products_and_references(self):
        seeded_items = [{**item, "is_demo": True} for item in FURNITURE]
        with patch("app.controllers.catalog_controller.get_all_furniture", return_value=seeded_items):
            response = self.client.get("/api/furniture")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 6)
        self.assertTrue(response.json()[0]["photo_url"].startswith("/media/demo/"))
        self.assertTrue(response.json()[0]["is_demo"])

    def test_swagger_ui_loads_the_openapi_yaml_file(self):
        docs_response = self.client.get("/docs")
        spec_response = self.client.get("/openapi.yaml")

        self.assertEqual(docs_response.status_code, 200)
        self.assertIn("/openapi.yaml", docs_response.text)
        self.assertEqual(spec_response.status_code, 200)
        self.assertIn("application/yaml", spec_response.headers["content-type"])
        self.assertIn("/api/admin/session:", spec_response.text)
        self.assertIn("HTTPBasic:", spec_response.text)
        self.assertIn("/api/preview:", spec_response.text)

    def test_admin_requires_valid_credentials(self):
        record = {"username": "admin", "password_hash": self.admin_password_hash}
        seeded_items = [{**item, "is_demo": True} for item in FURNITURE]
        with patch("app.services.admin_auth.get_admin_user", return_value=record):
            self.assertEqual(self.client.get("/api/admin/furniture").status_code, 401)
            invalid = self.client.get("/api/admin/furniture", auth=("admin", "wrong"))
            self.assertEqual(invalid.status_code, 401)
            with patch("app.controllers.admin_controller.get_all_furniture", return_value=seeded_items):
                valid = self.client.get(
                    "/api/admin/furniture",
                    auth=("admin", "test-password"),
                )
        self.assertEqual(valid.status_code, 200)

    def test_admin_can_replace_a_reference_photo(self):
        item = {**FURNITURE[0], "is_demo": True}
        photo_path = {"value": item["photo_path"]}

        def find_furniture(_settings, _furniture_id):
            return {**item, "photo_path": photo_path["value"], "is_demo": not photo_path["value"].startswith("uploads/")}

        def update_photo(_settings, _furniture_id, new_path):
            photo_path["value"] = new_path
            return True

        with (
            patch("app.services.admin_auth.get_admin_user", return_value={
                "username": "admin",
                "password_hash": self.admin_password_hash,
            }),
            patch("app.controllers.admin_controller.get_furniture", side_effect=find_furniture),
            patch("app.controllers.admin_controller.update_furniture_photo", side_effect=update_photo),
        ):
            response = self.client.post(
                "/api/admin/furniture/sofa-aurora/photo",
                files={"photo": ("custom.png", image_bytes("PNG", "red"), "image/png")},
                auth=("admin", "test-password"),
            )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["is_demo"])
        self.assertTrue(response.json()["photo_url"].startswith("/media/uploads/"))

        image_response = self.client.get(response.json()["photo_url"])
        self.assertEqual(image_response.status_code, 200)
        self.assertEqual(image_response.headers["content-type"], "image/png")
        image_response.close()

    def test_admin_rejects_invalid_image_upload(self):
        item = {**FURNITURE[0], "is_demo": True}
        with (
            patch("app.services.admin_auth.get_admin_user", return_value={
                "username": "admin",
                "password_hash": self.admin_password_hash,
            }),
            patch("app.controllers.admin_controller.get_furniture", return_value=item),
        ):
            response = self.client.post(
                "/api/admin/furniture/sofa-aurora/photo",
                files={"photo": ("bad.jpg", b"not an image", "image/jpeg")},
                auth=("admin", "test-password"),
            )
        self.assertEqual(response.status_code, 400)

    @patch("app.controllers.preview_controller.create_room_preview", return_value=b"generated-image")
    def test_preview_uses_selected_catalog_photo(self, create_preview):
        item = {**FURNITURE[0], "is_demo": True}
        demo_image = Settings.from_environment().demo_image_directory / "sofa-aurora.jpg"
        with (
            patch("app.controllers.preview_controller.get_furniture", return_value=item),
            patch("app.controllers.preview_controller.resolve_media_path", return_value=demo_image),
        ):
            response = self.client.post(
                "/api/preview",
                files={"room_photo": ("room.jpg", image_bytes(), "image/jpeg")},
                data={"furniture_id": "sofa-aurora"},
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["image"],
            f"data:image/png;base64,{base64.b64encode(b'generated-image').decode('ascii')}",
        )
        self.assertEqual(create_preview.call_args.args[4]["id"], "sofa-aurora")
        self.assertGreater(len(create_preview.call_args.args[2]), 0)

    def test_preview_rejects_unknown_furniture(self):
        with patch("app.controllers.preview_controller.get_furniture", return_value=None):
            response = self.client.post(
                "/api/preview",
                files={"room_photo": ("room.jpg", image_bytes(), "image/jpeg")},
                data={"furniture_id": "not-in-the-catalog"},
            )
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
