# Generated by Django 4.1.7 on 2023-04-12 16:03

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_school_avatar_ppoi_alter_school_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='logo',
            field=versatileimagefield.fields.VersatileImageField(upload_to='school'),
        ),
    ]
