from django.db import models
from django.contrib.auth import settings
from django.utils import timezone
from django.contrib.auth.models import UserManager, AbstractUser
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
import jwt


class ObjectManager(models.Manager):
    def get_queryset(self):
        return super(ObjectManager, self).get_queryset().all()


class User(AbstractUser):
    """Модель пользователя"""

    objects = UserManager()

    user_id_tg = models.IntegerField(verbose_name='Id пользователя в telegram', unique=True, null=True, blank=True)
    birthday = models.DateField(verbose_name='Дата рождения', null=True, blank=True)
    warn = models.IntegerField(verbose_name='количество нарушений', default=0, null=True, blank=True)
    hash_tg = models.CharField(verbose_name='хеш телеграмм', max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'username'

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        ordering = ['username']
        verbose_name = 'Мембер'
        verbose_name_plural = 'Мемберы'

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=30)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')


class Faq(models.Model):
    """ Модель справки."""

    objects = ObjectManager()

    title = models.CharField(verbose_name='Тема', max_length=128, unique=True)
    description = models.TextField(verbose_name='Содержание', max_length=255)

    class Meta:
        ordering = ['title']
        verbose_name = 'Справка'
        verbose_name_plural = 'Справки'

    def __str__(self):
        return self.title


class Block(models.Model):
    """
    Модель блокировки юзверя. В блок можно отправить только существующего юзверя
    Переопределенный save() при использовании добавляет Member'у одно нарушение и высчитывает время
    снятия бана. Если поле permanent модели = True, бан выдается до 9999-го года =Р
    В противном случае высчитывается время в зависимости от количества нарушений пользователя
    """

    objects = ObjectManager()

    user = models.CharField(verbose_name='Мембер', max_length=128)
    start_time = models.DateTimeField(verbose_name='Время начала', default=datetime.now, null=True,
                                      blank=True)  # время понадобится в
    # будущем развитии
    stop_time = models.DateTimeField(verbose_name='Время окончания', null=True, blank=True)
    permanent = models.BooleanField(verbose_name='Бан перманентно', default=False, null=True, blank=True)
    warn = models.IntegerField(verbose_name='Нарушение', default=1, null=True, blank=True)

    class Meta:
        verbose_name = 'Блокировка'
        verbose_name_plural = 'Блокировки'

    def __str__(self):
        return self.user

    def save(self, *args, **kwargs):
        """ Переопределяем сохранение для высчитывания времени бана"""
        user = get_object_or_404(User, user_id_tg=self.user)
        user.warn += 1
        user.save()
        self.warn = user.warn
        if self.permanent:
            self.stop_time = datetime(9999, 12, 1, 12, 00, 00)
        else:
            block_time = user.warn * 10 + (user.warn - 1) * 10
            self.stop_time = timezone.now() + timezone.timedelta(minutes=block_time)
        super(Block, self).save(*args, **kwargs)


class Poll(models.Model):

    """Модель голосования юзверей"""

    objects = ObjectManager()

    keyboard_id = models.IntegerField(verbose_name='Голосование', null=False, blank=False)
    user_id = models.IntegerField(verbose_name='Кто голосовал', null=False, blank=False)
    total_voted = models.IntegerField(verbose_name='Общее количество голосов', null=True, blank=True, default=1)

    class Meta:
        ordering = ['-keyboard_id']  # сортируем в обратном порядке, что бы последние были сверху в админке
        unique_together = ['keyboard_id', 'user_id']  # задаем уникальность что бы не было повторных голосов
        verbose_name = 'Голосование'  # удобочитаемое имя в единственном числе
        verbose_name_plural = 'Голосования'  # удобочитаемое имя во множественном числе

    def __str__(self):
        return str(self.keyboard_id)  # возвращаем удобочитаемое имя объекта

    def save(self, *args, **kwargs):
        polls = Poll.objects.filter(keyboard_id=self.keyboard_id)  # получаем все голосовалки по ид
        amount = polls.count()  # получаем сумму всех голосов
        for poll in polls:  # запускаем цикл по голосовалкам
            if poll.user_id == self.user_id:  # проверяем голосовал ли юзер
                self.total_voted = amount  # если голосовал сумму не меняем
                return  # просто возвращаем
            else:  # если не голосовал
                self.total_voted = amount + 1  # добавляем его голос
        super(Poll, self).save(*args, **kwargs)  # сохраняем в БД и возвращаем
