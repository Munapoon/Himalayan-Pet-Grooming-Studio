

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0007_appointment_balance_amount_appointment_paid_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='image',
            field=models.ImageField(blank=True, help_text='Upload a picture for the service.', null=True, upload_to='services/'),
        ),
    ]
