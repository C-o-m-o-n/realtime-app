# Generated by Django 4.1.7 on 2023-04-12 16:29

from django.db import migrations, models
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_school_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='optional_image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, upload_to='user_avatar/optional/', verbose_name='Optional Image'),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='user_avatars'),
        ),
    ]
