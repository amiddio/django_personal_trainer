# Generated by Django 4.2.3 on 2023-08-07 14:09

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('trainer', '0010_alter_comment_options_alter_comment_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trainer',
            name='avatar',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[300, None], upload_to='trainers/%Y/%m/%d/', verbose_name='Фотография'),
        ),
    ]