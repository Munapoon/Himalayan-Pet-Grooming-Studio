

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0009_servicereview_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicereview',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
