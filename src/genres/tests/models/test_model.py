# from django.test import TestCase

# from hitcount.utils import get_hitcount_model

# from ..models import Genre

# class TestBookModel(TestCase):
#     """Tests for Genres's model"""

#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         cls.trial = Genre.objects.create(name='test genre')

#     def test_create_defualt_hitcount_genre(self):
#         """Testing if add default hit to genre"""
#         expected_hits = 1

#         genre = self.trial
#         hit_count = get_hitcount_model().objects.get_for_object(genre)
#         real_hits = hit_count.hits

#         self.assertEqual(expected_hits, real_hits)
