# Generated by Django 5.0.4 on 2024-04-06 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_alter_author_options_alter_quote_options'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='author',
            table='author',
        ),
        migrations.AlterModelTable(
            name='quote',
            table='quote',
        ),
    ]