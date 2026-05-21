

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_payment_appointment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('refunded', 'Refunded')], default='pending', max_length=20),
        ),
        migrations.AlterUniqueTogether(
            name='product',
            unique_together={('name', 'category')},
        ),
    ]
