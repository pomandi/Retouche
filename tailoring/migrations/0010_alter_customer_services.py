# Generated by Django 4.1.7 on 2023-10-12 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tailoring', '0009_alter_customer_bus_alter_customer_huisnummer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='services',
            field=models.ManyToManyField(blank=True, to='tailoring.tailoringservice'),
        ),
    ]
