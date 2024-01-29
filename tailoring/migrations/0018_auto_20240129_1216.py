from django.db import migrations, models
import uuid

def generate_unique_tracking_ids(apps, schema_editor):
    Customer = apps.get_model('tailoring', 'Customer')
    for customer in Customer.objects.all():
        while True:
            tracking_id = uuid.uuid4()
            if not Customer.objects.filter(tracking_id=tracking_id).exists():
                break
        customer.tracking_id = tracking_id
        customer.save()

class Migration(migrations.Migration):

    dependencies = [
        ('tailoring', '0017_customer_tracking_id'),  # Replace with the name of your previous migration
    ]

    operations = [
        migrations.RunPython(generate_unique_tracking_ids),
    ]