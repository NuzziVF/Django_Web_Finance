# Generated by Django 4.1.3 on 2022-12-02 15:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("login", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stock",
            name="date",
        ),
    ]