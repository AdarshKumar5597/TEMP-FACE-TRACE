# Generated by Django 4.2.4 on 2023-11-02 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tempfacetrace', '0009_remove_imagedetails_id_alter_imagedetails_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagedetails',
            name='studentid',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
