# Generated by Django 4.1.3 on 2022-12-20 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inferimages', '0003_alter_imagetask_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagetask',
            name='image_after',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]