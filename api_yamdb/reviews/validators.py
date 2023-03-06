from datetime import datetime

from django.core.exceptions import ValidationError


def validate_year(year):
    if year > datetime.now().year:
        raise ValidationError(
            'Год выпуска произведения не может быть больше текущего!'
        )
