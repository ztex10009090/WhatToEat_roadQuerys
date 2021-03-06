# Generated by Django 2.1.7 on 2019-03-31 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('UserID', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('UserName', models.CharField(max_length=50)),
                ('UserPicture', models.CharField(blank=True, max_length=100)),
                ('EMail', models.CharField(blank=True, max_length=100)),
                ('Password', models.CharField(max_length=100)),
                ('VerificationCode', models.CharField(blank=True, max_length=10)),
                ('Weight', models.IntegerField(default=0)),
                ('SignInOrigin', models.CharField(default='testPost', max_length=20)),
                ('CreateDate', models.DateTimeField()),
                ('ModifyDate', models.DateTimeField()),
            ],
        ),
    ]
