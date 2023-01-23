from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    username = models.CharField(max_length=32, unique=True, help_text='Никнейм')
    email = models.EmailField(max_length=32, help_text='Электронная почта')
    first_name = models.CharField(max_length=32, help_text='Имя')
    last_name = models.CharField(max_length=32, help_text='Фамилия')
    avatar = models.ImageField('profile avatar', null=True, upload_to=f'uploads/{username}/', help_text='Аватар')


    def __str__(self) -> str:
        return f'{self.username}'


class Post(models.Model):

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    header = models.CharField(
        "Заголовок",
        max_length=64,
        null=True,
    )
    text = models.TextField(
        "Текст поста",
        null=True,
    )
    posting_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.owner}: {self.header}'

class Comment(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField("Текст комментария", null=True)
    posting_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.owner} to {self.post}'