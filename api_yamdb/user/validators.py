import re

from django.core.exceptions import ValidationError


def validate_username(username):
    pattern = r"^[\w.@+-]+$"
    match = re.fullmatch(pattern, username,)

    if not match:
        ValidationError(
            'В username недопустимые символы'
        )

    if username == 'me':
        raise ValidationError(
            'Имя пользователя не может быть me'
        )
    return username
