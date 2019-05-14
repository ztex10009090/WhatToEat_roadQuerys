# Generated by Django 2.1.7 on 2019-03-31 05:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classify',
            fields=[
                ('ClassifyID', models.AutoField(primary_key=True, serialize=False)),
                ('ClassifyName', models.CharField(max_length=50)),
                ('TagColor', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('CommentID', models.AutoField(primary_key=True, serialize=False)),
                ('StarAmount', models.IntegerField(default=0)),
                ('CommentContent', models.CharField(max_length=200)),
                ('CreateDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='RoadQuery',
            fields=[
                ('RoadQueryID', models.AutoField(primary_key=True, serialize=False)),
                ('RoadQueryName', models.CharField(max_length=50)),
                ('RoadQueryAddress', models.CharField(max_length=50)),
                ('RoadQueryPicture', models.CharField(blank=True, max_length=100)),
                ('Introduction', models.TextField()),
                ('Star', models.IntegerField(default=0)),
                ('OpenTime', models.CharField(max_length=50)),
                ('Latitude', models.CharField(max_length=30)),
                ('Longitude', models.CharField(max_length=30)),
                ('CreateDate', models.DateTimeField()),
                ('ModifyDate', models.DateTimeField()),
                ('Classify', models.ManyToManyField(to='roadQuerys.Classify')),
                ('CreateUser', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='RoadQuery_CreateUser', to='users.UserAccount')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='RoadQuery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Comment_RoadQuery', to='roadQuerys.RoadQuery'),
        ),
        migrations.AddField(
            model_name='comment',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='Comment_User', to='users.UserAccount'),
        ),
    ]