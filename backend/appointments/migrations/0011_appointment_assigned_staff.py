

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appointments', '0010_servicereview_is_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='assigned_staff',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'staff'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_appointments', to=settings.AUTH_USER_MODEL),
        ),
    ]
