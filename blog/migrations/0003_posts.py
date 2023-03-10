# Generated by Django 4.1.5 on 2023-01-15 11:50

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_customuser_birth_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(max_length=64, null=True, verbose_name='Заголовок')),
                ('text', models.TextField(null=True, verbose_name='Текст поста')),
                ('posting_date', models.DateField(default=datetime.datetime(2023, 1, 15, 11, 50, 22, 913816))),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
