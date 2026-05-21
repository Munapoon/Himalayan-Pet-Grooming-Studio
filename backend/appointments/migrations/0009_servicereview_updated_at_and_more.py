

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0008_service_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicereview',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='advance_amount',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('khalti', 'Khalti'), ('cash', 'Cash in hand'), ('online', 'Online')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='payment_status',
            field=models.CharField(choices=[('pending_payment', 'Pending Payment'), ('unpaid', 'Unpaid'), ('advance_paid', 'Advance Paid'), ('paid', 'Paid'), ('refunded', 'Refunded')], default='unpaid', max_length=20),
        ),
    ]
