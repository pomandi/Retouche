# Generated by Django 4.1.7 on 2023-10-05 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tailoring', '0003_alter_customer_email_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='email_content',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='sms_content',
        ),
    ]
