from django.db import migrations, models
import uuid

def create_uuid(apps, schema_editor):
    Customer = apps.get_model('tailoring', 'Customer')
    for customer in Customer.objects.filter(tracking_id__isnull=True):
        # Ensure the generated UUID is unique for each customer
        while True:
            unique_id = uuid.uuid4()
            if not Customer.objects.filter(tracking_id=unique_id).exists():
                break
        customer.tracking_id = unique_id
        customer.save()

class Migration(migrations.Migration):

    dependencies = [
        ('tailoring', '0012_customer_order_ready'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='tracking_id',
            field=models.UUIDField(default=uuid.uuid4, unique=True),
        ),
        migrations.RunPython(create_uuid),
    ]