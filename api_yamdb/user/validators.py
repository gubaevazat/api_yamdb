import re

from django.core.exceptions import ValidationError


def validate_username(username):

    if not re.match(r'^[\w.@+-]+$', username):
        ValidationError(
            'В username недопустимые символы'
        )

    if username == 'me':
        raise ValidationError(
            'Имя пользователя не может быть me'
        )
    return username
