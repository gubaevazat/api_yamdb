import codecs
import csv
import os.path

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from user.models import User


class Command(BaseCommand):
    help = 'load data from csv'

    def handle(self, *args, **options):

        load_dir = os.path.join(f'{settings.BASE_DIR}', 'static', 'data')

        with codecs.open(os.path.join(load_dir, 'category.csv'),
                         "r", "utf_8_sig") as csv_file:
            print('Загрузка сategory.csv...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                category = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                category.save()
            print('Загрузка сategory.csv завершена.')

        with codecs.open(os.path.join(load_dir, 'genre.csv'), "r",
                         "utf_8_sig") as csv_file:
            print('Загрузка genre.csv...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                genre = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                genre.save()
            print('Загрузка genre.csv завершена.')

        with codecs.open(os.path.join(load_dir, 'titles.csv'),
                         "r", "utf_8_sig") as csv_file:
            print('Загрузка titles.csv...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                category = Category.objects.get(pk=row['category'])
                title = Title(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=category
                )
                title.save()
            print('Загрузка titles.csv завершена.')

        with codecs.open(os.path.join(load_dir, 'genre_title.csv'),
                         "r", "utf_8_sig") as csv_file:
            print('Загрузка genre_title.csv...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                title = Title.objects.get(pk=row['title_id'])
                genre = Genre.objects.get(pk=row['genre_id'])
                genre_title = GenreTitle(
                    id=row['id'],
                    title=title,
                    genre=genre
                )
                genre_title.save()
            print('Загрузка genre_title.csv завершена.')

        with codecs.open(os.path.join(load_dir, 'users.csv'),
                         "r", "utf_8_sig") as csv_file:
            print('Загрузка users.csvv...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                user = User(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
                user.save()
            print('Загрузка users.csv завершена.')

        with codecs.open(os.path.join(load_dir, 'review.csv'),
                         "r", "utf_8_sig") as csv_file:
            print('Загрузка review.csv...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                title = Title.objects.get(pk=row['title_id'])
                author = User.objects.get(pk=row['author'])
                review = Review(
                    id=row['id'],
                    title=title,
                    text=row['text'],
                    author=author,
                    score=row['score'],
                    pub_date=row['pub_date']
                )
                review.save()
            print('Загрузка review.csv завершена.')

        with codecs.open(os.path.join(load_dir, 'comments.csv'),
                         "r", "utf_8_sig") as csv_file:
            print('Загрузка comments.csv...')
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                review = Review.objects.get(pk=row['review_id'])
                author = User.objects.get(pk=row['author'])
                comments = Comment(
                    id=row['id'],
                    review=review,
                    text=row['text'],
                    author=author,
                    pub_date=row['pub_date']
                )
                comments.save()
            print('Загрузка comments.csv завершена.')
            print('Все файлы загружены!')
