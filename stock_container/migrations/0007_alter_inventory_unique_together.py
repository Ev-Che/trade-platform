# Generated by Django 3.2.9 on 2021-12-02 14:45

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stock_management', '0001_initial'),
        ('stock_container', '0006_alter_inventory_user'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='inventory',
            unique_together={('user', 'stock')},
        ),
    ]