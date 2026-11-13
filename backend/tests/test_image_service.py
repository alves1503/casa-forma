import base64
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app.services.image_service import create_room_preview
from app.seed import SEED_ADMIN_PASSWORD_HASH
from app.services.password_service import hash_password, verify_password


class ImageServiceTests(unittest.TestCase):
    def test_seeded_admin_password_matches_its_hash(self):
        self.assertTrue(
            verify_password(
                "3_kFWYsLZJ1EYZCtpZHRMZaRlescNxfi",
                SEED_ADMIN_PASSWORD_HASH,
            )
        )
        self.assertFalse(verify_password("incorrect-password", SEED_ADMIN_PASSWORD_HASH))

    def test_password_hashes_are_salted(self):
        first_hash = hash_password("test-password")
        second_hash = hash_password("test-password")
        self.assertNotEqual(first_hash, second_hash)
        self.assertTrue(verify_password("test-password", first_hash))

    @patch("app.services.image_service.OpenAI")
    def test_sends_room_and_uploaded_product_image_as_references(self, openai_class):
        openai = openai_class.return_value
        openai.images.edit.return_value = SimpleNamespace(
            data=[SimpleNamespace(b64_json=base64.b64encode(b"preview").decode("ascii"))]
        )

        result = create_room_preview(
            room_image=b"room",
            room_content_type="image/png",
            furniture_image=b"product",
            furniture_content_type="image/webp",
            furniture={"name": "Sofá Aurora", "prompt": "green three-seat sofa"},
            api_key="test-key",
            model="gpt-image-2.5-sunburst",
        )

        self.assertEqual(result, b"preview")
        call = openai.images.edit.call_args.kwargs
        self.assertEqual(call["quality"], "low")
        self.assertEqual(len(call["image"]), 2)
        self.assertEqual(call["image"][0][2], "image/png")
        self.assertEqual(call["image"][1][2], "image/webp")
        self.assertIn("Treat the second image as the authoritative reference", call["prompt"])


if __name__ == "__main__":
    unittest.main()
