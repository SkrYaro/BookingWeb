from django.utils import timezone

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(blank=True,null=True,max_length=1000,default="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBwgHBgkIBwgKCgkLDRYPDQwMDRsUFRAWIB0iIiAdHx8kKDQsJCYxJx8fLT0tMTU3Ojo6Iys/RD84QzQ5OjcBCgoKDQwNGg8PGjclHyU3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3Nzc3N//AABEIAMAAzAMBIgACEQEDEQH/xAAbAAEBAQADAQEAAAAAAAAAAAAAAQUDBAYCB//EADIQAQACAQIDBQUHBQAAAAAAAAABAgMEEQUhMRITQVFxIlJhcpEUFSQzU2LBMkJEobH/xAAVAQEBAAAAAAAAAAAAAAAAAAAAAf/EABYRAQEBAAAAAAAAAAAAAAAAAAABEf/aAAwDAQACEQMRAD8A/KAFQAAAAAAAAAAAAAAAAAAAAAABAUSFABAJNwAVFAAAAAAAEWAAAEVOQKgAQqKAACQqKAioCoACooAG4J6cyOc7RHPyafDuGd/WMufeuOelfebOHBjwViMVK0iPKOa4PMV02e0b1w5Jj5ZLafNSN74ckR5zWXqpjf4+pt6GDyM8p2SHqs+lw56zGSkT8Y5SwdforaSYmJ7WOeljB1AEBFQA8AAlUUABBFBQABNhQAADd2eHaeNTqqY5jekc7ejqtngFI7Oa/jvELBrREREREdFHBrdR9m098sc5jlAOceVy58uW82yZbTafj0c2h1uXT5axa9pxzO1omdwekcefFTNitjvHK0bS+4nfmoPJ5sU4slsdutZ2cbR45Ts6uLR/dXeWd4oKigCKAAAIoAAAAAAAACNzgPLT5I/f/DEbfA71rgyRMxv2vGfgsGoz+Nx+Cj54d7vK+9X6s3jeSs6WK9qN5tExEAxJlNxyYadvLSnnMQD1OLljrH7YfaRG0beS+IMXj35uL5ZZLS43ftamlfKrNhBQAAAAAAAAAAABJWAAAAAAQBocGwd9q+8tHs443nbzdGsTa0ViN5npHm9Lw/TRpdPFdvbnnefio7KWnZWfxfVdzgmlZ9vJG0fCPEGNrcvfaq946b7R6OEj13EAEBRFAEhQAAAAAAQJAWBFAAABzaTD9o1FMXhPX0WDS4LpP8nLHOf6In/rXfFaxSsVrG1YjaPR9bxHUHHqMtMOK2S8+zWN5eZ1Oe2oy2yXnr0jyh3uM6qb5YwVn2ac7erM2QUABCQFEAIVIUAAEhUUAAEFARQAAAavAcUTky5fKOzDK6NvgO3cZZ/csGo4tTk7rT5Mnu13crqcUn8Bl28gectabTNrTvM85lDfkIAAJIoAioCgAAAAAAAAAAAAAOzo9bl0kzNNrRPWLOs7/DdBXWVva+SaxWdtojmsHJ99Zv0sf+3FqeKZs+G2OaUrFuuzufcmL9bJ9IfOXg2KmK1q5rzMRM7TsDHjoJ0VAAABAUAAAAEQIVFUQAAAFEUAAEno3OA/k5fm/hiO/wAO19dJW9bUm0WnflPQHoHFqeeDJv7suhPGsX6V/rDizcYpfHatMV95jbnsujJ8IISN/FYQBFBEUANwAiVQBQQFAARUAIADxVPFQAAEUBAAFhFgAAER9SgAAKJCgAAQAAigIKkgKQAAAAAgoAAAAAAAigAAAAP/2Q==")
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
    time_start = models.DateTimeField(blank=False)
    time_end = models.DateTimeField(blank=False)
    time_contract = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Book_Others"
        unique_together = ('title','customer')

    def __str__(self):
        return self.title.title

    def clean(self):
        if not self.time_start or not self.time_end:
            raise ValidationError('Укажіть час початку і кінця оренди ')
            return
        if self.customer == self.title.owner:
            raise ValidationError('Не можна заказувати в самого себе')
        if self.time_start >= self.time_end:
            raise ValidationError('Час завершення має бути пізніше за час початку.')

        if self.time_start < timezone.now():
            raise ValidationError('Не можна бронювати час у минулому.')

        if self.title and self.time_start and self.time_end:
            overlapping = Book.objects.filter(
                title=self.title,
                time_start__lt=self.time_end,
                time_end__gt=self.time_start,
            ).exclude(id=self.id)

            if overlapping.exists():
                raise ValidationError('Цей час уже зайнятий іншим бронюванням.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Запуск clean() перед збереженням
        super().save(*args, **kwargs)

class Profile(models.Model):
    genders = (
        ("man","Чоловік"),
        ("woman","Жінка")
    )
    name = models.OneToOneField(User ,on_delete=models.CASCADE)
    gender = models.CharField(choices=genders,max_length=100,blank=True,null=True)
    date_of_birth = models.DateTimeField(null=True,blank=True, default=None)
    avatar = models.TextField(blank=True, null=True,default=' ')
    bio = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.name.username

