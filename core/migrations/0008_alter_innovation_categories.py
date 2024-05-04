# Generated by Django 5.0.4 on 2024-05-04 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_innovation_dataset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='innovation',
            name='categories',
            field=models.CharField(choices=[('H', 'HIV'), ('T', 'Tuberculosis'), ('A', 'Airborne'), ('W', 'Waterborne'), ('O', 'Other')], default='H', max_length=1, verbose_name='Categories'),
        ),
    ]
