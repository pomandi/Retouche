# Generated by Django 4.1.7 on 2023-11-11 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tailoring', '0011_alter_customer_email_content_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='order_ready',
            field=models.BooleanField(default=False),
        ),
    ]
