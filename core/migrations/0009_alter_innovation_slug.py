# Generated by Django 5.0.4 on 2024-05-04 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_innovation_categories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='innovation',
            name='slug',
            field=models.SlugField(blank=True, default='djangodbmodelsfieldscharfield-2024-05-04-074105466388', unique=True),
        ),
    ]
