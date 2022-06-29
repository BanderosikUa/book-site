import os, django
import csv
import lorem
import urllib
import string
import random
import numpy as np

from tqdm import tqdm
from time import sleep
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from django.urls import reverse
from django.test import Client
from django.core.files import File  # you need this somewhere
from django.core.exceptions import MultipleObjectsReturned

from Genres.models import Genre
from Authors.models import Author
from Books.models import Book, UserBookRelation
from users.models import CustomUser


class FillDbWithDataClass:
    """Class to fill db with data from book database and lorem description.
    Usage: assign class to some variable and then call this variable as function"""
    file_path = BASE_DIR.joinpath('staticfiles') / 'main_dataset.csv'
    imgs_path = BASE_DIR.joinpath('staticfiles')\
                        .joinpath('book-covers')

    def __init__(self, genre_amount: int, book_amount: int = 100):
        self.book_amount = book_amount
        self.genre_amount = genre_amount

    def __create_books(self):
        """Main function that read a csvfile and create book and
        random userbookrelation"""
        with open(self.file_path) as csvfile:
            csvreader = csv.reader(csvfile)
            columns_names = next(csvreader)
            genre_list = []

            for row in tqdm(csvreader):

                name = row[columns_names.index('name')]
                author = row[columns_names.index('author')]
                genre = row[columns_names.index('category')]
                genre_list.append(genre)
                if self.genre_amount:
                    if len(genre_list) == self.genre_amount:
                        break

                if Book.objects.filter(genre__name=genre).count() == self.book_amount:
                    continue

                photo_url = self.imgs_path / row[columns_names.index('img_paths')].split('dataset/')[1]
                
                try:
                    genre_obj = Genre.objects.get_or_create(name=genre)[0]
                    author_obj = Author.objects.get_or_create(
                        name=author,
                        defaults={'biography': lorem.text()}
                        )[0]
                    if not Book.objects.filter(name__iexact=name).exists():
                        book = Book.objects.create(
                            name=name,
                            author=author_obj,
                            about=lorem.text()
                            )
                        book.genre.add(genre_obj)
                        book.photo.save(photo_url.split('/')[-1],
                                        File(open(photo_url, 'rb')))
                        book.save()
                        
                        self.__create_userbookrelation(book)
                except MultipleObjectsReturned:
                    continue
    
    def _add_photos(self):
        """Function that separately add photos to book,
        use if something went wrong"""
        with open(self.file_path) as csvfile:
            csvreader = csv.reader(csvfile)
            columns_names = next(csvreader)

            for row in tqdm(csvreader):

                name = row[columns_names.index('name')]
                if Book.objects.filter(name__iexact=name).exists():
                    book = Book.objects.get(name__iexact=name)
                    photo_url = self.imgs_path / row[columns_names.index('img_paths')].split('dataset/')[1]
                    book.photo.save(photo_url.name,
                                    File(open(photo_url, 'rb')))
                    book.save()

    def __create_users(self):
        """Create 100 random users"""
        users_pk = []
        for count in range(100):
            username = "".join(random.choices(string.ascii_lowercase, k=8))
            email = f'{username}@gmail.com'
            password = '12345678'
            user = CustomUser.objects.create(username=username,
                                             password=password,
                                             email=email)
            users_pk.append(user.pk)
        return users_pk
    
    def __create_userbookrelation(self, book):
        """Creating random bookmark and rate"""
        for user in CustomUser.objects.filter(pk__in=self.users_pk):
            bookmark = random.choice([1, 2, 3, 4])
            rate = random.choice(list(range(6)))
            UserBookRelation.objects.create(book=book, user=user,
                                            bookmarks=bookmark, rate=rate)

    def __delete_old_users(self):
        CustomUser.objects.all().exclude(pk__lt=7).delete()

    def __delete_old_genres(self):
        Genre.objects.all().exclude(pk__in=[1, 2]).delete()
    
    def __delete_old_books(self):
        Book.objects.all().exclude(pk__in=[1, 2, 3, 4]).delete()

    @staticmethod
    def add_hit_default_hitcount(self, queryset):
        """Add 1 hitcount to all object in queryset, call this if
        something went wrong with hits"""
        client = Client()
        for object in tqdm(queryset):
            try:
                if not object.hit_count.hits:
                    url = reverse(object._meta.model_name, args=(object.slug,))
                    client.get(url)
            except:
                object.delete()

    def __call__(self):
        """Main execution function"""
        self.users_pk = self.__create_users()
        self.__delete_old_users()
        self.__delete_old_genres()
        self.__delete_old_books()
        self.__create_books()
        print('Done')


fill_data = FillDbWithDataClass()
fill_data()
