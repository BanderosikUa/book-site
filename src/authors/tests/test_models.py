from django.test import TestCase

from hitcount.utils import get_hitcount_model

from ..models import Author


class TestAuthorModel(TestCase):
    """Tests for Author's model"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.trial = Author.objects.create(name='test author')

    def test_create_defualt_hitcount_genre(self):
        """Testing if add default hit to author"""
        expected_hits = 1

        author = self.trial
        hit_count = get_hitcount_model().objects.get_for_object(author)
        real_hits = hit_count.hits

        self.assertEqual(expected_hits, real_hits)
