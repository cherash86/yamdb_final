from csv import DictReader
from django.core.management.base import BaseCommand
from reviews import models
from users.models import CustomUser


class Command(BaseCommand):
    help = "Loads data from csv"

    def handle(self, *args, **options):
        print('Loadind csv data')

        for row in DictReader(
                open('static/data/category.csv', encoding="utf8")):
            obj = models.Category(name=row['name'], slug=row['slug'])
            obj.save()

        for row in DictReader(open('static/data/genre.csv', encoding="utf8")):
            obj = models.Genre(name=row['name'], slug=row['slug'])
            obj.save()

        for row in DictReader(open('static/data/titles.csv', encoding="utf8")):
            obj = models.Title(name=row['name'], year=row['year'],
                               category=models.Category.objects.get(
                               id=row['category']))
            obj.save()

        for row in DictReader(
                open('static/data/genre_title.csv', encoding="utf8")):
            title = models.Title.objects.get(id=row['title_id'])
            genre = models.Genre.objects.get(id=row['genre_id'])
            title.genre.add(genre)

        for row in DictReader(open('static/data/users.csv', encoding="utf8")):
            obj = CustomUser(id=row['id'], username=row['username'],
                             email=row['email'], role=row['role'],
                             bio=row['bio'], first_name=row['first_name'],
                             last_name=row['last_name'])
            obj.save()

        for row in DictReader(open('static/data/review.csv', encoding="utf8")):
            obj = models.Review(title=models.Title.objects.get(
                                id=row['title_id']),
                                text=row['text'],
                                author=CustomUser.objects.get(
                                id=row['author']),
                                score=row['score'],
                                pub_date=row['pub_date'])
            obj.save()

        for row in DictReader(
                open('static/data/comments.csv', encoding="utf8")):
            obj = models.Comment(review=models.Review.objects.get(
                                 id=row['review_id']),
                                 text=row['text'],
                                 author=CustomUser.objects.get(
                                 id=row['author']),
                                 pub_date=row['pub_date'])
            obj.save()
