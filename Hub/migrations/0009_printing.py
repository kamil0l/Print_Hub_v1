# Generated by Django 4.2.3 on 2023-08-07 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Hub', '0008_delete_printing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Printing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, null=True, upload_to='project_images/')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Hub.project')),
            ],
        ),
    ]
