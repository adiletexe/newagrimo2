# Generated by Django 4.2.1 on 2023-07-21 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_shapes_shape'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='farm',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='region',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]