from django.contrib import admin

from reviews.models import Review, Comment, Title


admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Title)
