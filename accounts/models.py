from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager)
from django.core import validators
from django.db import models
import re


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(
        'Apelido / Usuário',
        max_length=30,
        unique=True,
        validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'Informe um nome válido. '
                'Este valor deve conter apenas letras, números '
                'e os caracteres: @/./+/-.',
                'invalid'
            )
        ],
        help_text='Um nome curto que será usado para identifica-lo de forma única na plataforma'
    )
    name = models.CharField('Nome', max_length=100)
    email = models.EmailField('E-mail', unique=True)
    is_staff = models.BooleanField('Membro da Equipe', default=False)
    is_active = models.BooleanField('Ativo', default=False)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    object = UserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.name or self.username

    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return str(self).split(' ')[0]

