import os, django
import csv
import lorem
import urllib
import string
import random
import numpy as np
from tqdm import tqdm
from time import sleep

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from Genres.models import Genre
from Authors.models import Author
from Books.models import Book, UserBookRelation
from users.models import CustomUser
from django.core.files import File  # you need this somewhere

class FillDbWithDataClass:
    def __init__(self):
        self.books = []
        self.users = []
        self.file_path = '/home/banderosik/Downloads/main_dataset.csv'
        self.imgs_path = '/home/banderosik/Downloads/book-covers/'


    def __create_books(self):
        with open(self.file_path) as csvfile:
            csvreader = csv.reader(csvfile)
            columns_names = next(csvreader)
            for row in csvreader:
                name = row[columns_names.index('name')]
                author = row[columns_names.index('author')]
                genre = row[columns_names.index('category')]
                photo_url = self.imgs_path+row[columns_names.index('img_paths')].split('dataset/')[1]
                author_obj = Author.objects.get_or_create(name=author)[0]
                genre_obj = Genre.objects.get_or_create(name=genre)[0]
                try:
                    if not Book.objects.filter(name=name).exists():
                        book = Book.objects.create(name=name, author=author_obj)
                        book.genre.add(genre_obj)
                        book.photo.save(photo_url.split('/')[-1],
                                        File(open(photo_url, 'rb')))
                        book.save()
                        self.books.append(book)
                except:
                    continue
    
    def __create_users(self):
        for count in range(100):
            username = random.choices(string.ascii_lowercase, k=8)
            email = f'{username}@gmail.com'
            password = '12345678'
            user = CustomUser.objects.create(username=username,
                                             password=password,
                                             email=email)
            self.users.append(user)
    
    def __create_userbookrelation(self):
        for book in self.books:
            for user in self.users:
                bookmark = random.choice[1, 2, 3, 4]
                rate = random.choice[list(range(6))]
                UserBookRelation.objects.create(book=book, user=user,
                                                bookmark=bookmark, rate=rate)

    def __call__(self):
        self.__create_books()
        self.__create_users()
        self.__create_userbookrelation()
        print('Done')

result = FillDbWithDataClass()
result()
