import re

from django.core.exceptions import ValidationError


def validate_username(username):
    reg = re.compile(r'^[\w.@+-]+')
    if not reg.match(username):
        ValidationError(
            'В username недопустимые символы'
        )

    if username == 'me':
        raise ValidationError(
            'Имя пользователя не может быть me'
        )
