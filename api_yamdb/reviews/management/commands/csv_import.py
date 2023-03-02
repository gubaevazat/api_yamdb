import csv
import codecs
from django.core.management.base import BaseCommand
from django.conf import settings

from reviews.models import (Title, Genre, Category, GenreTitle,
                            Review, Comment)
from user.models import User


class Command(BaseCommand):
    help = 'load data from csv'

    def handle(self, *args, **options):
        with codecs.open(f'{settings.BASE_DIR}/static/data/category.csv',
                         "r", "utf_8_sig") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                category = Category(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                category.save()

        with codecs.open(f'{settings.BASE_DIR}/static/data/genre.csv', "r",
                         "utf_8_sig") as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                genre = Genre(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                genre.save()

        with codecs.open(f'{settings.BASE_DIR}/static/data/titles.csv',
                         "r", "utf_8_sig") as csv_file:
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

        with codecs.open(f'{settings.BASE_DIR}/static/data/genre_title.csv',
                         "r", "utf_8_sig") as csv_file:
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

        # with codecs.open(f'{settings.BASE_DIR}/static/data/users.csv',
        #                  "r", "utf_8_sig") as csv_file:
        #     csv_reader = csv.DictReader(csv_file, delimiter=',')
        #     for row in csv_reader:
        #         user = User(
        #             id=row['id'],
        #             username=row['username'],
        #             email=row['email'],
        #             role=row['role'],
        #             bio=row['bio'],
        #             first_name=row['first_name'],
        #             last_name=row['last_name']
        #         )
        #         user.save()

        # with codecs.open(f'{settings.BASE_DIR}/static/data/review.csv',
        #                  "r", "utf_8_sig") as csv_file:
        #     csv_reader = csv.DictReader(csv_file, delimiter=',')
        #     for row in csv_reader:
        #         title = Title.objects.get(pk=row['title_id'])
        #         review = Review(
        #             id=row['id'],
        #             title=title,
        #             text=row['text'],
        #             author=row['author'],
        #             score=row['score'],
        #             pub_date=row['pub_date']
        #         )
        #         review.save()

        # with codecs.open(f'{settings.BASE_DIR}/static/data/comments.csv',
        #                  "r", "utf_8_sig") as csv_file:
        #     csv_reader = csv.DictReader(csv_file, delimiter=',')
        #     for row in csv_reader:
        #         review = Title.objects.get(pk=row['review_id'])
        #         author = User.objects.get(pk=row['author'])
        #         comments = Comment(
        #             id=row['id'],
        #             review=review,
        #             text=row['text'],
        #             author=author,
        #             pub_date=row['pub_date']
        #         )
        #         comments.save()
