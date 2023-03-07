import re

from django.core.exceptions import ValidationError


def validate_username(username):
    if not bool(re.match(r'^[\w.@+-]+$', username)):
        raise ValidationError(
            'Некорректные символы в username.'
            'Используйте цифры, буквы и символы: точка @, +, -, _'
        )

    if username.lower() == 'me':
        raise ValidationError(
            'Имя пользователя не может быть me'
        )
    return username
