# Generated by Django 4.1.7 on 2023-05-08 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_notes_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notes',
            name='data',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='notes',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
