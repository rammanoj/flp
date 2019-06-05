# Generated by Django 2.2 on 2019-06-04 05:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20190604_0512'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postfilerecomment',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='postfilerecomment',
            name='user',
        ),
        migrations.AddField(
            model_name='postcomment',
            name='postfile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.PostFile'),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Post'),
        ),
        migrations.DeleteModel(
            name='PostFileComment',
        ),
        migrations.DeleteModel(
            name='PostFileReComment',
        ),
    ]
