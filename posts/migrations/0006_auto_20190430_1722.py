# Generated by Django 2.2 on 2019-04-30 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20190430_1243'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='item',
            new_name='file',
        ),
        migrations.AddField(
            model_name='post',
            name='header',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]