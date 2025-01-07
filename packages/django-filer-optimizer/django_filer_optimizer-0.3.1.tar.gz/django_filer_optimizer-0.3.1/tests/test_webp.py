"""Unit Tests for the module"""

import os
import logging

from django.test import TestCase
from django.core.files import File as DjangoFile
from django.urls import reverse

from filer.models.imagemodels import Image

from tests.helpers import create_image, create_superuser

LOGGER = logging.getLogger(name="django-filer-optimizer")


class TestCase(TestCase):
    """Test Case for django-filer-optimizer"""

    def setUp(self):
        """Set up common assets for tests"""
        LOGGER.debug("Tests setUp")
        self.superuser = create_superuser()
        self.client.login(username="admin", password="secret")
        self.img = create_image()
        self.image_name = "test_file.jpg"
        self.filename = os.path.join(os.path.dirname(__file__), self.image_name)
        self.img.save(self.filename, "JPEG")
        with open(self.filename, "rb") as upload:
            self.file_object = Image.objects.create(
                file=DjangoFile(upload, name=self.image_name)
            )
        super().setUp()

    def tearDown(self):
        """Remove Test Data"""
        LOGGER.debug("Tests tearDown")
        self.client.logout()
        os.remove(self.filename)
        for img in Image.objects.all():
            img.delete()
        super().tearDown()

    # @patch('filer_optimizer.signals.image_optimizer.send')
    def test_upload_image_form(self, extra_headers={}):

        # self.assertEqual(Image.objects.count(), 0)
        with open(self.filename, "rb") as fh:
            file_obj = DjangoFile(fh)
            url = reverse("admin:filer-ajax_upload")
            post_data = {
                "Filename": self.image_name,
                "Filedata": file_obj,
                "jsessionid": self.client.session.session_key,
            }
            response = self.client.post(url, post_data, **extra_headers)  # noqa
            # self.assertEqual(Image.objects.count(), 1)
            stored_image = Image.objects.first()
            # self.assertEqual(stored_image.original_filename, self.image_name)
            self.assertEqual(stored_image.mime_type, "image/jpeg")

        # # Check that your signal was called.
        # self.assertTrue(mock.called)
        #
        # # Check that your signal was called only once.
        # self.assertEqual(mock.call_count, 1)
