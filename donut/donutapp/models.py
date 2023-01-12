from django.db import models
from datetime import datetime
from django.core.validators import *
from django.contrib.auth.models import User
from PIL import Image, ImageDraw
from django.core.files import File
import qrcode
from io import BytesIO


def default_datetime():
    return datetime.now()


MALE_CHOICES = (
    ('female', 'FEMALE'),
    ('male', 'MALE'),
)

LIKE_CHOICES = {
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
}


class Profile(models.Model):
    name = models.CharField(max_length=100, default='none')
    following = models.ManyToManyField(User, related_name='following', blank=True)
    img = models.ImageField(upload_to='images/', default='images/default.png')
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    male = models.CharField(max_length=6, choices=MALE_CHOICES, default='male')
    qr_code = models.ImageField(upload_to='qr_code/', blank=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        qrcode_img = qrcode.make('http://localhost:8000/' + str(self.pk))
        canvas = Image.new('RGB', (350, 350), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class Posts(models.Model):
    description = models.TextField(max_length=2000)
    date = models.DateTimeField(default=default_datetime)
    user = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE, related_name='creators')
    img = models.ImageField(upload_to='posts/')
    liked = models.ManyToManyField(User, default=None, blank=True)

    @property
    def num_likes(self):
        return self.liked.all().count()

    def save(self, **kwargs):
        super().save()
        img = Image.open(self.img.path)

        if img.height > 900 or img.width > 900:
            output_size = (720, 900)
            img.thumbnail(output_size)
            img.save(self.img.path)

    def __str__(self):
        return "Публикация пользователя: " + str(self.user)


class Facts(models.Model):
    description = models.TextField(max_length=2000)

    def __str__(self):
        return "Факт № " + str(self.pk)