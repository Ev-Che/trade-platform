# Generated by Django 3.2.9 on 2021-11-18 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0002_auto_20211117_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Is active'),
        ),
    ]
