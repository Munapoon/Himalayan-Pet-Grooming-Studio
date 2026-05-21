

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0011_alter_pet_pet_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='pet_type',
            field=models.CharField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('rabbit', 'Rabbit'), ('other', 'Other')], default='dog', max_length=20),
        ),
    ]
