import csv
import lorem
import string
import random
from tqdm import tqdm
from time import sleep
from pathlib import Path

from django.core.management.base import BaseCommand
from django.urls import reverse
from django.test import Client
from django.core.files import File  # you need this somewhere
from django.core.exceptions import MultipleObjectsReturned

from genres.models import Genre
from authors.models import Author
from books.models import Book, UserBookRelation
from users.models import User


class Command(BaseCommand):
    """Class to fill db with data from book database and lorem description.
    Usage: assign class to some variable and then call this variable as function"""
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    file_path = BASE_DIR.joinpath('staticfiles') / 'main_dataset.csv'
    imgs_path = BASE_DIR.joinpath('staticfiles')\
                        .joinpath('book-covers')

    def add_arguments(self, parser):
        parser.add_argument(
            '--books',
            default='100',
            help='Amount of book for every genre that will fill db'
            )
        parser.add_argument(
            '--genres',
            default='33',
            help='Amount of genres that will fill db, default 33'
            )

    def handle(self, *args, **options):
        self.book_amount = int(options.get('books'))
        self.genre_amount = int(options.get('genres'))
        self.users_pk = self.__create_users()
        self.__create_books()
        self.stdout.write(self.style.SUCCESS('Db has filled!'))

    def __create_books(self):
        """Main function that read a csvfile and create book and
        random userbookrelation"""
        with open(self.file_path) as csvfile:
            csvreader = csv.reader(csvfile)
            columns_names = next(csvreader)
            genre_list = []

            for row in tqdm(csvreader):

                name = row[columns_names.index('name')]
                author = row[columns_names.index('author')].strip()
                if author == '':
                    continue
                genre = row[columns_names.index('category')]
                if genre not in genre_list:
                    genre_list.append(genre)
                if self.genre_amount:
                    if len(genre_list) == self.genre_amount:
                        break

                if Book.objects.filter(genre__name=genre).count() == self.book_amount:
                    continue

                photo_url = self.imgs_path / row[columns_names.index('img_paths')].split('dataset/')[1]
                
                try:
                    genre_obj = Genre.objects.get_or_create(name=genre)[0]
                    try:
                        author_obj = Author.objects.get_or_create(
                            name=author,
                            defaults={'biography': lorem.text()}
                            )[0]
                    except:
                        continue
                    if not Book.objects.filter(name__iexact=name).exists():
                        book = Book.objects.create(
                            name=name,
                            author=author_obj,
                            about=lorem.text()
                            )
                        book.genre.add(genre_obj)
                        book.photo.save(photo_url.name,
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
            user = User.objects.create(username=username,
                                             password=password,
                                             email=email)
            users_pk.append(user.pk)
        return users_pk
    
    def __create_userbookrelation(self, book):
        """Creating random bookmark and rate"""
        for user in User.objects.filter(pk__in=self.users_pk):
            bookmark = random.choice([1, 2, 3, 4])
            rate = random.choice(list(range(6)))
            UserBookRelation.objects.create(book=book, user=user,
                                            bookmarks=bookmark, rate=rate)

    def __delete_old_users(self):
        User.objects.all().exclude(pk__lt=7).delete()

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
