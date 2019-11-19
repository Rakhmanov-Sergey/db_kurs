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
    name = models.CharField(max_length=20)
    artist = models.CharField(max_length=20)
    file_name = models.CharField(max_length=50)

    def __str__(self):
        return "Song %s for %s" % (self.id, list(map(lambda event: "Event#%s" % event.id, self.event_set.all())))


class Event(models.Model):
    date = models.DateField()
    host = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return "Event#%s" % self.id


class SongRights(models.Model):
    SONG_RIGHTS_CHOICES = (('requested', 'Запрос отправлен'), ('processing', 'В обработке'), ('confirmed', 'Подтверждено'))
    organization = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=SONG_RIGHTS_CHOICES)
    song = models.OneToOneField(Song, on_delete=models.CASCADE)

    def __str__(self):
        return "Song rights for song %s with state %s" % (self.song, self.status)


class Client(models.Model):
    number = models.CharField(max_length=20, blank=True)
    card_number = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Client extension for user#%s" % self.user_id.username


class Editor(models.Model):
    staff_code = models.CharField(max_length=20, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Editor extension for user#%s" % self.user_id.username


class Manager(models.Model):
    staff_code = models.CharField(max_length=20, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Manager extension for user#%s" % self.user_id.username


class Request(models.Model):
    STATE_CHOICES = (('processing', 'В обработке'), ('confirmed', 'Подтверждена'))
    date = models.DateTimeField()
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    music = models.TextField()
    event = models.ForeignKey(Event, blank=True, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Request for %s" % self.user.username
