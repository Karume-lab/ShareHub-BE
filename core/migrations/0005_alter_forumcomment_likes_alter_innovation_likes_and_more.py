# Generated by Django 5.0.4 on 2024-05-08 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_innovation_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumcomment',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='Likes'),
        ),
        migrations.AlterField(
            model_name='innovation',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='Likes'),
        ),
        migrations.AlterField(
            model_name='innovationcomment',
            name='likes',
            field=models.IntegerField(default=0, verbose_name='Likes'),
        ),
    ]
