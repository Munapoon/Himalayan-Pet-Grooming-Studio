

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_user_is_email_verified_user_verification_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='priority',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', max_length=20),
        ),
    ]
