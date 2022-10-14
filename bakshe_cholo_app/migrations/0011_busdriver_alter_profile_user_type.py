# Generated by Django 4.1.2 on 2022-10-14 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bakshe_cholo_app", "0010_user_coordinates_created_at"),
    ]

    operations = [
        migrations.CreateModel(
            name="BusDriver",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("bus_title", models.CharField(max_length=100)),
                ("bus_route", models.CharField(max_length=200)),
                ("bus_sits", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name="profile",
            name="user_type",
            field=models.CharField(
                choices=[
                    ("Regular User", "Regular User"),
                    ("Bus Driver", "Bus Driver"),
                ],
                default="Regular User",
                max_length=100,
            ),
        ),
    ]
