from django.db import models


class MultipleChoicesField(models.Field):
    """Custom field for handling challenges multiple choices.

    Ayah based challenge:
        Python representation:
            (
                <Ayah: '2:182'>,
                <Ayah: '2:192'>,
                <Ayah: '2:181'>,
                <Ayah: '3:182'>,
            )
        Database representation:
            '2:182;2:192;2:181;3:182'

    Word based challenge:
        Python representation:
            [
                ('a', 'b', 'c', 'd'),
                ('e', 'f', 'g', 'h'),
                ...
            ]
        Database representation:
            'a,b,c,d;e,f,g,h;...'
    """
