

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0010_alter_appointment_pet_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='pet_type',
            field=models.CharField(choices=[('dog', 'Dog'), ('cat', 'Cat')], default='dog', max_length=20),
        ),
    ]
