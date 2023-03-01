# Generated by Django 4.1.7 on 2023-02-28 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_alter_customer_zipcode"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderplaced",
            name="status",
            field=models.CharField(
                choices=[
                    ("Accepted", "Accepted"),
                    ("Packed", "Packed"),
                    ("Delivered", "Delivered"),
                    ("On The Way", "On The Way"),
                    ("Cancel", "Cancel"),
                ],
                default="Pending",
                max_length=50,
            ),
        ),
    ]