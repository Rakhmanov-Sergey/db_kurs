from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.db import transaction

# Create your models here.


class User(AbstractUser):
    TYPE_CHOICES = (('manager', 'Организатор мероприятия'), ('client', 'Заказчик'), ('editor', 'Музыкальный редактор'))
    type = models.CharField(max_length=20, blank=True, choices=TYPE_CHOICES)

    def save(self, *args, **kwargs):
        self.is_staff = True

        if self.type == 'client':
            group = Group.objects.get(name='clients')
        elif self.type == 'editor':
            group = Group.objects.get(name='editors')
        elif self.type == 'manager':
            group = Group.objects.get(name='managers')

        super(User, self).save(*args, **kwargs)
        self.groups.add(group)


class Song(models.Model):
    name = models.CharField(max_length=20, verbose_name="Название")
    artist = models.CharField(max_length=20, verbose_name="Исполнитель")
    file_name = models.CharField(max_length=50, verbose_name="Название музыкального файла")

    class Meta:
        verbose_name = "музыкальную композицию"
        verbose_name_plural = "музыкальные композиции"

    def has_rights(self):
        rights = SongRights.objects.filter(name=self.name, artist=self.artist, status="confirmed")
        return len(rights) != 0

    has_rights.boolean = True
    has_rights.verbose_name = "Имеются права"

    def __str__(self):
        return "%s - %s" % (self.artist, self.name)


class SongRights(models.Model):
    SONG_RIGHTS_CHOICES = (('requested', 'Запрос отправлен'), ('processing', 'В обработке'), ('confirmed', 'Подтверждено'))
    name = models.CharField(max_length=20, verbose_name="Название")
    artist = models.CharField(max_length=20, verbose_name="Исполнитель")
    organization = models.CharField(max_length=50, verbose_name="Организация")
    status = models.CharField(max_length=20, choices=SONG_RIGHTS_CHOICES)

    class Meta:
        verbose_name = "права на композицию"
        verbose_name_plural = "права на композицию"

    def __str__(self):
        return "Права на композицию %s - %s" % (self.artist, self.name)


class Client(models.Model):
    number = models.CharField(max_length=20, blank=True, verbose_name="номер телефона")
    card_number = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "заказчика"
        verbose_name_plural = "заказчики"

    def __str__(self):
        return "Заказчик %s %s" % (self.user_id.first_name, self.user_id.last_name)


class Editor(models.Model):
    staff_code = models.CharField(max_length=20, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "редактора"
        verbose_name_plural = "редакторы"

    def __str__(self):
        return "Музыкальный редактор %s %s" % (self.user_id.first_name, self.user_id.last_name)


class Manager(models.Model):
    staff_code = models.CharField(max_length=20, blank=True, verbose_name="Номер сотрудника")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "организатора"
        verbose_name_plural = "организаторы"

    def __str__(self):
        return "Организатор %s %s" % (self.user_id.first_name, self.user_id.last_name)


class Request(models.Model):
    STATE_CHOICES = (('processing', 'В обработке'), ('confirmed', 'Подтверждена'))
    date = models.DateTimeField(verbose_name='Дата начала')
    state = models.CharField(max_length=20, choices=STATE_CHOICES, verbose_name='Статус')
    music = models.TextField(verbose_name='Список музыки')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "запрос"
        verbose_name_plural = "запросы"

    def __str__(self):
        return "Запрос от %s на %s" % (self.user.first_name, self.date)


class Event(models.Model):
    date = models.DateTimeField(verbose_name="Дата начала")
    songs = models.ManyToManyField(Song, verbose_name="Список музыкальных композиций")
    host = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Запрос")

    class Meta:
        verbose_name = "мероприятие"
        verbose_name_plural = "мероприятия"

    def __str__(self):
        return "Мероприятие в %s" % self.date
