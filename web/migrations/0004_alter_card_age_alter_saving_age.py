# Generated by Django 4.1.1 on 2022-10-11 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("web", "0003_card_age_saving_age"),
    ]

    operations = [
        migrations.AlterField(
            model_name="card", name="age", field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="saving", name="age", field=models.CharField(max_length=100),
        ),
    ]
