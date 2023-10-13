# Generated by Django 4.2.4 on 2023-08-25 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tempfacetrace', '0002_attendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('studentname', models.CharField(max_length=50)),
                ('studentid', models.IntegerField()),
                ('date', models.DateField()),
                ('query', models.CharField(max_length=300)),
            ],
            options={
                'db_table': 'queriesdb',
            },
        ),
    ]
