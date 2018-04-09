# Generated by Django 2.0.1 on 2018-03-15 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cloudlaunch', '0004_add_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publickey',
            name='user_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='public_key', to='djcloudbridge.UserProfile'),
        ),
    ]