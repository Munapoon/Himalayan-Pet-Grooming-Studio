

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_payment_appointment_alter_payment_order'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='cart',
            name='size',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='size',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='cart',
            unique_together={('user', 'product', 'size')},
        ),
    ]
