from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title

admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Title)
admin.site.register(Category)
admin.site.register(Genre)
