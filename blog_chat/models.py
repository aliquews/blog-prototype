from django.db import models

from blog.models import CustomUser
# Create your models here.


class Message(models.Model):
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='owner_messages')
    chat = models.ForeignKey(
        'Chat', on_delete=models.CASCADE, related_name='chat_instance', null=True)
    text = models.TextField()
    timestamp = models.TimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.owner.username}: {self.text}'

    @classmethod
    def last_10_messages(cls):
        return Message.objects.order_by('-timestamp').all()[:10]


class Chat(models.Model):
    user1 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='user2')

    def __str__(self) -> str:
        return f'{self.pk}'

    def last_message_in_chat(self):
        return Message.objects.filter(chat=self.pk).order_by('-timestamp').all[:1]
