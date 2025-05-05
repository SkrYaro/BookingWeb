from django.utils import timezone

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name="owner", on_delete=models.CASCADE)
    cost = models.IntegerField()
    description = models.TextField(null=True)
    add_at = models.DateTimeField(auto_now=True)
    upt_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}({self.owner})"

    class Meta:
        verbose_name_plural = "Posts for selling"


class Book(models.Model):
    title = models.ForeignKey(Post, related_name='book_title', on_delete=models.CASCADE)
    customer = models.ForeignKey(User, related_name='customer', on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    time_contract = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Rents"
        unique_together = ('title','customer')

    def __str__(self):
        return self.title.title

    def clean(self):
        if self.time_start >= self.time_end:
            raise ValidationError('Час завершення має бути пізніше за час початку.')

        if self.time_start < timezone.now():
            raise ValidationError('Не можна бронювати час у минулому.')

        overlapping = Book.objects.filter(
            time_start__lt=self.time_end,
            time_end__gt=self.time_start,
        ).exclude(id=self.id)

        if overlapping.exists():
            raise ValidationError('Цей час уже зайнятий іншим бронюванням.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Запуск clean() перед збереженням
        super().save(*args, **kwargs)

