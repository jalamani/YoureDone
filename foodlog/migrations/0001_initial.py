# Generated by Django 2.2.1 on 2019-06-08 21:10

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Foodlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eat_date', models.DateField(default=datetime.date.today, verbose_name='Date Eaten')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_text', models.CharField(default='NA', max_length=20)),
                ('calories', models.IntegerField(default=0)),
                ('foodlist', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='foodlog.Foodlist')),
            ],
        ),
    ]
